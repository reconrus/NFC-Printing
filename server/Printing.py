import win32print, win32ui, win32gui
import win32con, pywintypes


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
             filename=r'D:\test.txt',
             copies = 1,
            orientation = win32con.DMORIENT_PORTRAIT,
            duplex = win32con.DMDUP_HORIZONTAL,
            printQuality = win32con.DMRES_HIGH,
            color = win32con.DMCOLOR_MONOCHROME,
            paperSize = win32con.DMPAPER_LETTER,  # or DMPAPER_A4
             text=None):
    if text is None:
        f = open(filename, "rb")
        buffer_size = 100000
        text_data = f.read(buffer_size)
    else:
        text_data = text
    job_info = ("Raw File Print", filename, 'RAW')
    h_printer = win32print.OpenPrinter(printer)
    devmode = win32print.GetPrinter(h_printer, 2)['pDevMode']
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

    h_dc = win32gui.CreateDC('WINSPOOL', printer, devmode)
    dc = win32ui.CreateDCFromHandle(h_dc)
    try:
        dc.StartDoc('Postscript File Print', filename)
        try:
            dc.StartPage()
            dc.EndPage()
        finally:
            dc.EndDoc()
    finally:
        win32print.ClosePrinter(h_printer)
StartPrint('Microsoft XPS Document Writer', 'D:\Text.pdf' )
