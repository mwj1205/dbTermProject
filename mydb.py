import mysql.connector

connection = mysql.connector.connect(user='mwhan', password='wj0522',
                              host='192.168.56.101', port='4567',
                              database='CCG_db')
# 커서 생성
if connection.is_connected():
    cursor = connection.cursor()
# 새로운 유저 생성
def userinsert(name):
    add_user = ("INSERT INTO User "
                "(Username) "
                "VALUES (\'%s\')" %(name))
    cursor.execute(add_user)
    connection.commit()
# 유저 리스트 읽기
def userprint():
    userprint = "SELECT Username FROM User"
    cursor.execute(userprint)

    row = cursor.fetchall()
    return row
# 유저 삭제
def userdelete(user):
    deluser = "DELETE FROM User WHERE Username = '%s'" %(user)
    cursor.execute(deluser)
    connection.commit()

# 유저 정보 확인
def seled_user(field, user):
    myquery = "SELECT %s FROM User WHERE Username = '%s'" %(field, user)
    if user is not None:
        cursor.execute(myquery)
        row=cursor.fetchone()
        row = row[0]        
        return row
# 유저 재화 보유량 업데이트
def update_money(kind , num, uid):
    up_pyr = "UPDATE User SET %s = %s WHERE UID = %s" %(kind, num, uid)
    cursor.execute(up_pyr)
    connection.commit()
# 인벤토리 읽기
def read_inventory(uid):
    uinven = "SELECT Item_ID, Remaining FROM Owned_Item WHERE UID = %s" %(uid)
    cursor.execute(uinven)
    row=cursor.fetchall()
    return row
# 아이템 이름 읽기
def itemname(itemid):
    itname = "SELECT Item_name FROM Item_Info WHERE Item_ID = %s" %(itemid)
    cursor.execute(itname)
    row=cursor.fetchone()
    row = row[0]
    return row
# 아이템 설명 읽기
def itemdesc(itemid):
    itname = "SELECT Item_name, Item_desc FROM Item_Info WHERE Item_ID = %s" %(itemid)
    cursor.execute(itname)
    row=cursor.fetchone()
    return row
def gacha_char(stars):
    charcs = "SELECT Character_ID FROM Basic_Character WHERE Basic_star_quantity = %s" %(stars)
    cursor.execute(charcs)
    row=cursor.fetchall()
    charlist = []
    for i in row:
        char = i[0]
        charlist.append(char)
    return charlist

# 캐릭터 가챠
def get_charac(uid, charid):
    # 캐릭터가 이미 가지고 있는건지 체크
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
    # 캐릭터 등급에 따라 엘리그마 획득 개수가 달라짐
    if stars == 1:
        elamount = 1
    elif stars == 2:
        elamount = 5
    else:
        elamount =30

    if row == 0: # 캐릭터가 없었으면
        # 뽑은 캐릭터 삽입
        insertchar = "INSERT INTO Owned_Character (UID, Character_ID, Star_quantity)\
        VALUES(%s, %s, %s)" %(uid, charid, stars)
        cursor.execute(insertchar)
        connection.commit()
        
    else: # 캐릭터가 있었으면
        # 진화석 획득
        inserteligma = "INSERT INTO Owned_Item (UID, Item_ID, Remaining) VALUES(%s, %s, %s)\
                        ON DUPLICATE KEY UPDATE Remaining = Remaining + %s" %(uid, eligmaid, elamount, elamount)
        cursor.execute(inserteligma)
        connection.commit()

# 보유중인 캐릭터 수
def char_amount(UID):
    charamount = "SELECT COUNT(CASE WHEN UID = %s THEN 1 END) FROM Owned_Character" %(UID)
    cursor.execute(charamount)
    num = cursor.fetchone()
    return num

# 캐릭터 보유 목록 읽기
def read_charlist(UID):
    charlist = "SELECT Character_ID FROM Owned_Character WHERE UID = %s" %(UID)
    cursor.execute(charlist)
    row = cursor.fetchall()
    return row

# 캐릭터 이름 읽기
def charname(charid):
    cname = "SELECT Character_name FROM Basic_Character WHERE Character_ID = %s" %(charid)
    cursor.execute(cname)
    row = cursor.fetchone()
    row = row[0]
    return row

# 캐릭터 기본 정보 이름, 기본 등급
def getcharbasicinfo(charid):
    basicinfo = "SELECT Character_name, Basic_star_quantity FROM Basic_Character WHERE Character_ID = %s" %(charid)
    cursor.execute(basicinfo)
    row = cursor.fetchone()
    return row

def char_basicinfo(charname):
    charid = "SELECT * FROM Basic_Character WHERE Character_name = '%s'" %(charname)
    cursor.execute(charid)
    row = cursor.fetchone()
    return row

def nowcharinfo(uid, charid):
    owncharinfo = "SELECT Current_EXP, Star_quantity, Active_skill_level, Passive_skill_level, Equipment_tier, Equipment_level \
        FROM Owned_Character WHERE UID = %s AND Character_ID = %s" %(uid, charid)
    cursor.execute(owncharinfo)
    row = cursor.fetchone()
    return row

