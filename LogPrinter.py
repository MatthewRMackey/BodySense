import os
import logging
import traceback

class LogPrinter:
    def __init__(self):
        os.makedirs(self.get_path_root()+ "\\Errors", exist_ok=True)
        self.path = self.get_path_root() + "\\Errors\\errors.log"
    
    def log_output(self, error, data):
        logging.basicConfig(filename=self.path, level=logging.ERROR)
        logging.error(f'\nError processing list: {data}\nException: {error}\nTraceback: {traceback.format_exc()}\n\n')

    # Determine the root up to the current user's home directory (Windows only)
    def get_path_root(self):
        cwd = os.getcwd()
        slashes = 0
        index = 0
        root_path = ""
        while slashes < 3:
            root_path += cwd[index]
            if cwd[index] == "\\":
                slashes += 1
            index += 1
        return root_path + "BodySense"