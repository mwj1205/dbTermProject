import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import *
import mydb as db
import gacha as gc

root = Tk()
root.title("Blue Archive")
root.geometry("640x380")

#서브 프레임 생성
frame_user_select = Frame(root)
frame_user = Frame(root)
frame_get_item = Frame(root)
frame_inventory = Frame(root)
frame_gacha = Frame(root)
frame_gacha_got_char = Frame(root)
frame_charac_list = Frame(root)
frame_charac_info = Frame(root)

frame_user_select.grid(row=0, column=0, sticky="nsew")
frame_user.grid(row=0, column=0, sticky="nsew")
frame_get_item.grid(row=0, column=0, sticky="nsew")
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
                messagebox.showinfo("Error", "중복된 닉네임이 존재합니다")
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
        messagebox.showinfo("선택한 유저 정보", "Name = %s\nUID = %s" %(Username, UID))


su_user_select_btn = Button(frame_user_select, padx=15, pady=5, text="접속하기", command=lambda:[seluser(frame_user), patch_userinfo(Selected_user)])
su_user_select_btn.grid(row=3, column=3, sticky="w")

# 선택 유저 삭제 버튼
def user_deletion():
    if su_userlist.curselection() :
        selected_user = su_userlist.get(su_userlist.curselection())
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

def setcharlist(UID):
    row=db.read_charlist(UID)
    num_char = db.char_amount(UID)
    clist_charamount_label.configure(text = "보유중인 캐릭터 수 : %s" %(num_char))
    for i in row:
        charid = i[0]
        charname = db.charname(charid)
        clist_charlist_listbox.insert(END, charname)

# 캐릭터 목록 텍스트 #
uf_label_gacha = Label(frame_user, text="\n\n보유중인 캐릭터 보기")
uf_label_gacha.grid(row=4, column = 6, sticky="s")
# 캐릭터 목록으로 이동하는 버튼 #
uf_btn_go_charlist = Button(frame_user, text="캐릭터", padx=10, pady=5, command=lambda:[openFrame(frame_charac_list), setcharlist(UID)])
uf_btn_go_charlist.grid(row=5, column = 6)

# 아이템 얻기 텍스트 #
uf_label_getitem = Label(frame_user, text="\n\n아이템 얻으러 가기")
uf_label_getitem.grid(row=6, column= 2, sticky="s")
# 아이템을 얻는 화면으로 이동하는 버튼 #
uf_btn_getitem = Button(frame_user, text="아이템 얻기", padx=10, pady=5, command=lambda:[openFrame(frame_get_item)])
uf_btn_getitem.grid(row=7, column= 2, sticky="s")

#------------------ 캐릭터 뽑기를 할 수 있는 프레임 -------------- #
# 첫 화면으로 돌아가는 버튼 #
def back_frame_user():
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
# 10연 뽑기시 마지막 뽑기는 2성 확정
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
    if Pyroxene < 120 * num:
        messagebox.showinfo("Error", "골드가 부족합니다")
        return
    Pyroxene = Pyroxene - (120 * num)
    db.update_money("Pyroxene",Pyroxene, UID)

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
# 돌아갈 때 리스트 박스 초기화
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
# 전 화면으로 돌아가는 버튼
clist_btn_back = Button(frame_charac_list, text="<-", padx=10, pady=5, \
    command=lambda:[back_frame_user(), clist_charlist_listbox.delete(0,END)])
clist_btn_back.grid(row=0, column=0)

# 보유중인 캐릭터 수
clist_charamount_label = Label(frame_charac_list, text="보유중인 캐릭터 수 : ")
clist_charamount_label.grid(row=0, column=1, sticky="s")

# 보유중인 캐릭터 텍스트
clist_charlist_label = Label(frame_charac_list, text="보유중인 캐릭터")
clist_charlist_label.grid(row=0, column=2, sticky="w")

# 보유중인 캐릭터 리스트박스
clist_charlist_listbox = Listbox(frame_charac_list, selectmode="single")
clist_charlist_listbox.grid(row=1, column=1, sticky="nswe")

