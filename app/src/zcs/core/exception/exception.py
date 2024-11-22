import random
import string
import traceback

class ZcsException(Exception):

    def __init__(self, user_message = "Unknown error.", error_source = "Unspecified", status_code = 500, internal_message = None):
        super().__init__(user_message)
        
        self.__error_source = error_source
        self.__status_code = status_code
        self.__user_message = user_message
        self.__internal_message = internal_message
        self.__error_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def get_status_code(self):
        return self.__status_code
    
    def get_error_source(self):
        return self.__error_source
    
    def get_user_message(self):
        return self.__user_message
    
    def get_internal_message(self):
        return self.__internal_message
    
    def get_error_code(self):
        return self.__error_code

    def get_as_dict(self):
        return {
            'error_code': self.get_error_code(),
            'user_message': self.get_user_message(),
            'internal_message': self.get_internal_message(),
            'error_source': self.get_error_source(),
            'status_code': self.get_status_code(),
            'traceback': "".join(traceback.format_exception(self))
        }
    
    def __str__(self):
        return f"{self.get_error_code()} - {self.get_error_source()} - {self.get_internal_message()} - {self.get_user_message()}"