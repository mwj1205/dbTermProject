from tkinter import *
import mydb as db
import gacha as gc

root = Tk()
root.title("Blue Archive")
root.geometry("640x280")

#서브 프레임 생성
frame_user_select = Frame(root)
frame_user = Frame(root)
frame_inventory = Frame(root)
frame_gacha = Frame(root)
frame_gacha_got_char = Frame(root)
frame_charac_list = Frame(root)
frame_charac_info = Frame(root)

frame_user_select.grid(row=0, column=0, sticky="nsew")
frame_user.grid(row=0, column=0, sticky="nsew")
frame_inventory.grid(row=0, column=0, sticky="nsew")
frame_gacha.grid(row=0, column=0, sticky="nsew")
frame_gacha_got_char.grid(row=0, column=0, sticky="nsew")
frame_charac_list.grid(row=0, column=0, sticky="nsew")
frame_charac_info.grid(row=0, column=0, sticky="nsew")

Selected_user = None
Username = None
UID = None
Gold = None
Pyroxene = None

# ------------------------------- 첫 화면. 로그인 프레임 -------------------------- #
# 로그인 프래임
# 맨 위에 글들
su_label0 = Label(frame_user_select, text="로그인")
su_label0.grid(row=0, column=2)

su_label1 = Label(frame_user_select, text="신규 유저")
su_label1.grid(row=1, column=1, sticky="s")

su_label2 =Label(frame_user_select, text="기존 유저 선택")
su_label2.grid(row=1, column=3, sticky="s")

# 신규 유저 생성 닉네임 입력
su_newname_entry = Entry(frame_user_select, width = 30)
su_newname_entry.grid(row=2, column=1)
su_newname_entry.insert(0, "닉네임을 입력해주세요")

# 유저 생성 버튼
def newuser():
    nickname = su_newname_entry.get()
    stat=0
    
    if len(nickname) > 0:
        if su_userlist.size() == 0:
            su_userlist.insert(END, nickname)
            db.userinsert(nickname)
            db.userprint()
            return
        # 중복된 닉네임 확인
        for ch in su_userlist.get(0,su_userlist.size()) :
            if ch == nickname:
                stat=1
                print("중복금지")
                break

        if stat != 1:
            su_userlist.insert(END, nickname)
            db.userinsert(nickname)
            db.userprint()

su_main_newuser_btn = Button(frame_user_select, padx=10, pady=5, text="신규 유저 생성", command=newuser)
su_main_newuser_btn.grid(row=2, column=1, sticky="s")

# 존재하는 유저 list box
su_userlist = Listbox(frame_user_select, selectmode="single", width=30, height=9)
su_userlist.grid(row=2, column=3, sticky="n")

# 기존 존재하던 유저 입력
row = db.userprint()
for us in row:
    c = us[0]
    su_userlist.insert(END, c)

# 선택 유저 접속 버튼
def openFrame(frame):
    frame.tkraise()

def seluser(frame):
    global Selected_user
    if su_userlist.curselection() :
        Selected_user = su_userlist.get(su_userlist.curselection())
        print(Selected_user)
        openFrame(frame)

def patch_userinfo(Selected_user):
    global Username
    global UID
    global Gold
    global Pyroxene
    if su_userlist.curselection() :
        Username = db.seled_user("Username", Selected_user)
        UID = db.seled_user("UID", Selected_user)
        Gold = db.seled_user("Gold", Selected_user)
        Pyroxene = db.seled_user("Pyroxene", Selected_user)
        uf_label_user_nickname.configure(text=Username)
        uf_label_user_UID.configure(text=UID)
        uf_label_owned_gold.configure(text=Gold)
        uf_label_owned_Pyroxene.configure(text=Pyroxene)


su_user_select_btn = Button(frame_user_select, padx=15, pady=5, text="접속하기", command=lambda:[seluser(frame_user), patch_userinfo(Selected_user)])
su_user_select_btn.grid(row=3, column=3, sticky="w")