# 캐릭터 기본 정보 저장
#인덱스  0:CID  1:이름  2:팀  3:공격타입  4:방어타입  5:사거리  6:입는장비
def set_char_info(char_basic_info):
    charid_int = char_basic_info[0]
    name = char_basic_info[1]
    character_team = char_basic_info[2]
    attack_type = char_basic_info[3]
    defence_tpye = char_basic_info[4]
    attackrange = char_basic_info[5]
    wearable_equipment = char_basic_info[12]
    charbasiclist = [charid_int, name, character_team, attack_type, defence_tpye, attackrange, wearable_equipment]
    return charbasiclist

# 소유한 캐릭터의 현재 정보
# 인덱스  0:경험치,  1:별,  2:EX 레벨,  3:기본스킬 레벨, 4:장비티어, 5:장비레벨 
def now_char_stat(UID, charid):
    now_char_info = db.nowcharinfo(UID, charid)
    total_exp_int = now_char_info[0]
    star_quant_int = now_char_info[1]
    EX_level_int = now_char_info[2]
    Basic_level_int = now_char_info[3]
    itemtier_int = now_char_info[4]
    itemlevel_int = now_char_info[5]
    charnowlist = [total_exp_int, star_quant_int, EX_level_int, Basic_level_int, itemtier_int, itemlevel_int]
    return charnowlist

# 공격력, 방어력, 체력 계산
def calc_char_stat_lv(UID, charid): 
    # 인덱스  0 : 레벨,  1 : 공격력,  2 : 방어력,  3 : 체력,  4 : 크확,  5 : 크뎀
    char_now_stat = db.cal_char_stat_level(UID, charid)
    return char_now_stat

def calc_char_stat_equip(lvstat,etype, etier, elevel):
    eqstat = db.cal_char_equip(lvstat, etype, etier, elevel)
    return eqstat

def calc_char_stat_stars(eqstat, stars):
    starstat = eqstat
    for i in range(1,3):
        starstat[i] = starstat[i] * ((1.1)**stars)
    return starstat

def real_char_stat(UID, charid, etype, etier, elevel, stars):
    lvstat = calc_char_stat_lv(UID, charid)
    eqstat = calc_char_stat_equip(lvstat, etype, etier, elevel)
    starstat = calc_char_stat_stars(eqstat, stars)
    return starstat


# cb 인덱스  0:CID  1:이름  2:팀  3:공격타입  4:방어타입  5:사거리  6:입는장비
def update_char_basicinfo_frame(cb):
    charid_int = cb[0]
    name = cb[1]
    attack_type = cb[3]
    defence_type = cb[4]
    character_team = cb[2]
    attackrange = cb[5]

    CID = "CID : %s" %(charid_int)
    Name = "Character name : %s" %(name)
    ATK_type = "Attack type : %s" %(attack_type)
    DEF_type = "Defence type : %s" %(defence_type)
    CTeam = "Team : %s" %(character_team)
    Normal_atk_rangee = "Normal attack range : %s" %(attackrange)
    
    # 보유중인 캐릭터 정보 출력
    # 캐릭터 ID
    cinfo_charinfo_CID.configure(text = CID)
    # 이름
    cinfo_charinfo_name.configure(text=Name)
    # 공격 타입
    cinfo_charinfo_atk_type.configure( text=ATK_type)
    # 방어 타입
    cinfo_charinfo_def_type.configure(text=DEF_type)
    # 소속
    cinfo_charinfo_team.configure(text=CTeam)
    # 공격 사거리
    cinfo_charinfo_Normal_range.configure(text=Normal_atk_rangee)

