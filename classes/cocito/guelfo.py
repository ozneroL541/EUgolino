#!/bin/python3
'''
    GEUlfo
    file name: guelfo.py
    author: Lorenzo Radice
    license: European Union Public Licence v. 1.2.
'''

import requests
from classes.cocito.eugolino import *

class GUElfo(EUgolino):
    """
    GUElfo is a class which allow to download PDF files from a list of URLs.
    """
    destination: str = "pdf_guelfo/"
    """Destination folder for downloaded files."""
    not_downloaded_files:str = "not_downloaded_guelfo.txt"
    """File to store the list of files that were not downloaded."""
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
            # Download the pdf
            dat = requests.get(url=self.current.url)
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
