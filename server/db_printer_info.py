import pyodbc


def connection():
    driver = 'DRIVER={SQL Server}'
    server = 'SERVER=PROJECTPRINT01'
    db = 'DATABASE=test_skip_card'
    user = 'UID=user'
    pwd = 'PWD=kQzYxVJMt8l5O8P51r0YdHHc'

    conn_str = ';'.join([driver, server, db, user, pwd])

    # Connection to DB
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return cursor

# Main methid
def getPrinterInfo(idChip):

    cursor = connection()

    # SQL request that will be executed
    sql = 'SELECT macPrinter, ipPrinter FROM printers WHERE idChip=?'

    # Execution
    cursor.execute(sql, idChip)
    results = cursor.fetchall()

    # Getting MAC address of the printer that we need
    macPrinter = results[0][0]
    ipPrinter = results[0][1]

    return macPrinter, ipPrinter

