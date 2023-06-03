## What is this intended for?
This script grabs PDFs named like "**XXXXX-###.pdf**" from a URL in [Convention Master](https://civetsolutions.com/) ("CM"), which produces 1 PDF per HTTP request, saves them to the filesystem, and combines them into one "**output.pdf**".

## How do I use this?
 * Set up your PDF "cloud printer" in CM and obtain the secret key established at setup.
 * Set environmental variables for your CM install url base (**CM_URL_BASE**), and for the secret key you obtained earlier (**CM_PDF_KEY**) to form **fetchURL**.
 * Adjust any of the **baseFolder**, **fileDir**, or **outputPDF** paths as needed for your circumstances.
 * Print to your "cloud printer" in your Convention Master instance and execute the script.
 * The script will run until a special "no more files" file is given by CM and then produce one combined output file, with pages ordered by the **###** integer in the source filenames.

## What is Mysterium?
[Mysterium](https://mysterium.net/) is the independent annual convention for fans of Myst and to the other games from Cyan, Inc.