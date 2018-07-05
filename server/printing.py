import win32api
import win32print
GHOSTSCRIPT_PATH = "C:\\Program Files\\GHOSTSCRIPT\\bin\\gswin32.exe"
GSPRINT_PATH = "C:\\Program Files\\GSPRINT\\gsprint.exe"
DOCS_PATH = "C:\\docs_for_print\\"

def print_all(user_name, server, printer_name):
    # send all files to the right printer one by one using a loop:
    # file_name = ...
    win32api.ShellExecute(
        0,
        'open',
        GSPRINT_PATH,
        '-ghostscript "'+ GHOSTSCRIPT_PATH +'" -printer "\\\\'+ server +'\\'+ printer_name +'" ' 
        + file_name, 
        '.',
        0
        )
    pass