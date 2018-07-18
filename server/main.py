from flask import Flask, request
from db_printer_info import getPrinterInfo
app = Flask(__name__)

# gets the data from nfc reader and the database, sends it to the printing service
@app.route("/", methods=['POST'])
def index():
    card_id = request.get_json()['card_id']
    reader_id = request.get_json()['reader_id']
    # find printer in the database:
    macPrinter = getPrinterInfo[0]
    return "OK"

if __name__ == '__main__':
    app.run(host= '0.0.0.0')