# 선택 유저 삭제 버튼
def user_deletion():
    if su_userlist.curselection() :
        selected_user = su_userlist.get(su_userlist.curselection())
        print(selected_user)
        db.userdelete(selected_user)
        su_userlist.delete(su_userlist.curselection())

su_user_deletion_btn = Button(frame_user_select, padx=15, pady=5, text="삭제하기", command=user_deletion)
su_user_deletion_btn.grid(row=3, column=3, sticky="e")


# --------------------------- 2번 선택한 유저 화면 ----------------------- #
# 유저 닉네임 #
uf_label_nickname = Label(frame_user, text="이름 :")
uf_label_nickname.grid(row=1, column=1, sticky="e")

uf_label_user_nickname = Label(frame_user, text=Username)
uf_label_user_nickname.grid(row=1, column=2, sticky="w")

# 유저 ID #
uf_label_UID = Label(frame_user, text="UID :")
uf_label_UID.grid(row=1, column=3, sticky="e")

uf_label_user_UID = Label(frame_user, text=UID)
uf_label_user_UID.grid(row=1, column=4, sticky="w")

# 보유중인 골드 #
uf_label_gold = Label(frame_user, text="골드 :")
uf_label_gold.grid(row = 1, column=5, sticky="e")

uf_label_owned_gold = Label(frame_user, text=Gold)
uf_label_owned_gold.grid(row = 1, column=6, sticky="w")

# 보유중인 청휘석 #
uf_label_Pyroxene = Label(frame_user, text="청휘석 :")
uf_label_Pyroxene.grid(row = 1, column=7, sticky="e")

uf_label_owned_Pyroxene = Label(frame_user, text=Pyroxene)
uf_label_owned_Pyroxene.grid(row = 1, column=8, sticky="w")

def backlogin(frame):
    global Selected_user
    Selected_user = None
    openFrame(frame)

# 첫 화면으로 돌아가는 버튼 #
uf_btn_backtologin = Button(frame_user, text="<-", padx=10, pady=5, command=lambda:[backlogin(frame_user_select)])
uf_btn_backtologin.grid(row=0, column=0)

# 캐릭터 뽑기 텍스트 #
uf_label_gacha = Label(frame_user, text="\n\n캐릭터 뽑으러 가기")
uf_label_gacha.grid(row=4, column = 2)
# 캐릭터 뽑기창으로 이동하는 버튼 #
uf_btn_go_gacha = Button(frame_user, text="뽑기", padx=10, pady=5, command=lambda:[openFrame(frame_gacha)])
uf_btn_go_gacha.grid(row=5, column = 2, sticky="s")

def setinventory(UID):
    row=db.read_inventory(UID)
    for i in row:
        itemid = i[0]
        itemname = db.itemname(itemid)
        remains = i[1]
        item_text = "이름 : %s     남은 수량 : %s  ID : %s" %(itemname, remains, itemid)
        inven_itemlist2.insert(END, item_text)


# 인벤토리 텍스트 #
uf_label_gacha = Label(frame_user, text="\n\n보유중인 아이템 보기")
uf_label_gacha.grid(row=4, column = 4) 
# 인벤토리로 이동하는 버튼 #
uf_btn_go_inventory = Button(frame_user, text="인벤토리", padx=10, pady=5, command=lambda:[openFrame(frame_inventory), setinventory(UID)])
uf_btn_go_inventory.grid(row=5, column = 4, sticky="s")

# 캐릭터 목록 텍스트 #
uf_label_gacha = Label(frame_user, text="\n\n보유중인 캐릭터 보기")
uf_label_gacha.grid(row=4, column = 6, sticky="s")
# 캐릭터 목록으로 이동하는 버튼 #
uf_btn_go_charlist = Button(frame_user, text="캐릭터", padx=10, pady=5, command=lambda:[openFrame(frame_charac_list)])
uf_btn_go_charlist.grid(row=5, column = 6)

