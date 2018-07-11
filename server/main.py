from flask import Flask, request
app = Flask(__name__)
# from printing import print_all

@app.route("/", methods=['POST'])
def print():
    card_id = request.values.get("card_id")
    readed_id = request.values.get("reader_id")
    # find user and printer in the database:
    # user_name = ...
    # server = ...
    # printer_name = ...
    # print_all(user_name, server, printer_name)
    # return "OK"
    pass

if __name__ == '__main__':
main()