# cn 인덱스  0:경험치,  1:별,  2:EX 레벨,  3:기본스킬 레벨, 4:장비티어, 5:장비레벨 
# rs 인덱스  0 : 레벨,  1 : 공격력,  2 : 방어력,  3 : 체력,  4 : 크확,  5 : 크뎀
def update_charstat_frame(cn, rs):
    level_int = rs[0]
    now_exp_int = cn[0]
    star_quant_int = cn[1]
    atk_int = int(rs[1])
    def_int = int(rs[2])
    max_hp_int = int(rs[3])
    EX_level_int = cn[2]
    Basic_level_int = cn[3]
    crit_int = rs[4]
    crit_damage_int = int(rs[5])
    itemtier_int = cn[4]
    itemlevel_int = cn[5]

    EXP = "EXP : %s" %(now_exp_int)
    STARTS = "Star quantity : %s" %(star_quant_int)
    Level = "Level : %s" %(level_int)
    ATK = " ATK : %s" %(atk_int)
    DEF = " DEF : %s" %(def_int)
    MAX_HP = "MAX HP : %s" %(max_hp_int)
    Crit = "Crit : %s" %(crit_int)
    Crit_damage = "Crit damage : %s" %(crit_damage_int)
    EX_level = "EX skill level : %s" %(EX_level_int)
    Basic_level = "Basic skill level : %s" %(Basic_level_int)
    Item_tier = "Item tier : %s" %(itemtier_int)
    Item_level = "Item level : %s" %(itemlevel_int)

    # 별 개수
    cinfo_charinfo_stars.configure(text=STARTS)
    # 레벨
    cinfo_charinfo_level.configure(text=Level)
    # 경험치
    cinfo_charinfo_exp.configure(text=EXP)
    # 공격력
    cinfo_charinfo_atk.configure(text=ATK)
    # 방어력
    cinfo_charinfo_def.configure(text=DEF)
    # 체력
    cinfo_charinfo_max_hp.configure(text=MAX_HP)
    # 크리티컬
    cinfo_charinfo_Crit.configure(text=Crit)
    # 크리 데미지
    cinfo_charinfo_Crit_damage.configure(text=Crit_damage)
    # EX 스킬 레벨
    cinfo_charinfo_EX_level.configure(text=EX_level)
    # 기본 스킬 레벨
    cinfo_charinfo_Basic_level.configure(text=Basic_level)
    # 아이템 티어
    cinfo_charinfo_item_tier.configure(text=Item_tier)
    # 아이템 레벨
    cinfo_charinfo_item_level.configure(text=Item_level)

def set_btn_text():
    need_money_text()
    cinfo_btn_Item_levelup.configure(text="Equipment level up\n소모골드 : %s" %((cnowinfo[5])*1000))

def build_nc_list():
    global cnowinfo
    global real_stat

    cnowinfo = now_char_stat(UID, cbasicinfo[0])
    real_stat = real_char_stat(UID, cbasicinfo[0], cbasicinfo[6] ,cnowinfo[4], cnowinfo[5], cnowinfo[1])
    update_charstat_frame(cnowinfo, real_stat)

# 선택한 캐릭터 정보 화면으로
def char_info(frame):
    global cbasicinfo

    if clist_charlist_listbox.curselection() :
        selected_character = clist_charlist_listbox.get(clist_charlist_listbox.curselection())
        char_basic_info = db.char_basicinfo(selected_character)
        cbasicinfo = set_char_info(char_basic_info)
        build_nc_list()
        update_char_basicinfo_frame(cbasicinfo)
        set_btn_text()
        need_bd_gold()
        need_basic_gold()
        openFrame(frame)

clist_charlist_btn = Button(frame_charac_list, padx=15, pady=5, text="캐릭터 정보 확인", command=lambda:[char_info(frame_charac_info)])
clist_charlist_btn.grid(row=3, column=1)

#--------------------- 캐릭터 정보를 확인하는 프레임 -------------------#
cinfo_btn_back = Button(frame_charac_info, text="<-", padx=10, pady=5, command=lambda:[openFrame(frame_charac_list)])
cinfo_btn_back.grid(row=0, column=0)

# 선택한 캐릭터 정보 텍스트
cinfo_charinfo_label = Label(frame_charac_info, text="캐릭터 정보")
cinfo_charinfo_label.grid(row=0, column=3, sticky="e")

