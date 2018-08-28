import win32print, win32ui, win32gui, win32api, win32event
import win32con, pywintypes
import os, time

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
    win32print.SetDefaultPrinter(printer)

    try:
        listOfFiles = os.listdir(path)
        if (len(listOfFiles)!=0):
            for file in listOfFiles:
                filename = path+'\\'+file
                print(filename)
                print(win32api.ShellExecute(
                   0,
                   "printto",
                   filename,
                   '"%s"' % win32print.GetDefaultPrinter(),
                   ".",
                   0
                ))
            listOfFiles = os.listdir(path)
            print_jobs = win32print.EnumJobs(h_printer, 0, -1, 2)
            delete = True
            while (delete):
                old_print_jobs = print_jobs
                print_jobs = win32print.EnumJobs(h_printer, 0, -1, 2)
                if((len(print_jobs) == 0) & (len(old_print_jobs)!=0)):
                    print('ok')
                    delete = False
                    for file in listOfFiles:
                        filename = path+'\\'+file
                        os.remove(filename)
    except FileNotFoundError:
        print('Directory not created.')
