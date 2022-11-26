import mysql.connector

connection = mysql.connector.connect(user='mwhan', password='wj0522',
                              host='192.168.56.101', port='4567',
                              database='CCG_db')

if connection.is_connected():
    # 커서 생성
    cursor = connection.cursor()

def userinsert(name):
    add_user = ("INSERT INTO User "
                "(Username) "
                "VALUES (\'%s\')" %(name))

    cursor.execute(add_user)

def userprint():
    userprint = "SELECT * FROM User"
    cursor.execute(userprint)

    row = cursor.fetchone()
    while row is not None:
        print("show data")
        print(row)
        row = cursor.fetchone()
    print()

