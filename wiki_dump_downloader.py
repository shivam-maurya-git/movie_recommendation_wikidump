import subprocess
import sys

#winget install aria2
URL = "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"
OUTPUT = "enwiki-latest-pages-articles.xml.bz2"
#Used to run external terminal commands (here: aria2c) from Python.

def download():
    command = [ #aria2c requires arguments in the same order as the terminal, so in Python subprocess.run() you need to preserve that exact sequence.
        "aria2c", #downloader program being called.
        "-x", "16",                # parallel connections
        "-s", "16",                # segments
        "-k", "1M",                # segment size
        "--continue=true",         # resume if interrupted
        "--max-tries=5",           # retry attempts
        "--retry-wait=5",          # wait between retries
        "--file-allocation=none",
        "-o", OUTPUT, #Output filename (stored in variable OUTPUT).
        URL #Download link.
    ]

    try:
        subprocess.run(command, check=True) #check=True → if the command fails, Python raises an exception (CalledProcessError).
        #Python is not downloading the file itself.
# Instead it is telling aria2c (installed software) to perform the download.
        print("Download completed.")
    except subprocess.CalledProcessError:
        print("Download failed.")
        sys.exit(1)

if __name__ == "__main__":
    download()