#------------------ 캐릭터 뽑기를 할 수 있는 프레임 -------------- #
# 첫 화면으로 돌아가는 버튼 #
def back_frame_user():
    global Gold
    global Pyroxene
    uf_label_owned_gold.configure(text=Gold)
    uf_label_owned_Pyroxene.configure(text=Pyroxene)
    openFrame(frame_user)

gc_btn_backtomain = Button(frame_gacha, text="<-", padx=10, pady=5, command=back_frame_user)
gc_btn_backtomain.grid(row=0, column=0)

# 캐릭터 뽑기 프레임이라는 텍스트 #
gc_label_gacha = Label(frame_gacha, text="캐릭터 뽑기")
gc_label_gacha.grid(row=0, column=2)

# 가챠해서 저장하고 출력
def gachalogic():
    char_get = gc.rare_gacha()
    db.get_charac(UID, char_get)
    getinfo = db.getcharbasicinfo(char_get)
    char_name = getinfo[0]
    char_star = getinfo[1]
    gettext ="%s      ★%s" %(char_name, char_star)
    ggc_get_charlist.insert(END, gettext)

def gacha10logic():
    char_get = gc.gacha_10last()
    db.get_charac(UID, char_get)
    getinfo = db.getcharbasicinfo(char_get)
    char_name = getinfo[0]
    char_star = getinfo[1]
    gettext ="%s      ★%s" %(char_name, char_star)
    ggc_get_charlist.insert(END, gettext)

# 청휘석 소모, 가챠 실행
def dogacha(num):
    global Pyroxene
    Pyroxene = Pyroxene - (120 * num)
    db.update_pyroxene(Pyroxene, UID)

    if num == 1:
        gachalogic()

    elif num == 10:
        for i in range(9):
            gachalogic()
        # 10번째는 2성 이상 확정
        gacha10logic()

# 캐릭터 1번 뽑기 텍스트 #
gc_label_gacha1 = Label(frame_gacha, text="120 청휘석 소모")
gc_label_gacha1.grid(row=1, column=2)

# 캐릭터 뽑기 1회 
gc_btn_gacha = Button(frame_gacha, text="1회 뽑기", command=lambda:[openFrame(frame_gacha_got_char), dogacha(1)])
gc_btn_gacha.grid(row=2, column=2, sticky="s")

# 캐릭터 10번 뽑기 텍스트 #
gc_label_gacha10 = Label(frame_gacha, text="1200 청휘석 소모")
gc_label_gacha10.grid(row=1, column=4)
# 캐릭터 뽑기 10회 
gc_btn_gacha = Button(frame_gacha, text="10회 뽑기", command=lambda:[openFrame(frame_gacha_got_char), dogacha(10)])
gc_btn_gacha.grid(row=2, column=4, sticky="s")


#------------------ 뽑기로 뽑은 캐릭터를 확인하는 프레임 ---------------#
# 전 화면으로 돌아가는 버튼
ggc_btn_back = Button(frame_gacha_got_char, text="확인", command=lambda:[openFrame(frame_gacha), ggc_get_charlist.delete(0,END)])
ggc_btn_back.grid(row=1, column=1)

# 뽑은 캐릭터 확인하는 listbox
ggc_get_charlist = Listbox(frame_gacha_got_char, selectmode="single")
ggc_get_charlist.grid(row=2, column=3, sticky="nsew")

#--------------------- 인벤토리를 확인하는 프레임 ---------------------#
# 전 화면으로 돌아가는 버튼
def del_inven():
    inven_itemlist2.delete(0,END)
    inven_itemname_entry.configure(text="\nitem name"+"\n\n")
    inven_itemlist.configure(text="Item Description\n\n")
    
inven_btn_back = Button(frame_inventory, text="<-", padx=10, pady=5, command=lambda:[openFrame(frame_user), del_inven()])
inven_btn_back.grid(row=0, column=0, sticky="w")

