#!/bin/python3
'''
    EUgolino
    file name: eugolino.py
    author: Lorenzo Radice
'''

import os
import threading
import requests
from bs4 import BeautifulSoup

from classes.log_manager import LogManager

class DownloadCandidate:
    """
    A class representing a download candidate with a URL and a filename.
    """
    url: str
    """The URL of the file."""
    name: str
    """The name of the file."""
    filename: str
    """The filename of the file."""

    def __init__(self, url: str, filename: str) -> None:
        """
        Constructor
        
        Initializes an instance of DownloadCandidate.

        Args:
            url (str): The URL of the file.
            filename (str): The name of the file.

        Returns:
            None
        """
        self.url = url
        self.name = filename
        self.filename = filename + ".pdf"

    @staticmethod    
    def make_candidate(line: str) -> "DownloadCandidate":
        """
        Create a DownloadCandidate object based on the given line.

        Args:
            line (str): The input line containing the name and URL separated by a comma.

        Returns:
            DownloadCandidate: The created DownloadCandidate object.

        Raises:
            None

        """
        # Initialize the candidate
        candite: DownloadCandidate = None
        # Initialize the Log Manager
        log = LogManager()
        try:
            # Remove the newline character
            line = line.strip()
            # Split the line
            name = line.split(",")[0]
            url = line.split(",")[1]
            # Check if the name and URL are not empty
            if name != "" and url != "":
                # Create the candidate
                candite = DownloadCandidate(url, name)
            else:
                log.print_err("Error line non parsed:\t" + line)
        except:
            log.print_err("Error line:\t" + line)
        # Return the candidate
        return candite
    
    def print_candidate(self) -> str:
            """
            Returns a string representation of the candidate's name and URL.
            It works for CSV format.

            Returns:
                A string in the format "<name>,<url>" representing the candidate's name and URL.
            """
            return self.name + "," + self.url

    def __str__(self) -> str:
        return "Name" + self.name + "Filename: " + self.filename + "\n" + "URL: " + self.url