# 보유중인 캐릭터 정보 출력
# 캐릭터 ID
cinfo_charinfo_CID = Label(frame_charac_info)
cinfo_charinfo_CID.grid(row=0, column=5, sticky="n")
# 이름
cinfo_charinfo_name = Label(frame_charac_info)
cinfo_charinfo_name.grid(row=1, column=2)
# 별 개수
cinfo_charinfo_stars = Label(frame_charac_info)
cinfo_charinfo_stars.grid(row=1, column=3, sticky="e")
# 공격 타입
cinfo_charinfo_atk_type = Label(frame_charac_info)
cinfo_charinfo_atk_type.grid(row=2, column=2)
# 방어 타입
cinfo_charinfo_def_type = Label(frame_charac_info)
cinfo_charinfo_def_type.grid(row=2, column=3)
# 소속
cinfo_charinfo_team = Label(frame_charac_info)
cinfo_charinfo_team.grid(row=2, column=4)
# 레벨
cinfo_charinfo_level = Label(frame_charac_info)
cinfo_charinfo_level.grid(row=3, column=2)
# 경험치
cinfo_charinfo_exp = Label(frame_charac_info)
cinfo_charinfo_exp.grid(row=3, column=3)
# 공격력
cinfo_charinfo_atk = Label(frame_charac_info)
cinfo_charinfo_atk.grid(row=4, column=2)
# 방어력
cinfo_charinfo_def = Label(frame_charac_info)
cinfo_charinfo_def.grid(row=4, column=3)
# 체력
cinfo_charinfo_max_hp = Label(frame_charac_info)
cinfo_charinfo_max_hp.grid(row=4, column=4)
# 공격 사거리
cinfo_charinfo_Normal_range = Label(frame_charac_info)
cinfo_charinfo_Normal_range.grid(row=5, column=2, sticky="s")
# 크리티컬
cinfo_charinfo_Crit = Label(frame_charac_info)
cinfo_charinfo_Crit.grid(row=5, column=3, sticky="s")
# 크리 데미지
cinfo_charinfo_Crit_damage = Label(frame_charac_info)
cinfo_charinfo_Crit_damage.grid(row=5, column=4, sticky="s")
# EX 스킬 레벨
cinfo_charinfo_EX_level = Label(frame_charac_info)
cinfo_charinfo_EX_level.grid(row=6, column=2)
# 기본 스킬 레벨
cinfo_charinfo_Basic_level = Label(frame_charac_info)
cinfo_charinfo_Basic_level.grid(row=6, column=3)
# 아이템 티어
cinfo_charinfo_item_tier = Label(frame_charac_info)
cinfo_charinfo_item_tier.grid(row=7, column=2)
# 아이템 레벨
cinfo_charinfo_item_level = Label(frame_charac_info)
cinfo_charinfo_item_level.grid(row=7, column=3)

# 골드 계산
def patchGold(num):
    global Gold
    Gold = Gold - (num)
    db.update_money("Gold", Gold, UID)

# 엘리그마 사용
def patcheligma(num):
    db.patcheligma(UID, cbasicinfo[0], num)

# 골드가 충분한지 확인
def check_need_gold(needgold):
    checkgold = db.check_needgold(UID, needgold)

    if checkgold == 1:
        patchGold(needgold)
        return 1
    else: 
        messagebox.showinfo("Error", "골드가 부족합니다")
        return 0

# 캐릭터를 업그레이드 시킬 진화석이 있는지 확인
def check_eligma():
    if cnowinfo[1] == 1:
        needeligma = 30
    elif cnowinfo[1] == 2:
        needeligma = 80
    elif cnowinfo[1] == 3:
        needeligma = 100
    elif cnowinfo[1] == 4:
        needeligma = 120
    else:
        return 0
    checkeligma = db.check_needeligma(UID, cbasicinfo[0], needeligma)

    if checkeligma == 1:
        patcheligma(needeligma)
        return 1
    else: 
        messagebox.showinfo("Error", "엘리그마가 부족합니다")
        return 0

# 캐릭터 등급 상승에 필요한 골드
def needgold_starup():
    if cnowinfo[1] == 1:
        needgold = 10000
    elif cnowinfo[1] == 2:
        needgold = 40000
    elif cnowinfo[1] == 3:
        needgold = 200000
    elif cnowinfo[1] == 4:
        needgold = 1000000
    else:
        return 0
    return needgold

# 캐릭터 등급 상승
def star_up():
    if cnowinfo[1] < 5:
        needgold = needgold_starup()
        if check_eligma() and check_need_gold(needgold):
            db.char_levelup(UID, cbasicinfo[0], cnowinfo[1]+1, "Star_quantity")
            build_nc_list()
            need_money_text()

# 등급 상승시킬 때 필요한 재화량 출력
def need_money_text():
    if cnowinfo[1] == 1:
        mtext = "소모 골드 : 10,000\n소모 엘리그마 30"
    elif cnowinfo[1] == 2:
        mtext = "소모 골드 : 40,000\n소모 엘리그마 80"
    elif cnowinfo[1] == 3:
        mtext = "소모 골드 : 200,000\n소모 엘리그마 100"
    elif cnowinfo[1] == 4:
        mtext = "소모 골드 : 1,000,000\n소모 엘리그마 120"
    else:
        mtext = "최대 등급입니다"
    cinfo_conmat_starup.configure(text=mtext)

