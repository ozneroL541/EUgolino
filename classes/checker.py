#!/bin/python3
'''
    EUgolino Checker
    file name: checker.py
    author: Lorenzo Radice
'''

import os
import threading
import requests

class Checker(threading.Thread):
    """
    A class that represents a checker for monitoring a directory.
    """
    
    name:str = "Checker"
    """Name of the Checker."""
    directory:str = 'pdf/'
    """Directory to monitor."""
    sleep_time:int = 10
    """Sleep time between checks."""
    check_URL:str = None
    """URL to send the check."""
    send_check:bool = False
    """Flag indicating whether to send the check."""
    previous_len:int = 0
    """Previous number of files in the directory."""    
    current_len:int = 0
    """Current number of files in the directory."""
    max_len:int = 0
    """Maximum number of files in the directory."""
    halt:bool = False
    """Flag indicating whether to stop the checker."""
    e:threading.Event = threading.Event()
    """Event for waiting."""

    def __init__(self, name:str = "Checker", directory:str = "pdf/", sleep_time:int = 10, check_URL:str = None, send_check:bool = False, max_len:int = 0) -> None:
        """
        Costructor
        
        Initializes a new instace of the Checker class.

        Args:
            name (str, optional): Name of the Checker. Defaults to "Checker".
            directory (str, optional): Directory to monitor. Defaults to "pdf/".
            sleep_time (int, optional): Sleep time between checks. Defaults to 10.
            check_URL (str, optional): URL to send the check. Defaults to None.
            send_check (bool, optional): Flag indicating whether to send the check. Defaults to False.
            max_len (int, optional): Maximum number of files in the directory. Defaults to 0.
        """
        self.name = name
        self.directory = directory
        self.sleep_time = sleep_time
        self.check_URL = check_URL
        if check_URL is None:    
            self.send_check = False
        else:
            self.send_check = send_check
        self.max_len = max_len
        threading.Thread.__init__(self, name=name)
    
    def __str__(self) -> str:
        """
        String representation of the Checker.

        Returns:
            str: String representation of the Checker.
        """
        return "Name:\t" + self.name + "\nDirectory:\t" + self.directory + "\nSleep Time:\t" + str(self.sleep_time) + "\nCheck URL:\t" + str(self.check_URL) + "\nSend Check:\t" + str(self.send_check) + "\nMax Length:\t" + str(self.max_len)
    
    def stop(self) -> None:
        """
        Stop the checker.
        """
        self.halt = True
        self.e.set()

    def update_current_len(self) -> None:
        """
        Update the current length of the directory.
        """
        try:
            # Update the current length
            self.current_len = len(os.listdir(self.directory))
        except:
            self.current_len = 0
            self.previous_len = 0
        
    def get_progress(self) -> str:
        """
        Returns the progress of the checker as a string.

        If the maximum length is not set, the progress is represented as the current length.
        If the maximum length is set, the progress is represented as a formatted string with the current length and the maximum length.

        Returns:
            str: The progress of the checker.
        """
        # If max length is not set
        if self.max_len == 0:
            # Make progress as current length
            return str(self.current_len)
        else:
            # Make progress
            return "[" + "{:{}}".format((self.current_len), len(str(self.max_len))) + '/' + str(self.max_len) + "]"
    
    def send_success(self, success:bool = None, URL:str = None, send:bool = True) -> None:
        """
        Send the check to the specified URL.

        Args:
            success (bool, optional): Flag indicating whether the check was successful. Defaults to None.
            URL (str, optional): URL to send the check. Defaults to None.
            send (bool, optional): Flag indicating whether to send the check. Defaults to True.
        
        Returns:
            None
        """
        if URL is None:
            URL = self.check_URL
            if URL is None:
                send = False
            elif send is None:
                send = self.send_check
        # If check is required send it
        if send:
            # Make data
            dat = "Name:\t" + self.name + "\n\n" + self.get_progress()
            # Send the check with current length
            requests.post(url=(URL if success else URL + "/fail"), data=dat)
    
    def is_len_increased(self, URL:str = None, send:bool = None) -> bool:
        """
        Checks if the number of files in the directory has increased.

        Args:
            URL (str, optional): The URL to check. If not provided, the default URL will be used.
            send (bool, optional): Indicates whether to send the check. If not provided, the default value will be used.

        Returns:
            bool: True if the length of the directory has increased, False otherwise.
        """
        if URL is None:
            URL = self.check_URL
            if URL is None:
                send = False
            elif send is None:
                send = self.send_check
        else:
            send = True

        # Assume that the check is not successful
        success = False

        # Check if the length of the directory has increased
        if self.current_len > self.previous_len:
            # Update the previous length
            self.previous_len = self.current_len
            # Success
            success = True

        self.send_success(success, URL, send)
        return success

    def check_len(self, URL:str = None, send:bool = None) -> bool:
        """
        Update the current lenght and check if it is increased.

        Args:
            URL (str, optional): The URL to send the check. Defaults to None.
            send (bool, optional): Indicates whether to send the check or not. Defaults to None.

        Returns:
            bool: True if the number is increased, False otherwise.
        """
        if URL is None:
            URL = self.check_URL
            if URL is None:
                send = False
            elif send is None:
                send = self.send_check
        else:
            send = True

        # Update current length
        self.update_current_len()

        # Return the result of the check
        return self.is_len_increased(URL=URL, send=send)

    def check_timed(self, sleep_time:int = None, URL:str = None, send:bool = None) -> bool:
        """
        Make a check after waiting a sleep time.

        Args:
            sleep_time (int, optional): The time to sleep before checking. If not provided, the default sleep time from the class instance will be used.
            URL (str, optional): The URL to check. If not provided, the default URL from the class instance will be used.
            send (bool, optional): Indicates whether to send the check. If not provided, the default send value from the class instance will be used.

        Returns:
            bool: Result of the check.
        """
        if URL is None:
            URL = self.check_URL
            if URL is None:
                send = False
            elif send is None:
                send = self.send_check
        else:
            send = True
        if sleep_time is None:
            sleep_time = self.sleep_time
        # Sleep for the specified time
        try:
            self.e.wait(sleep_time)
        except:
            pass
        # Check the length
        return self.check_len(URL=URL, send=send)

    def continuous_check(self, sleep_time:int = None, URL:str = None, send:bool = None) -> None:
        """
        Continuously performs checks at regular intervals.

        Args:
            sleep_time (int, optional): The time to sleep between each check in seconds. If not provided, the default sleep time will be used.
            URL (str, optional): The URL to send the check request to. If not provided, the default check URL will be used.
            send (bool, optional): Whether to send the check request. If not provided, the default send option will be used.

        Returns:
            None
        """
        if URL is None:
            URL = self.check_URL
            if URL is None:
                send = False
            elif send is None:
                send = self.send_check
        else:
            send = True
        if sleep_time is None:
            sleep_time = self.sleep_time
        # Send the starting check
        if send:
            self.send_start(URL)
        # Forever
        while not self.halt:
            # Check
            self.check_timed(sleep_time=sleep_time,URL=URL, send=send)
        # Reset the stop flag
        self.halt = False
        # Send the ending check
        if send:
            # Update the current length
            self.update_current_len()
            # Send the done message
            self.send_generic(URL=URL, data="\n\nDONE\n\n" + self.get_progress())

    def send_start(self, URL) -> None:
        """
        Send the starting check.
        
        Args:
            URL (str): The URL to send the starting check to.
        
        Returns:
            None
        """
        requests.post(url=URL+"/start", data=str("Name:\t" + self.name))

    def send_generic(self, URL:str = None, data:str = None, sleep_time:int = None) -> None:
        """
        Send a message to the specified URL.

        Args:
            URL (str, optional): The URL to send the done message to. If not provided, the default URL will be used.
            data (str, optional): The data to send with the done message. Defaults to None.

        Returns:
            None
        """
        if URL is None:
            URL = self.check_URL
            if URL is None:
                return
        if sleep_time is None:
            sleep_time = self.sleep_time
        # Update data
        data = "Name:\t" + self.name + "\n\n" + data
        # Send the done message
        requests.post(url=URL, data=data, timeout=10)

    def run(self) -> None:
        """
        Run the checker.
        """
        self.continuous_check()
        return