# 아이템 설명 텍스트
inven_itemdesc = Label(frame_inventory, text="아이템 설명")
inven_itemdesc.grid(row=0, column=1)

# 선택한 아이템 이름
inven_itemname_entry = Label(frame_inventory, text="\nitem name\n\n")
inven_itemname_entry.grid(row=1, column=1, sticky="n")

# 아이템 설명이 나올 리스트 박스
inven_itemlist =Label(frame_inventory, text="Item Description\n\n", width=30, wraplength=200)
inven_itemlist.grid(row=1, column=1, sticky="s")

# 보유중인 아이템 텍스트
inven_itemlist_text = Label(frame_inventory, text="보유중인 아이템")
inven_itemlist_text.grid(row=0, column=2)
# 보유중인 아이템이 출력될 리스트 박스
inven_itemlist2 = Listbox(frame_inventory, selectmode="single", width=50)
inven_itemlist2.grid(row=1, column=2, sticky="nsew")

# 선택한 아이템 정보 출력
def iteminfo():
    if inven_itemlist2.curselection() :
        selected_item = inven_itemlist2.get(inven_itemlist2.curselection())
        selected_item = selected_item[-5:]
        info=db.itemdesc(selected_item)
        name = info[0]
        desc = info[1]
        inven_itemname_entry.configure(text="\nitem name"+"\n\n"+name)
        inven_itemlist.configure(text="Item Description\n\n"+desc)
        
# 선택한 아이템의 정보 확인
inven_btn_iteminfo = Button(frame_inventory, text="선택한 아이템 정보 확인", padx=10, pady=5, command=iteminfo)
inven_btn_iteminfo.grid(row=2, column=2)

#--------------------- 캐릭터 리스트를 확인하는 프레임 ------------------#
clist_btn_back = Button(frame_charac_list, text="<-", padx=10, pady=5, command=lambda:[openFrame(frame_user)])
clist_btn_back.grid(row=0, column=0)

# 보유중인 캐릭터 텍스트
clist_charlist_label = Label(frame_charac_list, text="보유중인 캐릭터")
clist_charlist_label.grid(row=0, column=1, sticky="n")
# 보유중인 캐릭터 리스트박스
clist_charlist_listbox = Listbox(frame_charac_list, selectmode="single")
clist_charlist_listbox.grid(row=1, column=1, sticky="nswe")

clist_charlist_listbox.insert(END, "이오리")

# 선택한 캐릭터 정보 화면으로
def char_info(frame):
    if clist_charlist_listbox.curselection() :
        selected_character = clist_charlist_listbox.get(clist_charlist_listbox.curselection())
        openFrame(frame)

clist_charlist_btn = Button(frame_charac_list, padx=15, pady=5, text="캐릭터 정보 확인", command=lambda:[char_info(frame_charac_info)])
clist_charlist_btn.grid(row=3, column=1)

#--------------------- 캐릭터 정보를 확인하는 프레임 -------------------#
cinfo_btn_back = Button(frame_charac_info, text="<-", padx=10, pady=5, command=lambda:[openFrame(frame_charac_list)])
cinfo_btn_back.grid(row=0, column=0)

name = "이오리"
level_int = 1
total_exp_int = 0
now_exp_int = 0
star_quant_int = 1
atk_int = 1000
def_int = 100
max_hp_int = 10000
EX_level_int = 1
Basic_level_int = 1
attackrange = 650
crit_int = 200
crit_damage_int = 200000
itemtier_int = 1
itemlevel_int = 1

Name = "Character name : %s" %(name)
EXP = "EXP : %s" %(now_exp_int)
STARTS = "Star quantity : %s" %(star_quant_int)
Level = " Level : %s" %(level_int)
ATK = " ATK : %s" %(atk_int)
DEF = " DEF : %s" %(def_int)
MAX_HP = "MAX HP : %s" %(max_hp_int)
Normal_atk_rangee = "Normal attack range : %s" %(attackrange)
Crit = "Crit : %s" %(crit_int)
Crit_damage = "Crit damage : %s" %(crit_damage_int)
EX_level = "EX skill level : %s" %(EX_level_int)
Basic_level = "Basic skill level : %s" %(Basic_level_int)
Item_tier = "Item tier : %s" %(itemtier_int)
Item_level = "Item level : %s" %(itemlevel_int)


