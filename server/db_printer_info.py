import pyodbc


def connection():
    driver = 'DRIVER={SQL Server}'
    server = 'SERVER=PROJECTPRINT01'
    db = 'DATABASE=test_skip_card'
    user = 'UID=user'
    pwd = 'PWD=kQzYxVJMt8l5O8P51r0YdHHc'

    conn_str = ';'.join([driver, server, db, user, pwd])

    #Подключение по данным к бд
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return cursor

#Основной метод
def getPrinterInfo(idChip):

    #Забираем указатель
    cursor = connection()

    #Чип, с которого пришёл запрос
    #idChip = 1

    #SQL запрос, который будет исполняться
    sql = 'SELECT macPrinter, ipPrinter FROM printers WHERE idChip='+str(idChip)

    #Исполняем
    cursor.execute(sql)
    results = cursor.fetchall()

    #Достаём mac и ip принтера, который нам нужен
    macPrinter = results[0][0]
    ipPrinter = results[0][1]

    return macPrinter, ipPrinter



