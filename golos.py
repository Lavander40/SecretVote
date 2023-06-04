from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
import alg_encrypt as enc

global msg, S, K, P, Ke, Ce, E, D, N, C
msg, S, K, Ke = 0, 0, 0, 0#, 0, 0, 0

########################################################################################################################
app = Tk()
app.geometry("400x300+" + str(app.winfo_screenwidth()//8) + "+" + str(app.winfo_screenheight()//4))
app.title("Система голосования")
app.resizable(False, False)

server = Tk()
server.geometry("400x250+" + str(app.winfo_screenwidth()//8) + "+" + str(app.winfo_screenheight()//4))
server.title("Система валидации голосов")
server.resizable(False, False)
########################################################################################################################
def com1():
    if log.get() == '' or pas.get() == '':
        lb['text'] = "Пожалуйста, заполните поля регистрации"
        return
    if not reg(log.get(), pas.get()):
        lb['text'] = "Данные пользователя не верны"
        return
    lb['text'] = "Вы принимаете участие в голосовании\nВыберете кандидата"
    # clear
    log_lb.pack_forget()
    log.pack_forget()
    pas_lb.pack_forget()
    pas.pack_forget()
    join_bt.pack_forget()
    # set
    g1.pack()
    g2.pack()
    g3.pack()
    res_bt.pack(pady=10)
    gen_lb.pack()
    # server
    notice_lb['text'] = f"Пользователь {log.get()} учавствует в голосовании"

def reg(login, password):
    return True

def com2():
    global S, K, Ke, P, msg
    if golos.get() == 0:
        res_lb['text'] = "Пожалуйста, выберете кандидата из списка"
        return
    result = askyesno(title="Подтвержение выбора", message=f"В подтверждаете выбор канидата №{golos.get()}?")
    if result:
        msg = golos.get()
        g1.pack_forget()
        g2.pack_forget()
        g3.pack_forget()
        res_bt.pack_forget()
        res_lb['text'] = f"Голос за кандидата №{golos.get()} принят"
        K, P, S = enc.gKey(enc.genSimple(), enc.genSimple())
        Ke = K*P
        gen_lb['text'] = f"Для дальнейшей передачи сгенерированы\nK: {K}, S: {S}\nКлюч К маскируется случайным образом К': {Ke}"
        send_ke_lb['text'] = f"Получен ключ К': {Ke}"
        send_ke_lb.pack()
        gen_c_bt.pack()

def enc_bill():
    global msg
    serv_c_enc_bt.pack_forget()
    msg = enc.encrypt(msg, E, N)
    serv_c_sign_bt.pack()

def sign_bill():
    global msg, C
    serv_c_sign_bt.pack_forget()
    msg = enc.encrypt(msg, S, P)
    C = enc.decrypt(Ce, E, N)
    enc_bill_lb['text'] = f"Бюллетень зашифрован и подписан\nСнята маскировка с ключей К',С'\nK: {Ke / P}, C: {C}"
    enc_bill_lb.pack()
    send_all_bt.pack()

def send():
    send_all_bt.pack_forget()
    got_all_lb['text'] = f"Получены ключи С: {C}, К: {Ke / P}\nи подписанный бюллетень"
    got_all_lb.pack()
    check_all_bt.pack()

########################################################################################################################

log_lb = Label(text="Идентификатор голосующего:")
pas_lb = Label(text="Секретный ключ голосующего:")
log = Entry()
pas = Entry()
join_bt = Button(text="Принять участие в голосовании", command=com1)
lb = Label()

log_lb.pack(pady=10)
log.pack()
pas_lb.pack(pady=5)
pas.pack()
join_bt.pack(pady=10)
lb.pack(pady=10)
# -------------------------------------------------------------
golos = IntVar()
golos.set(0)
res_lb = Label()
gen_lb = Label()
g1 = ttk.Radiobutton(text="Кандидат 1", value=1, variable=golos)
g2 = ttk.Radiobutton(text="Кандидат 2", value=2, variable=golos)
g3 = ttk.Radiobutton(text="Кандидат 3", value=3, variable=golos)
res_bt = Button(text="Отправить голос", command=com2)
# -------------------------------------------------------------
serv_c_ans_lb = Label()
serv_c_enc_bt = Button(text="Зашифровать бюллетень", command=enc_bill)
serv_c_sign_bt = Button(text="Подписать бюллетень", command=sign_bill)
# -------------------------------------------------------------
enc_bill_lb = Label()
send_all_bt = Button(text="Отправить бюллетень, К и С", command=send)
final = Label()

########################################################################################################################
def gen_c():
    global Ce, E, D, N
    gen_c_bt.pack_forget()
    E, N, D = enc.gKey(enc.genSimple(), enc.genSimple())
    Ce = enc.encrypt(Ke, D, N)
    server_gen_lb['text'] = f"Полученный ключ подписан С': {Ce}\nОн и публичный ключ E: {E} отправлены голосующему"
    server_gen_lb.pack()
    serv_c_ans_lb['text'] = f"Получен подписанный ключ С': {Ce}\nи публичный ключ Е: {E}"
    serv_c_ans_lb.pack()
    serv_c_enc_bt.pack()

def check():
    global msg
    check_all_bt.pack_forget()
    msg = enc.decrypt(msg, K, P)
    msg = enc.decrypt(msg, D, N)
    msg = round(msg)
    if msg == 1 or msg == 2 or msg == 3:
        final['text'] = "Голос успешно принят"
        final_s['text'] = "Сообщение прошло проверку, голос засчитан"
    else:
        final['text'] = "Подпись не прошла проверку\nголос не засчитан"
    final.pack()

# new voter
notice_lb = Label(server)
# K'
send_ke_lb = Label(server)
# generate C'
gen_c_bt = Button(server, text="Подписать полученный ключ", command=gen_c)
server_gen_lb = Label(server)

notice_lb.pack(pady=10)

got_all_lb = Label(server)
check_all_bt = Button(server, text="Проверить С и К", command=check)
final_s = Label(server)
########################################################################################################################

app.mainloop()
server.mainloop()
