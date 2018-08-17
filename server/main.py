from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

from flask import Flask, request

from db_printer_info import getPrinterInfo
from Printing import StartPrint

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route("/print/", methods=['POST'])
def nfc_reader_request_handling():
    '''
    This method gets json with card_id and reader_id
    and looks for the printer name in the database
    then it sends printing data (Printer name and Card id) to the printing module to start printing
    '''
    card_id = request.get_json()['card_id']
    reader_id = request.get_json()['reader_id']
    macPrinter = getPrinterInfo(reader_id)[0]

    logger.info("Card ID: %s; NFC Reader ID: %s; Printer Name: %s" % (card_id,reader_id,macPrinter))

    StartPrint(printer=macPrinter, path=r'C:\\docs_for_print\\' + card_id)
    return "OK"

if __name__ == '__main__':
    '''
    This method starts the server
    '''
    app.run(host= '0.0.0.0')