# 캐릭터 레벨에 따른 스탯 게산
def cal_char_stat_level(UID, charid):
    charinfo = "SELECT * FROM cinfo_view WHERE UID = %s AND Character_ID = %s" %(UID, charid)
    cursor.execute(charinfo)
    cinfo = cursor.fetchone()
    charcrit = "SELECT Basic_Crit, Basic_Crit_damage FROM Basic_Character WHERE Character_ID = %s" %(charid)
    cursor.execute(charcrit)
    crits = cursor.fetchone()
    # 0 UID 1 Character ID 2 Level 3 Basic ATK 4 Basic DEF 5 Basic MAX HP
    # 6 ATK rising # 7 DEF rising 8 MAX HP rising
    clevel = cinfo[2]
    batk = cinfo[3]
    bdef = cinfo[4]
    bhp = cinfo[5]
    ratk = cinfo[6]
    rdef = cinfo[7]
    rhp = cinfo[8]
    ATK = batk + (ratk * clevel)
    DEF = bdef + (rdef * clevel)
    HP = bhp + (rhp * clevel)
    cinfolist=[clevel, ATK, DEF, HP, crits[0], crits[1]]
    return cinfolist

# 장비에 따른 캐릭터 스텟 계산
def cal_char_equip(lvstat, etype, etier, elevel):
    equipstat = "SELECT * FROM einfo_view WHERE Equipment_type = %s AND Equipment_tier = %s" %(etype, etier)
    cursor.execute(equipstat)
    eqfigure = cursor.fetchone()

    stat1 = eqfigure[2]
    stat1_fig = (eqfigure[4] - eqfigure[3]) * (elevel / 30) + eqfigure[3]
    
    if eqfigure[6]:
        stat2 = eqfigure[5]
        stat2_fig = (eqfigure[7] - eqfigure[6]) * (elevel / 30) + eqfigure[6]
    else: 
        stat2 = None
        stat2_fig = None
    
    stats = [stat1, stat2]
    stats_fig = [stat1_fig, stat2_fig]

    ATKP = 0
    DEF = 0
    HPP = 0
    Crit = 0
    Crit_dam = 0

    for i in range(2):
        if stats_fig[i] == None:
            break
        elif stats[i] == "ATK%":
            ATKP += stats_fig[i]
        elif stats[i] == "Crit":
            Crit += stats_fig[i]
        elif stats[i] == "Crit_damage":
            Crit_dam += stats_fig[i]
        elif stats[i] == "Max_HP%":
            HPP += stats_fig[i]
        elif stats[i] == "DEF":
            DEF += stats_fig[i]

    Crit_dam /= 100

    lvstat[1] *= (1+ATKP)
    lvstat[2] += DEF
    lvstat[3] *= (1+HPP)
    lvstat[4] += Crit
    lvstat[5] += Crit_dam

    return lvstat

# 캐릭터의 exp를 update
def update_char_exp(uid, cid, exp):
    qry = "UPDATE Owned_Character SET Current_EXP = %s WHERE UID = %s AND Character_ID = %s" %(exp, uid, cid)
    cursor.execute(qry)
    connection.commit()
# 캐릭터의 여러 종류의 level update
def char_levelup(uid, cid, num, kind):
    uplevel = "UPDATE Owned_Character SET %s = %s WHERE UID = %s AND Character_ID = %s" %(kind, num, uid, cid)
    cursor.execute(uplevel)
    connection.commit()
# 골드가 충분한가 체크
def check_needgold(uid, num):
    checkgold = "SELECT EXISTS (SELECT Gold FROM User WHERE UID = %s AND GOLD >= %s) as success" %(uid, num)
    cursor.execute(checkgold)
    cgold = cursor.fetchone()
    cgold = cgold[0]
    return cgold
# 진화석이 충분한가 체크
def check_needeligma(uid, cid, num):
    checkeligma = "SELECT EXISTS (SELECT Remaining FROM Owned_Item WHERE UID = %s AND Remaining >= %s AND Item_ID = (\
        SELECT Eligma_id FROM Basic_Character WHERE Character_ID = %s)) as success" %(uid, num, cid)
    cursor.execute(checkeligma)
    celigma = cursor.fetchone()
    celigma = celigma[0]
    return celigma

# 진화석 사용
def patcheligma(uid, cid, num):
    useeligma = "UPDATE Owned_Item SET Remaining = Remaining - %s WHERE UID = %s AND Item_ID = \
        (SELECT eligma_id FROM Basic_Character WHERE Character_ID = %s)" %(num, uid, cid)
    cursor.execute(useeligma)
    connection.commit()

# 스킬 강화 재료가 충분한가 확인
def check_skil_item(uid, itemid, num):
    myqry = "SELECT EXISTS \
        (SELECT Remaining FROM Owned_Item WHERE UID = %s AND Remaining >= %s AND Item_ID = %s) as success" \
            %(uid, num, itemid)
    cursor.execute(myqry)
    skillm = cursor.fetchone()
    skillm = skillm[0]
    return skillm

# 아이템 수량 업데이트
def patch_items(uid, itemid, num):
    myqry = "UPDATE Owned_Item SET Remaining = Remaining - %s WHERE UID = %s AND Item_ID = %s"\
         %(num, uid, itemid)
    cursor.execute(myqry)
    connection.commit()

def patch_items_get(uid, itemid, num):
    myqry = "INSERT INTO Owned_Item (UID, Item_ID, Remaining) VALUES(%s, %s, %s)\
                ON DUPLICATE KEY UPDATE Remaining = Remaining + %s" %(uid, itemid, num, num)
    cursor.execute(myqry)
    connection.commit()
