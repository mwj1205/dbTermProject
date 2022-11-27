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
    userprint = "SELECT Username FROM User"
    cursor.execute(userprint)

    row = cursor.fetchall()
    return row

def userdelete(user):
    deluser = "DELETE FROM User WHERE Username = '%s'" %(user)
    cursor.execute(deluser)
    print(deluser)

    userprint = "SELECT Username FROM User"
    cursor.execute(userprint)

    row = cursor.fetchall()
    print(row)

def seled_user(field, user):
    myquery = "SELECT %s FROM User WHERE Username = '%s'" %(field, user)
    if user is not None:
        cursor.execute(myquery)
        row=cursor.fetchone()
        row = row[0]        
        return row

def update_pyroxene(pyroxene, uid):
    up_pyr = "UPDATE User SET Pyroxene = %s WHERE UID = %s" %(pyroxene, uid)
    cursor.execute(up_pyr)

def read_inventory(uid):
    uinven = "SELECT Item_ID, Remaining FROM Owned_Item WHERE UID = %s" %(uid)
    cursor.execute(uinven)
    row=cursor.fetchall()
    return row

def itemname(itemid):
    itname = "SELECT Item_name FROM Item_Info WHERE Item_ID = %s" %(itemid)
    cursor.execute(itname)
    row=cursor.fetchone()
    row = row[0]
    return row

def itemdesc(itemid):
    itname = "SELECT Item_name, Item_desc FROM Item_Info WHERE Item_ID = %s" %(itemid)
    cursor.execute(itname)
    row=cursor.fetchone()
    return row

def get_charac(uid, charid):
    isexist = "SELECT EXISTS (SELECT UID, Character_ID FROM Owned_Character \
    WHERE UID=%s AND Character_ID = %s ) as success" %(uid, charid)
    cursor.execute(isexist)
    row=cursor.fetchone()
    row = row[0]

    # 뽑은 캐릭터 기본 등급 확인
    charstar = "SELECT Basic_star_quantity, Eligma_id FROM Basic_Character WHERE Character_ID = %s" %(charid)
    cursor.execute(charstar)
    rows=cursor.fetchone()
    stars = rows[0]
    eligmaid = rows[1]
    if stars == 1:
        elamount = 1
    elif stars == 2:
        elamount = 5
    else:
        elamount =30

    if row == 0:
        # 뽑은 캐릭터 삽입
        insertchar = "INSERT INTO Owned_Character (UID, Character_ID, Star_quantity)\
        VALUES(%s, %s, %s)" %(uid, charid, stars)
        cursor.execute(insertchar)
        
    else:
        # 진화석 획득
        inserteligma = "INSERT INTO Owned_Item (UID, Item_ID, Remaining) VALUES(%s, %s, %s)\
                        ON DUPLICATE KEY UPDATE Remaining = Remaining + %s" %(uid, eligmaid, elamount, elamount)
        cursor.execute(inserteligma)

def getcharbasicinfo(charid):
    basicinfo = "SELECT Character_name, Basic_star_quantity FROM Basic_Character WHERE Character_ID = %s" %(charid)
    cursor.execute(basicinfo)
    row = cursor.fetchone()
    return row
