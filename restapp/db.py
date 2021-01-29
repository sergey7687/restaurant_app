import mysql.connector

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Lindab123",
    database='restaurant'
)
# curs = my_db.cursor()
# curs.execute('show tables')
#
# res = curs.fetchall()
# for i in res:
#     print(i)


def decorator(func):
    def wrapper(arg):
        print('hello')
        value = func(arg)
        value = value[0].upper()
        return value
    return wrapper


@decorator
def fetchdb(com):
    curs = my_db.cursor()
    comm = curs.execute(com)
    res = curs.fetchone()
    return res



print(fetchdb('show tables'))

# @decorator
# def fetchdb_2(com):
#
#     return com
#
# print(fetchdb_2('show tables:'))