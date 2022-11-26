from tkinter import *

root = Tk()
root.title("Blue Archive")
root.geometry("640x280")
root.resizable(False, False)

label1 = Label(root, text="신규 유저")
label1.place(x=125, y=20)

label2 =Label(root, text="기존 유저 선택")
label2.place(x=430, y=20)

# 신규 유저 생성
newname_entry = Entry(root, width = 30)
newname_entry.place(x=55, y=100)
newname_entry.insert(0, "닉네임을 입력해주세요")

# 유저 생성 버튼
def newuser():
    nickname = newname_entry.get()
    if len(nickname) > 0:
        userlist.insert(END, nickname)

main_newuser_btn = Button(root, padx=10, pady=5, text="신규 유저 생성", command=newuser)
main_newuser_btn.place(x=100, y=130)

# 기존 유저 선택, 삭제
userlist = Listbox(root, selectmode="single", width=30, height=9)
userlist.place(x=370, y=45)
userlist.insert(END, "username")
userlist.insert(END, "username")
userlist.insert(END, "username")

# 선택 유저 접속 버튼
user_select_btn = Button(root, padx=15, pady=5, text="접속하기",)
user_select_btn.place(x=375, y=210)

# 선택 유저 삭제 버튼
def user_deletion():
    if userlist.curselection() :
        userlist.delete(userlist.curselection())

user_deletion_btn = Button(root, padx=15, pady=5, text="삭제하기", command=user_deletion)
user_deletion_btn.place(x=490, y=210)

root.mainloop()