# 캐릭터 등급 상승 버튼
cinfo_btn_Char_stars = Button(frame_charac_info, text="Character Star up", padx=10, pady=5, command=star_up)
cinfo_btn_Char_stars.grid(row=1, column=4)

cinfo_conmat_starup = Label(frame_charac_info)
cinfo_conmat_starup.grid(row=1, column=5)

# 캐릭터 레벨업 버튼
def Ch_expup(exp):
    if real_stat[0] < 50:
        db.update_char_exp(UID, cbasicinfo[0], cnowinfo[0]+exp)
        build_nc_list()
        patchGold(exp*10)

cinfo_btn_Char_exp100up = Button(frame_charac_info, text="Character EXP +100\n소모골드 : 1000", padx=10, pady=5, command=lambda:[Ch_expup(100)])
cinfo_btn_Char_exp100up.grid(row=3, column=4)

cinfo_btn_Char_exp1000up = Button(frame_charac_info, text="Character EXP +1000\n소모골드 : 10000", padx=10, pady=5, command=lambda:[Ch_expup(1000)])
cinfo_btn_Char_exp1000up.grid(row=3, column=5)

# 스킬 레벨업 할 때 item code 찾기
def find_skill_item_id(type, cteam):
    if type == "EX":
        if cteam == "게헨나":
            itemid = 23010
        elif cteam == "트리니티":
            itemid = 23020
        elif cteam == "밀레니엄":
            itemid = 23030
        elif cteam == "아비도스":
            itemid = 23040
        elif cteam == "백귀야행":
            itemid = 23050
    elif type == "Basic":
        if cteam == "게헨나":
            itemid = 24010
        elif cteam == "트리니티":
            itemid = 24020
        elif cteam == "밀레니엄":
            itemid = 24030
        elif cteam == "아비도스":
            itemid = 24040
        elif cteam == "백귀야행":
            itemid = 24050
    return itemid

# ex 스킬 강화에 필요한 BD 수
def need_BD():
    if cnowinfo[2] == 1:
        needBD = 3
    elif cnowinfo[2] == 2:
        needBD = 5
    elif cnowinfo[2] == 3:
        needBD = 10
    elif cnowinfo[2] == 4:
        needBD = 20       
    else: return 0
    return needBD

# ex스킬 강화에 필요한 골드
def needgold_exskillup():
    if cnowinfo[2] == 1:
        needgold = 80000
    elif cnowinfo[2] == 2:
        needgold = 500000
    elif cnowinfo[2] == 3:
        needgold = 3000000
    elif cnowinfo[2] == 4:
        needgold = 10000000
    else:
        return 0
    return needgold

# ex 스킬을 업할 때 bd가 부족한지 확인
def check_exup_item(needBD):

    itemid = find_skill_item_id("EX", cbasicinfo[2])
    checkbd = db.check_skil_item(UID, itemid, needBD)

    if checkbd == 1:
        db.patch_items(UID, itemid, needBD)
        return 1
    else:
        messagebox.showinfo("Error", "BD가 부족합니다")
        return 0

# ex스킬 레벨업 실행
def EX_levelup():
    if cnowinfo[2] < 5:
        needBD = need_BD()
        needgold = needgold_exskillup()
        if check_exup_item(needBD) and check_need_gold(needgold):
            db.char_levelup(UID, cbasicinfo[0], cnowinfo[2]+1, "Active_skill_level")
            build_nc_list()
            need_bd_gold()

# ex스킬 레벨업 할 때 필요한 재화량 출력
def need_bd_gold():
    if cnowinfo[2] == 1:
        mtext = "소모 골드 : 80,000\n소모 BD : 3"
    elif cnowinfo[2] == 2:
        mtext = "소모 골드 : 500,000\n소모 BD : 5"
    elif cnowinfo[2] == 3:
        mtext = "소모 골드 : 3,000,000\n소모 BD : 10"
    elif cnowinfo[2] == 4:
        mtext = "소모 골드 : 10,000,000\n소모 BD : 20"
    else:
        mtext = "최대 레벨입니다"
    cinfo_btn_Ex_levelup.configure(text=mtext)