# 선택한 캐릭터 정보 텍스트
cinfo_charinfo_label = Label(frame_charac_info, text="캐릭터 정보")
cinfo_charinfo_label.grid(row=0, column=3, sticky="e")

# 보유중인 캐릭터 정보 출력
# 이름
cinfo_charinfo_name = Label(frame_charac_info, text=Name)
cinfo_charinfo_name.grid(row=1, column=2)
# 별 개수
cinfo_charinfo_stars = Label(frame_charac_info, text=STARTS)
cinfo_charinfo_stars.grid(row=1, column=3, sticky="e")
# 레벨
cinfo_charinfo_level = Label(frame_charac_info, text=Level)
cinfo_charinfo_level.grid(row=2, column=2)
# 경험치
cinfo_charinfo_exp = Label(frame_charac_info, text=EXP)
cinfo_charinfo_exp.grid(row=2, column=3)
# 공격력
cinfo_charinfo_atk = Label(frame_charac_info, text=ATK)
cinfo_charinfo_atk.grid(row=3, column=2)
# 방어력
cinfo_charinfo_def = Label(frame_charac_info, text=DEF)
cinfo_charinfo_def.grid(row=3, column=3)
# 체력
cinfo_charinfo_max_hp = Label(frame_charac_info, text=MAX_HP)
cinfo_charinfo_max_hp.grid(row=3, column=4)
# 공격 사거리
cinfo_charinfo_Normal_range = Label(frame_charac_info, text=Normal_atk_rangee)
cinfo_charinfo_Normal_range.grid(row=4, column=2, sticky="s")
# 크리티컬
cinfo_charinfo_Crit = Label(frame_charac_info, text=Crit)
cinfo_charinfo_Crit.grid(row=4, column=3, sticky="s")
# 크리 데미지
cinfo_charinfo_Crit_damage = Label(frame_charac_info, text=Crit_damage)
cinfo_charinfo_Crit_damage.grid(row=4, column=4, sticky="s")
# EX 스킬 레벨
cinfo_charinfo_EX_level = Label(frame_charac_info, text=EX_level)
cinfo_charinfo_EX_level.grid(row=5, column=2, sticky="s")
# 기본 스킬 레벨
cinfo_charinfo_Basic_level = Label(frame_charac_info, text=Basic_level)
cinfo_charinfo_Basic_level.grid(row=5, column=3, sticky="s")
# 아이템 티어
cinfo_charinfo_item_tier = Label(frame_charac_info, text=Item_tier)
cinfo_charinfo_item_tier.grid(row=6, column=2, sticky="s")
# 아이템 레벨
cinfo_charinfo_item_level = Label(frame_charac_info, text=Item_level)
cinfo_charinfo_item_level.grid(row=6, column=3, sticky="s")

# 골드 계산
def patchGold(num):
    global Gold
    Gold = Gold - (num)
    db.update_pyroxene(Gold, UID)

# 캐릭터 스탯 재계산
def update_stat():
    global atk_int
    global def_int
    global max_hp_int
    atk_int += 1
    def_int += 1
    max_hp_int += 1
    ATK = " ATK : %s" %(atk_int)
    DEF = " DEF : %s" %(def_int)
    MAX_HP = "MAX HP : %s" %(max_hp_int)
    cinfo_charinfo_atk.configure(text=ATK)
    cinfo_charinfo_def.configure(text=DEF)
    cinfo_charinfo_max_hp.configure(text=MAX_HP)