class EUgolino(threading.Thread):
    """
    EUgolino is a class which allow to download PDF files from a list of URLs.

    It was specifically designed to download papers from the European Union DataBase.
    As the Conte Ugolino in Dante's Inferno, it is a greedy downloader.
    As Ugolino della Gherardesca eats from the head of his enemy, 
    EUgolino feeds himself with the knowledge of scientific papers.
    """
    file_in: str
    """Input file containing the list of URLs."""
    candidates: list[DownloadCandidate] = []
    """List of download candidates."""
    max_downloads: int = -1
    """Maximum number of downloads."""
    destination: str = "pdf/"
    """Destination folder for downloaded files."""
    current: DownloadCandidate = None
    """Current download candidate."""
    downloaded: int = 0
    """Number of downloaded files."""
    not_downloaded_files:str = "not_downloaded.txt"
    """File to store the list of files that were not downloaded."""
    output:LogManager = LogManager()

    def __init__(self, file_in: str, candidates: list[DownloadCandidate] = None, max_downloads: int = None, destination: str = None, not_downloaded_file: str = None, output: LogManager = None) -> None:
        """
        Initializes an instance of the EUgolino class.

        Args:
            file_in (str): The input file.
            candidates (list[DownloadCandidate], optional): List of download candidates. Defaults to None.
            max_downloads (int, optional): Maximum number of downloads. Defaults to None.
            destination (str, optional): Destination directory for downloaded files. Defaults to None.
            not_downloaded_file (str, optional): File to store the list of files that were not downloaded. Defaults to None.
            output (LogManager, optional): LogManager instance for logging. Defaults to None.
        """
        self.file_in = file_in
        if candidates is not None:
            self.candidates = candidates
        if max_downloads is not None:
            self.max_downloads = max_downloads
        if destination is not None:
            self.destination = destination
        if not_downloaded_file is not None:
            self.not_downloaded_files = not_downloaded_file
        if output is not None:
            self.output = output
        threading.Thread.__init__(self, name="EUgolino")

    def __str__(self) -> str:
        out = "Input file: " + self.file_in + "\n" + "Number of urls: " + str(self.candidates.__len__) + "\n" + "Destination folder: " + self.destination + "\n" + "Max downloads: " + str(self.max_downloads) + "\n" + "Downloaded: " + str(self.downloaded)
        if self.current is not None:
            out += "\n" + "Current\n" + self.current
        return out
    
    def import_file(self, file:str = None, candites: list[DownloadCandidate] = None) -> int:
        """
        Imports a file and processes its contents to create download candidates.

        Args:
            file (str, optional): The path of the file to import. Defaults to None.
            candites (list[DownloadCandidate], optional): The list of existing download candidates. Defaults to None.

        Returns:
            int: The number of errors encountered during the import process.
        """
        if file is not None:
            self.file_in = file
        if candites is not None:
            self.candidates = candites
        # Initialize the errors counter
        errors = 0
        # Initialize the candidate
        candite: DownloadCandidate = None
        try:
            # Open the file
            with open(self.file_in, 'r') as f:
                # Read the file line by line
                self.output.print_out("Importing file: " + self.file_in)
                # Process each line
                for line in f:
                    # Create a candidate
                    candite = DownloadCandidate.make_candidate(line)
                    # Check if the candidate is not None
                    if candite is not None:
                        # Add the candidate to the list
                        self.candidates.append(candite)
                    else:
                        errors += 1
            f.close()
            # ACK message
            self.output.print_out("File imported")
        except:
            self.output.print_err("Error: file\t" + self.file_in + "\tnot imported")
            errors = -1
        # If the current candidate is None, set it to the first candidate
        if self.candidates != [] and self.current is None:
            self.current = self.candidates[0]
        # Return the number of errors
        return errors
    
    def downloadPDF(self, candidate: DownloadCandidate = None, destination:str = None, not_downloaded_file = None) -> bool:
        """
        Downloads a PDF file from a given URL and saves it to the specified destination.

        Args:
            candidate (DownloadCandidate, optional): The download candidate object containing the URL and filename. If not provided, the current candidate will be used. Defaults to None.
            destination (str, optional): The destination directory where the PDF file will be saved. If not provided, the default destination will be used. Defaults to None.
            not_downloaded_file (str, optional): The file path to the log file where the details of the not downloaded files will be recorded. If not provided, the default log file will be used. Defaults to None.

        Returns:
            bool: True if the PDF file was successfully downloaded and saved, False otherwise.
        """
        if candidate is not None:
            self.current = candidate
        if destination is not None:  
            self.destination = destination
        if not_downloaded_file is not None:
            self.not_downloaded_files = not_downloaded_file
        full_path = self.destination + self.current.filename
        try:
            # Get the page
            dat = requests.get(url=self.current.url)
            # Get the cookies
            cookies = dat.cookies
            # Parse the page
            soup = BeautifulSoup(dat.text, 'html.parser')
            # Get the script tags
            link = soup.find_all("script")
            # Find the link to the pdf
            doc = ""
            # Search for the link
            for l in link:
                # Check if the script tag contains the link to the pdf
                if "window.location" in l.text:
                    # Split the script tag to get the link
                    s = l.text.split("\'")
                    # Get the link
                    doc = s[3]
            # Download the pdf
            dat = requests.get(url=doc, cookies=cookies)
            # Save the pdf
            with open(full_path, "wb") as f:
                f.write(dat.content)
            f.close()
            # Update the downloaded counter
            self.downloaded += 1
            # ACK message
            self.output.print_out("Downloaded\t" + full_path)
            return True
        except:
            self.output.print_err("Error\t" + full_path + "\tnot downloaded")
            try:
                # Save the not downloaded file
                with open(self.not_downloaded_files, "a") as f:
                    f.write(self.current.print_candidate() + "\n")
                f.close()
                # Update the input file
                self.file_in = self.not_downloaded_files
            except:
                self.output.print_err("Error\t" + self.not_downloaded_files + "\tnot updated")
            self.output.print_out("FAIL\t\t" + full_path)
            return False

    def download_all(self, candidates: list[DownloadCandidate] = None, destination:str = None, max_downloads:int = None, not_downloaded_files:str = None) -> int:
        """
        Downloads all the PDF files from the given list of download candidates.

        Args:
            candidates (list[DownloadCandidate], optional): List of DownloadCandidate objects representing the PDF files to download. If not provided, the previously set candidates will be used. Defaults to None.
            destination (str, optional): The destination folder where the downloaded PDF files will be saved. If not provided, the previously set destination will be used. Defaults to None.
            max_downloads (int, optional): The maximum number of PDF files to download. If not provided, all the candidates will be downloaded. Defaults to None.
            not_downloaded_files (str, optional): The file path to save the list of files that were not downloaded. If not provided, the previously set file path will be used. Defaults to None.

        Returns:
            int: The number of errors that occurred during the download process.
        """
        if candidates is not None:
            self.candidates = candidates
        if destination is not None:
            self.destination = destination
        if max_downloads is not None:   
            self.max_downloads = max_downloads
        if not_downloaded_files is not None:
            self.not_downloaded_files = not_downloaded_files

        # Initialize the errors counter
        errors = 0

        # Create the destination folder
        os.makedirs(self.destination, exist_ok=True)

        # Get the number of downloads
        num = self.candidates.__len__()

        # Check if the number of downloads is limited
        if self.max_downloads > 0:
            # Limit the number of downloads
            num = min(num, self.max_downloads)

        # Get the number of digits of the length
        fi = self.count_digits(num)

        # Download the PDFs
        for i in range(num):
            # Get the filename
            self.current = self.candidates.pop(0)

            # Print the progress
            self.output.print_out("[" + "{:{}}".format((i+1), fi) + '/' + str(num) + "]:", end="\t")

            # Download the PDF
            if not self.downloadPDF():
                # Update the errors counter
                errors += 1
                # Add the not downloaded file to the list of candidates
                self.candidates.append(self.current)

        return errors
    
    def do_all(self, file_in:str = None, destination:str = None, max_downloads:int = None, not_downloaded_files:str = None) -> int:
        """
        Performs all the necessary operations to import a file, download the PDFs, and returns the number of errors encountered.

        Args:
            file_in (str, optional): The input file path. Defaults to None.
            destination (str, optional): The destination folder path. Defaults to None.
            max_downloads (int, optional): The maximum number of PDFs to download. Defaults to None.
            not_downloaded_files (str, optional): The file path to store the list of not downloaded files. Defaults to None.

        Returns:
            int: The number of errors encountered during the process.
        """
        # Initialize the errors counter
        errors = 0
        if file_in is not None:
            self.file_in = file_in
        if destination is not None:
            self.destination = destination
        if max_downloads is not None:
            self.max_downloads = max_downloads
        if not_downloaded_files is not None:
            self.not_downloaded_files = not_downloaded_files
        # Initialize the lists
        errors += self.import_file()
        # Download the PDFs
        errors += self.download_all()
        # Return the number of errors
        return errors
    
    def run(self) -> None:
        """
        Executes the do_all method as thread.
        """
        self.do_all()

    @staticmethod
    def count_digits(n) -> int:
        """
        Count the number of digits in a given number.

        Args:
            n: The number to count the digits of.

        Returns:
            int: The number of digits in the given number.
        """
        ns = str(n)
        return len(ns)

