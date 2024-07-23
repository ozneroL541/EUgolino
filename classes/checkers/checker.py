#!/bin/python3
'''
    EUgolino Abstract Checker
    file name: checker.py
    author: Lorenzo Radice
    license: European Union Public Licence v. 1.2.
'''

from abc import ABC, abstractmethod
import threading
import requests


class Checker(ABC, threading.Thread):
    """
    Abstract class for checkers
    """

    name:str = "Checker"
    """Name of the checker"""
    sleep_time:int = 10
    """Time to wait before checking again"""
    url:str = None
    """URL to send the check"""
    send_check:bool = False
    """Flag indicating if the check should be sent"""
    halt:bool = False
    """Flag indicating if the checker should stop"""
    e:threading.Event = threading.Event()
    """Event for waiting"""

    def __init__(self, name:str = "Checker", sleep_time:int = 10, url:str = None, send_check:bool = False):
        """
        Constructor

        Initializes a new instance of the Checker class.

        Args:
            name (str, optional): Name of the checker. Defaults to "Checker".
            sleep_time (int, optional): Time to wait before checking again. Defaults to 10.
            url (str, optional): URL to send the check. Defaults to None.
            send_check (bool, optional): Flag indicating if the check should be sent. Defaults to False
        """
        self.name = name
        self.sleep_time = sleep_time
        self.url = url
        if url is None:    
            self.send_check = False
        else:
            self.send_check = send_check
        threading.Thread.__init__(self, name=name)
    
    def __str__(self) -> str:
        """
        String representation of the Checker.

        Returns:
            str: String representation of the Checker.
        """
        return "Name:\t" + self.name + "\nSleep time:\t" + str(self.sleep_time) + "\nCheck URL:\t" + str(self.url) + "\nSend check:\t" + str(self.send_check)
    
    def stop(self) -> None:
        """
        Stop the checker
        """
        self.halt = True
        self.e.set()
    
    def send(self, success:bool = True, data:str = "", url:str="") -> bool:
        """
        Send the check to the specified URL.

        Args:
            success (bool, optional): Flag indicating whether the check was successful. Defaults to None.
            data (str, optional): Data to send with the check. Defaults to "".
            url (str, optional): URL to send the check to. Defaults to "".

        Returns:
            bool: True if the check was sent, False otherwise.
        """
        if self.url is None and url == "":
            return
        if url == "":
            url = self.url
        # Make url
        url = url if success else url + "/fail"
        # If data is not set
        if data == "":
            # Make data
            data = "Name:\t" + self.name + "\n\n" + self.get_progresses()
        # Send the check with current length
        r = requests.post(url=url, data=data)
        # Return the result
        return r.ok
    
    def send_start(self) -> bool:
        """
        Send the starting check.
        
        Returns:
            bool: True if the check was sent, False otherwise
        """
        return requests.post(url=self.url+"/start", data=str("Name:\t" + self.name)).ok

    def send_done(self) -> bool:
        """
        Send the done check.
        
        Returns:
            bool: True if the check was sent, False otherwise
        """
        # Make data
        data = str("Name:\t" + self.name + "\n\nDONE\n\n" + self.get_progresses())
        # Send the message
        r = requests.post(url=self.url, data=data, timeout=10)
        # Return the result
        return r.ok

    @abstractmethod
    def check(self) -> bool:
        """
        Check the service
        
        Returns:
            bool: True if the service is up, False otherwise
        """
        pass

    @abstractmethod
    def get_progresses(self) -> str:
        """
        Get the progresses of the service
        
        Returns:
            dict: Dictionary containing the progresses of the service
        """
        return ""
    
    def timed_check(self, sleep_time:int = None, url:str = None, send:bool = None) -> bool:
        """
        Make a check after waiting a sleep time.

        Args:
            sleep_time (int, optional): The time to sleep before checking. If not provided, the default sleep time from the class instance will be used.
            url (str, optional): The URL to check. If not provided, the default URL from the class instance will be used.
            send (bool, optional): Indicates whether to send the check. If not provided, the default send value from the class instance will be used.

        Returns:
            bool: Result of the check.
        """
        if url is None:
            url = self.url
            if url is None:
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
        return self.check()

    
    def continuous_check(self, sleep_time:int = None, url:str = None, send:bool = None) -> None:
        """
        Continuously performs checks at regular intervals.

        Args:
            sleep_time (int, optional): The time to sleep between each check in seconds. If not provided, the default sleep time will be used.
            url (str, optional): The URL to send the check request to. If not provided, the default check URL will be used.
            send (bool, optional): Whether to send the check request. If not provided, the default send option will be used.

        Returns:
            None
        """
        if url is None:
            url = self.url
            if url is None:
                send = False
            elif send is None:
                send = self.send_check
        else:
            send = True
        if sleep_time is None:
            sleep_time = self.sleep_time
        # Send the starting check
        if send:
            self.send_start()
        # Forever
        while not self.halt:
            # Check
            self.timed_check(sleep_time=sleep_time,url=url, send=send)
        # Reset the stop flag
        self.halt = False
        # Send the ending check
        if send:
            # Send the done message
            self.send_done()
    
    def run(self) -> None:
        """
        Run the checker
        """
        self.continuous_check()
        return