# EX 스킬 레벨업 버튼
cinfo_btn_Ex_levelup = Button(frame_charac_info, padx=10, pady=5, command=EX_levelup)
cinfo_btn_Ex_levelup.grid(row=6, column=4)

# 기본스길 강회에 필요한 기술노트
def need_note():
    if cnowinfo[3] == 1:
        need_note = 1
    elif cnowinfo[3] == 2:
        need_note = 3
    elif cnowinfo[3] == 3:
        need_note = 5
    elif cnowinfo[3] == 4:
        need_note = 8
    elif cnowinfo[3] == 5:
        need_note = 12
    elif cnowinfo[3] == 6:
        need_note = 15
    elif cnowinfo[3] == 7:
        need_note = 20
    elif cnowinfo[3] == 8:
        need_note = 30
    elif cnowinfo[3] == 9:
        need_note = 50
    else: return 0
    return need_note

# 기본스킬 강화에 필요한 골드
def needgold_basicskillup():
    if cnowinfo[3] == 1:
        needgold = 5000
    elif cnowinfo[3] == 2:
        needgold = 7500
    elif cnowinfo[3] == 3:
        needgold = 60000
    elif cnowinfo[3] == 4:
        needgold = 90000
    elif cnowinfo[3] == 5:
        needgold = 300000
    elif cnowinfo[3] == 6:
        needgold = 450000
    elif cnowinfo[3] == 7:
        needgold = 1500000
    elif cnowinfo[2] == 8:
        needgold = 2400000
    elif cnowinfo[2] == 9:
        needgold = 4000000
    else:
        return 0
    return needgold

# 기본 스킬 레벨업에 필요한 노트 채크
def check_basicup_item(need_note):
    itemid = find_skill_item_id("Basic", cbasicinfo[2])
    checknote = db.check_skil_item(UID, itemid, need_note)

    if checknote == 1:
        db.patch_items(UID, itemid, need_note)
        return 1
    else:
        messagebox.showinfo("Error", "기술노트가 부족합니다")
        return 0

# basic 스킬 레벨 업
def Basic_levelup():
    if cnowinfo[3] < 10:
        neednote = need_note()
        needgold = needgold_basicskillup()
        if check_basicup_item(neednote) and check_need_gold(needgold):
            db.char_levelup(UID, cbasicinfo[0], cnowinfo[3]+1, "Passive_skill_level")
            build_nc_list()
            need_basic_gold()

# basic 스킬 레벨업 할 때 필요한 재화량 출력
def need_basic_gold():
    if cnowinfo[3] == 1:
        mtext = "소모 골드 : 5,000\n소모 기술노트 : 1"
    elif cnowinfo[3] == 2:
        mtext = "소모 골드 : 7,500\n소모 기술노트 : 3"
    elif cnowinfo[3] == 3:
        mtext = "소모 골드 : 60,000\n소모 기술노트 : 5"
    elif cnowinfo[3] == 4:
        mtext = "소모 골드 : 90,000\n소모 기술노트 : 8"
    elif cnowinfo[3] == 5:
        mtext = "소모 골드 : 300,000\n소모 기술노트 : 12"
    elif cnowinfo[3] == 6:
        mtext = "소모 골드 : 450,000\n소모 기술노트 : 15"
    elif cnowinfo[3] == 7:
        mtext = "소모 골드 : 1,500,000\n소모 기술노트 : 20"
    elif cnowinfo[3] == 8:
        mtext = "소모 골드 : 2,400,000\n소모 기술노트 : 30"
    elif cnowinfo[3] == 9:
        mtext = "소모 골드 : 4,000,000\n소모 기술노트 : 50"
    else:
        mtext = "최대 레벨입니다"
    cinfo_btn_Basic_levelup.configure(text=mtext)

# 기본 스킬 레벨업
cinfo_btn_Basic_levelup = Button(frame_charac_info, padx=10, pady=5, command=Basic_levelup)
cinfo_btn_Basic_levelup.grid(row=6, column=5)

# 장비 레벨업 버튼
def Item_levelup():
    if cnowinfo[5] < 30:
        if check_need_gold(cnowinfo[5]*1000):
            db.char_levelup(UID, cbasicinfo[0], cnowinfo[5]+1, "Equipment_level")
            build_nc_list()

    elif cnowinfo[5] >= 30 and cnowinfo[4] < 4:
        if check_need_gold(cnowinfo[5]*1000):
            db.char_levelup(UID, cbasicinfo[0], cnowinfo[4]+1, "Equipment_tier")
            db.char_levelup(UID, cbasicinfo[0], 1, "Equipment_level")
            build_nc_list()
    cinfo_btn_Item_levelup.configure(text="Equipment level up\n소모골드 : %s" %((cnowinfo[5])*1000))

