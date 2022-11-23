import mysql.connector

connection = mysql.connector.connect(user='mwhan', password='wj0522',
                              host='192.168.56.101', port='4567',
                              database='madang')

if connection.is_connected():
    db_info = connection.get_server_info()
    print('mysql Version : ', db_info)  
    print()
    
    # 커서 생성
    cursor = connection.cursor()

    # Book table에 데이터 삽입
    add_Book = ("INSERT INTO Book "
               "(bookid, bookname, publisher, price) "
               "VALUES (%s, %s, %s, %s)")

    data_Book = ('101','파이썬기초', '충북출판사', '13000')
    cursor.execute(add_Book, data_Book)
    
    # Book talbe의 bookid가 101인 데이터 출력
    cursor.execute("SELECT * FROM Book")

    # 차례차례 가져와서 터미널에 출력
    row = cursor.fetchone()
    while row is not None:
        print("show data")
        print(row)
        row = cursor.fetchone()
    print()

    # 삽입한 데이터 삭제
    delete_Book = ("DELETE FROM Book "
               "WHERE bookid = '101'")
    
    cursor.execute(delete_Book)
    print("Delete Book id = 101")
    print()

    # Book talbe의 bookid가 101인 데이터 출력
    cursor.execute("SELECT * FROM Book WHERE bookid = '101'")

    # 차례차례 가져와서 터미널에 출력
    row = cursor.fetchone()
    print("show data")
    while row is not None:
        print(row)
        row = cursor.fetchone()
    print()

cursor.close()
connection.close()
print('MySQL Connection Close')