# 캐릭터 등급 상승 버튼
def star_up():
        global star_quant_int
        if star_quant_int < 5:
            star_quant_int += 1
            STARTS = "Star quantity : %s" %(star_quant_int)
            cinfo_charinfo_stars.configure(text=STARTS)
            update_stat()

cinfo_btn_Char_stars = Button(frame_charac_info, text="Character Star up", padx=10, pady=5, command=star_up)
cinfo_btn_Char_stars.grid(row=1, column=4)

cinfo_conmat_starup = Label(frame_charac_info, text="소모 골드 : 100000\n소모 엘리그마 50")
cinfo_conmat_starup.grid(row=1, column=5)

# 캐릭터 레벨업 버튼

def Ch_expup(exp):
    global level_int
    global total_exp_int
    global now_exp_int
    if level_int < 80:
        total_exp_int += exp
        now_exp_int += exp

        if now_exp_int > 600:
            now_exp_int -= 600
            level_int += 1
            Level = " Level : %s" %(level_int)
            cinfo_charinfo_level.configure(text=Level)
            update_stat()
            
        EXP = "EXP : %s" %(now_exp_int)
        cinfo_charinfo_exp.configure(text=EXP)

cinfo_btn_Char_exp100up = Button(frame_charac_info, text="Character EXP +100\n소모골드 : 1000", padx=10, pady=5, command=lambda:[Ch_expup(100)])
cinfo_btn_Char_exp100up.grid(row=2, column=4)

cinfo_btn_Char_exp1000up = Button(frame_charac_info, text="Character EXP +1000\n소모골드 : 10000", padx=10, pady=5, command=lambda:[Ch_expup(1000)])
cinfo_btn_Char_exp1000up.grid(row=2, column=5)

# 스킬 레벨업 버튼
def EX_levelup():
    global EX_level_int
    if EX_level_int < 5:
       EX_level_int = EX_level_int + 1
       EX_level = "EX skill level : %s" %(EX_level_int)
       cinfo_charinfo_EX_level.configure(text = EX_level)
        
def Basic_levelup():
    global Basic_level_int
    if Basic_level_int < 10:
       Basic_level_int = Basic_level_int + 1
       Basic_level = "Basic Skill level : %s" %(Basic_level_int)
       cinfo_charinfo_Basic_level.configure(text = Basic_level)

# EX 스킬 레벨업
cinfo_btn_Ex_levelup = Button(frame_charac_info, text="Ex level up\n소모골드 : 100000", padx=10, pady=5, command=EX_levelup)
cinfo_btn_Ex_levelup.grid(row=5, column=4)

# 기본 스킬 레벨업
cinfo_btn_Basic_levelup = Button(frame_charac_info, text="Basic level up\n소모골드 : 10000", padx=10, pady=5, command=Basic_levelup)
cinfo_btn_Basic_levelup.grid(row=5, column=5)

# 장비 레벨업 버튼
def Item_levelup():
    global itemlevel_int
    global itemtier_int
    if itemlevel_int < 30:
        itemlevel_int = itemlevel_int + 1
        Item_level = "Item level : %s" %(itemlevel_int)
        cinfo_charinfo_item_level.configure(text = Item_level)
        update_stat()

    elif itemlevel_int >= 30 and itemtier_int < 4:
        itemlevel_int = 1
        itemtier_int = itemtier_int + 1
        Item_tier = "Item tier : %s" %(itemtier_int)
        Item_level = "Item level : %s" %(itemlevel_int)
        cinfo_charinfo_item_level.configure(text = Item_level)
        cinfo_charinfo_item_tier.configure(text = Item_tier)
        update_stat()

cinfo_btn_Item_levelup = Button(frame_charac_info, text="Equipment level up\n소모골드 : 10000", padx=10, pady=5, command=Item_levelup)
cinfo_btn_Item_levelup.grid(row=6, column=4)

# gui 실행 #
openFrame(frame_user_select)
root.resizable(False, False)
root.mainloop()

db.cursor.close()
db.connection.close()