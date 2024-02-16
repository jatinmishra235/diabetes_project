import sys

def error_messege_detail(error_msg,error_detail):
    _, _, exc_tb = error_detail.exc_info()
 
    filename = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occured script name [{0}] line number [{1}] error message [{2}]".format(
        filename, exc_tb.tb_lineno, str(error_msg)
    )

    return error_message


class CustomException(Exception):
    def __init__(self, error_messege, error_detail):
        super().__init__(error_messege)

        self.error_message = error_messege_detail(
            error_messege, error_detail
        )

    def __str__(self):
        return self.error_message