import PyPDF2
import os
import sys
import shutil
import ssl
from urllib.request import urlopen

# This is where Convention Master dumps our "printed" PDFs.
fetchURL = f"{os.getenv('CM_URL_BASE')}/printing/cloudPDF.php?k={os.getenv('CM_PDF_KEY')}"
# Some stuff for talking to a server over https.
sslC = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
sslC.check_hostname = False
sslC.verify_mode = ssl.CERT_NONE
# A folder to base our working and output files in. Default is the same folder as this script.
baseFolder = '.'
# A folder for storing the individual PDFs while we're working.
fileDir = os.path.join(baseFolder, 'working')
# A single PDF for our combined files.
outputPDF = os.path.join(baseFolder, 'output.pdf')

# Split PDF file names in the format "XXXX-###.pdf" where "XXXX-" is a prefix that we 
# don't care about, "###" is a positive integer, and ".pdf" is the file extension. 
# Return a list of tuples in the format (###, filename).
def parsePDFNames(names):
    nameList = []
    for name in names:
        nameList.append((int(name.split(sep="-")[-1].split(sep=".")[0]), name))
    return nameList

# Check for our environmental variables.
for env in ('CM_URL_BASE', 'CM_PDF_KEY'):
    if os.getenv(env) == None:
        print(f"Environmental variable '{env}' was not found. Quitting.")
        sys.exit(1)

# Check for write access to the working directory and exit if we can't.
if not os.access(baseFolder, os.W_OK):
    print("Can't write to '"+os.path.abspath(baseFolder)+"'. Quitting.")
    sys.exit(1)

# Check for the working directory we define above and, if not found, create it.
if not os.path.isdir(fileDir):
    os.mkdir(fileDir)

# Check for any old output PDFs files and, if found, delete it.
if os.path.isfile(outputPDF):
    os.remove(outputPDF)

# Check for any old files in our working directory and, if found, delete them.
for f in os.listdir(fileDir):
    os.remove(os.path.join(fileDir, f))

# Loops until finished.
while True:
    # Open our PDF generator URL.
    with urlopen(fetchURL, context=sslC) as pdf:
        # Get download filename from HTTP headers.
        outfile = pdf.headers.get('Content-Disposition', '').split(sep='=')[-1]
        # 'noQueue.txt' is given by the URL when there are no more files left to give.
        if outfile == 'noQueue.txt':
            break
        # If we got a PDF, write it to the working directory.
        with open(os.path.join(fileDir,outfile),'wb') as f:
            shutil.copyfileobj(pdf, f)

# Collect all of the PDFs only.
allPDFs = []
allPDFs += [each for each in os.listdir(fileDir) if each.endswith('.pdf')]

# No files found in the directory.
if len(allPDFs) == 0:
    print("No PDFs in the target directory '"+os.path.abspath(fileDir)+"'. Quitting.")
    sys.exit(1)

# Get a list of (index, filename) pairs from the function and sort them ascending by index.
allPDFs = sorted(parsePDFNames(allPDFs))

# Combine all of the working files into one output PDF.
with open(os.path.join(".", outputPDF), "wb") as outputFile, PyPDF2.PdfWriter() as merger:
    for pdf in allPDFs:
        with open(os.path.join(fileDir, pdf[1]), "rb") as pdfFile:
            merger.append(pdfFile)
    merger.write(outputFile)

# Check for any old files in our working directory and, if found, delete them.
for f in os.listdir(fileDir):
    os.remove(os.path.join(fileDir, f))