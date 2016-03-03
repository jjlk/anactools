import sys
import os


"""
Static class for utilities (warning, info, etc.)
"""
class Utilities(object):

    @staticmethod
    def warning(string):
        """
        Print warning
        Parameters
        ----------
        string: string to be printed
        """
        WARNINGCOLOR = "\033[31;01m"
        RESETCOLOR = "\033[0m"
        print(WARNINGCOLOR + "WARNING> " + RESETCOLOR + string)
        sys.stdout.flush()

    @staticmethod
    def info(string):
        """
        Print warning
        Parameters
        ----------
        string: string to be printed
        """
        INFOCOLOR = "\033[32;01m"
        RESETCOLOR = "\033[0m"
        print(INFOCOLOR + "INFO> " + RESETCOLOR + string)
        sys.stdout.flush()

