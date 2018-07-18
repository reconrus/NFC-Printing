import win32print, win32ui, win32gui, win32api
import win32con, pywintypes
import os


def install_printer (printer_name='MyPSPrinter'):
    printer_info = {
        'pPrinterName': printer_name,
        'pDevMode': pywintypes.DEVMODEType(),
        'pDriverName': 'MS Publisher Imagesetter',
        'pPortName': 'FILE:',
        'pPrintProcessor': 'WinPrint',
        'Attributes': 0,
        'AveragePPM': 0,
        'cJobs': 0,
        'DefaultPriority': 0,
        'Priority': 0,
        'StartTime': 0,
        'Status': 0,
        'UntilTime': 0,
        'pComment': '',
        'pLocation': '',
        'pDatatype': None,
        'pParameters': None,
        'pSecurityDescriptor': None,
        'pSepFile': None,
        'pServerName': None,
        'pShareName': None}

    h_printer = win32print.AddPrinter(None, 2, printer_info)
    return h_printer

def uninstall_printer (printer_name='MyPSPrinter'):
    printer_info = {
        'pPrinterName': printer_name,
        'pDevMode': pywintypes.DEVMODEType(),
        'pDriverName': 'Test Driver',
        'pPortName': 'FILE:',
        'pPrintProcessor': 'WinPrint',
        'Attributes': 0,
        'AveragePPM': 0,
        'cJobs': 0,
        'DefaultPriority': 0,
        'Priority': 0,
        'StartTime': 0,
        'Status': 0,
        'UntilTime': 0,
        'pComment': '',
        'pLocation': '',
        'pDatatype': None,
        'pParameters': None,
        'pSecurityDescriptor': None,
        'pSepFile': None,
        'pServerName': None,
        'pShareName': None}

    del_printer = win32print.DeletePrinter(printer_info)
    return del_printer

def StartPrint (printer='MyPSPrinter',
             path=r'D:\test.txt',
             copies = 1,
            orientation = win32con.DMORIENT_PORTRAIT,
            duplex = win32con.DMDUP_HORIZONTAL,
            printQuality = win32con.DMRES_HIGH,
            color = win32con.DMCOLOR_MONOCHROME,
            paperSize = win32con.DMPAPER_LETTER,  # or DMPAPER_A4
             text=None):
    PRINTER_DEFAULTS = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
    h_printer = win32print.OpenPrinter(printer, PRINTER_DEFAULTS)
    properties = win32print.GetPrinter(h_printer, 2)
    devmode = properties["pDevMode"]
    devmode.FormName = 'Letter'  # or 'A4'
    devmode.PaperSize = paperSize
    devmode.Orientation = orientation
    devmode.PrintQuality = printQuality
    devmode.Color = color
    devmode.TTOption = win32con.DMTT_SUBDEV
    devmode.Scale = 100
    devmode.Copies = copies
    devmode.Duplex =duplex
    devmode.Fields |= (win32con.DM_FORMNAME |
                       win32con.DM_PAPERSIZE |
                       win32con.DM_ORIENTATION |
                       win32con.DM_PRINTQUALITY |
                       win32con.DM_COLOR |
                       win32con.DM_TTOPTION |
                       win32con.DM_SCALE)
    properties['pDevMode'] =devmode
    win32print.SetPrinter(h_printer, 2, properties, 0)
    listOfFiles = os.listdir(path)

    for file in listOfFiles:
        filename = path+'\\'+file
        print(filename)
        print(win32api.ShellExecute(
           0,
           "print",
           filename,
           '"%s"' % win32print.GetPrinter(h_printer, 2),
           ".",
           0
        ))


StartPrint('Samsung M337x 387x 407x Series', 'D:\Text' )