cinfo_btn_Item_levelup = Button(frame_charac_info, text="Equipment level up\n소모골드 : 10000", padx=10, pady=5, command=Item_levelup)
cinfo_btn_Item_levelup.grid(row=7, column=4)

# ------------------------ 아이템을 얻는 프레임 --------------------- # frame_get_item
gi_btn_backtomain = Button(frame_get_item, text="<-", padx=10, pady=5, command=back_frame_user)
gi_btn_backtomain.grid(row=0, column=0)

def gi_get_gold():
    num = gi_entry_getgold.get()
    if num.isdigit():
        num = int(num)
        if num <= 100000000:
            patchGold(-num)
        else : messagebox.showinfo("Error", "값이 너무 큽니다")
    else: messagebox.showinfo("Error", "정수를 입력해주세요")

# 골드 획득하는 부분
gi_label_getgold = Label(frame_get_item, text="\n골드 획득하기\n")
gi_label_getgold.grid(row=1, column=1)

gi_entry_getgold = Entry(frame_get_item, width = 30)
gi_entry_getgold.insert(0, "최대 1억 골드")
gi_entry_getgold.grid(row=2, column=1)

gi_btn_getgold = Button(frame_get_item, padx=10, pady=5, text="골드 획득", command=gi_get_gold)
gi_btn_getgold.grid(row=3, column=1)

def gi_get_pyroxene():
    num = gi_entry_getpyroxene.get()
    if num.isdigit():
        num = int(num)
        if num <= 100000000:
            global Pyroxene
            Pyroxene = Pyroxene + (num)
            db.update_money("Pyroxene", Pyroxene, UID)
        else : messagebox.showinfo("Error", "값이 너무 큽니다")
    else: messagebox.showinfo("Error", "정수를 입력해주세요")

# 보석 획득하는 부분
gi_label_getpyroxene = Label(frame_get_item, text="\n보석 획득하기\n")
gi_label_getpyroxene.grid(row=1, column=2)

gi_entry_getpyroxene = Entry(frame_get_item, width = 30)
gi_entry_getpyroxene.insert(0, "보석 최대 1억개")
gi_entry_getpyroxene.grid(row=2, column=2)

gi_btn_getpyroxene = Button(frame_get_item, padx=10, pady=5, text="보석 획득", command=gi_get_pyroxene)
gi_btn_getpyroxene.grid(row=3, column=2)

# 아이템 획득하는 부분
gi_label_getitem = Label(frame_get_item, padx=10, pady=5, text="\n\n아이템 얻기")
gi_label_getitem.grid(row = 4, column=1)

def gi_get_item():
    itemid = gi_combobox_getitem.get()
    num = gi_entry_getitem.get()
    if not itemid:
        messagebox.showinfo("Error", "Value not selected")
        return
    if num.isdigit():
        num = int(num)
        if num <= 100000000:
            db.patch_items_get(UID, itemid, num)
        else : messagebox.showinfo("Error", "값이 너무 큽니다")
    else: messagebox.showinfo("Error", "정수를 입력해주세요")

values = [str(i) for i in range(10000, 10020, 1)]
values.extend(str(i) for i in range(23010, 23060, 10))
values.extend(str(i) for i in range(24010, 24060, 10))
gi_combobox_getitem = ttk.Combobox(frame_get_item, height = 10, values=values)
gi_combobox_getitem.current()
gi_combobox_getitem.grid(row=5, column=1)

gi_btn_getitem = Button(frame_get_item, padx=10, pady=5, text="아이템 획득", command=gi_get_item)
gi_btn_getitem.grid(row=6, column=2)

gi_entry_getitem = Entry(frame_get_item, width = 30)
gi_entry_getitem.insert(0, "아이템 최대 1억개")
gi_entry_getitem.grid(row=5, column=2)

# gui 실행 #
openFrame(frame_user_select)
root.resizable(False, False)
root.mainloop()

db.cursor.close()
db.connection.close()