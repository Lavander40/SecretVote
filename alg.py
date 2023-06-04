from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
from enc import *

global se, sn, sd, e, n, d, msg
se, sn, sd, e, n, d, msg = 0, 0, 0, 0, 0, 0, 0

def com1():
    if log.get() == '' or pas.get() == '':
        lb['text'] = "Пожалуйста, заполните поля регистрации"
        return

    if not reg(log.get(), pas.get()):
        lb['text'] = "Данные пользователя не верны"
        return

    lb['text'] = "Вы принимаете участие в голосовании\nВыберете кандидата"
    bt.pack_forget()
    log.pack_forget()
    log_lb.pack_forget()
    pas.pack_forget()
    pas_lb.pack_forget()
    g1.pack()
    g2.pack()
    g3.pack()
    bt1.pack(pady=10)
    lbg.pack(pady=10)
    slb['text'] = f"Пользователь {log.get()} учавствует в голосовании"
    sbtn.pack()

def reg(login, password):
    return True

def com2():
    global e, n, d
    if golos.get() == 0:
        lbg['text'] = "Пожалуйста, выберете кандидата из списка"
        return
    result = askyesno(title="Подтвержение выбора", message=f"В подтверждаете выбор канидата №{golos.get()}?")
    if result:
        g1.pack_forget()
        g2.pack_forget()
        g3.pack_forget()
        bt1.pack_forget()
        lbg['text'] = f"Голос за кандидата №{golos.get()} принят"
        smp1 = gSimple()
        smp2 = gSimple()
        e, n, d = gKey(smp1, smp2)
        lbsimpl['text'] = f"Для дальнейшей передачи сгенерированы\nдва простых числа {smp1}, {smp2}\nНа из основе получены ключи ({e}, {n}),\n({d}, {n})"
        lbsimpl.pack()

def sign():
    global msg
    signbtn.pack_forget()
    ok.pack()
    msg = encrypt(golos.get(), d, n)
    sendbtn.pack()

def send():
    global msg
    sendbtn.pack_forget()
    ok.pack_forget()
    sended.pack()
    msg = encrypt(msg, se, sn)
    svdecrbtn.pack()

app = Tk()
app.geometry("400x300+" + str(app.winfo_screenwidth()//8) + "+" + str(app.winfo_screenheight()//4))
app.title("Система голосования")
app.resizable(False, False)

ok = Label(text="Сообщение подписано")
sended = Label(text="Сообщение отправлено")
log_lb = Label(text="Идентификатор голосующего:")
log_lb.pack(pady=10)
log = Entry()
log.pack()
pas_lb = Label(text="Секретный ключ голосующего:")
pas_lb.pack(pady=5)
pas = Entry()
pas.pack()

bt = Button(text="Принять участие в голосовании", command=com1)
bt.pack(pady=10)
lb = Label()
lb.pack(pady=10)

golos = IntVar()
golos.set(0)
g1 = ttk.Radiobutton(text="Кандидат 1", value=1, variable=golos)
g2 = ttk.Radiobutton(text="Кандидат 2", value=2, variable=golos)
g3 = ttk.Radiobutton(text="Кандидат 3", value=3, variable=golos)
bt1 = Button(text="Отправить голос", command=com2)
lbg = Label()

lbsimpl = Label()
serverkey = Label()
signbtn = Button(text="Подписать сообщение", command=sign)
sendbtn = Button(text="Отправить сообщение", command=send)


def genKey():
    global se, sn, sd
    sbtn.pack_forget()
    smp1 = gSimple()
    smp2 = gSimple()
    se, sn, sd = gKey(smp1, smp2)
    slb2['text'] = f"Для передачи сгенерированы\nдва простых числа {smp1}, {smp2}\nНа из основе получены ключи ({se}, {sn}),\n({sd}, {sn})"
    serverkey['text'] = f"Получен открытый ключ системы верификации голосования\n{se, sn},\nвозможна передача результатов"
    serverkey.pack()
    signbtn.pack()
    slb2.pack()

def decr():
    global msg
    msg = decrypt(msg, sd, sn)
    svdecrbtn.pack_forget()
    svcheckbtn.pack()

def check():
    global msg
    svcheckbtn.pack_forget()
    msg = decrypt(msg, e, n)
    msg = round(msg)
    final['text'] = f"Полученный голос: {msg}"
    final.pack()
    if msg == 1 or msg == 2 or msg == 3:
        sended['text'] = "Голос успешно принят"
    else:
        sended['text'] = "Подпись не прошла проверку\nголос не засчитан"

server = Tk()
server.geometry("400x250+" + str(app.winfo_screenwidth()//8) + "+" + str(app.winfo_screenheight()//4))
server.title("Система валидации голосов")
server.resizable(False, False)

slb = Label(server)
slb.pack(pady=10)
slb2 = Label(server)
sbtn = Button(server, text="Сгенерировать ключи", command=genKey)
svcheckbtn = Button(server, text="Проверить подпись", command=check)
svdecrbtn = Button(server, text="Получить сообщение", command=decr)
final = Label(server)

app.mainloop()
server.mainloop()