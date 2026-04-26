import sys

class CustomException(Exception):
    def __init__(self, message, error_detail: Exception=None):
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(message, error_detail):
        _,_, exe_tb  = sys.exc_info()
        if exe_tb:
            line_number = exe_tb.tb_lineno
            file_name = exe_tb.tb_frame.f_code.co_filename
        else:
            line_number = None
            file_name = None

        return (
            f"{message} | "
            f"Error Detail:{error_detail} | "
            f"File Name: {file_name} | "
            f"Line Number: {line_number}" 
        )
    

    def __str__(self):
        return self.error_message