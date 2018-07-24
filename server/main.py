from http.server import BaseHTTPServer
# import os
from flask import Flask, request
from db_printer_info import getPrinterInfo, getCardId
from Printing import StartPrint
app = Flask(__name__)

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 4600

class UserRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(s):
        '''
        This method handles post requests to the server from clients and sends back responsess:
            it gets: user that sent the file to print, the document he sent and the printing settings
            the method looks up card id of the user in the database and saves the document and its print settings
            the folder it saves into is named after card id of the user
            if the folder does not exist it creates a new folder
        '''
        if s.path == "/send_file/":
            s.send_response(200)
            s.send_header("Content-type", "application/ipp")
            s.end_headers()
            # content of the response:
            # s.wfile.write("")
            # here we need authentication (email and passw)
            # card_id = getCardId(email, passw)
            # pathname = r'C:\\docs_for_print\\' + card_id
            # if not os.path.exists(pathname):
            #     os.makedirs(pathname)
            # here we need to get the document and its print settings and save it all to two files

            # for research purposes:
            print(s.rfile())

        else:
            # error response
            pass

        

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
    StartPrint(printer=macPrinter, path=r'C:\\docs_for_print\\' + card_id)
    # should delete files after the printing is complete
    return "OK"

if __name__ == '__main__':
    '''
    This method starts both servers
    '''
    app.run(host= '0.0.0.0')
    
    # server_class = BaseHTTPServer.HTTPServer
    # httpd = server_class((HOST_NAME, PORT_NUMBER), UserRequestHandler)
    # print "Server Starts" % (HOST_NAME, PORT_NUMBER)
    # try:
    #     httpd.serve_forever()
    #     except KeyboardInterrupt:
    #         pass
    #     httpd.server_close()
    #     print "Server Stops" % (HOST_NAME, PORT_NUMBER)