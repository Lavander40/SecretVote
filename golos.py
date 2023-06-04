from tkinter import *

def com1():
    lb['text'] = "Вы принимаете участие в голосовании"
    bt.pack_forget()

def com2():
    pass

app = Tk()
app.geometry("400x250+" + str(app.winfo_screenwidth()//8) + "+" + str(app.winfo_screenheight()//4))
app.title("Система голосования")
app.resizable(False, False)

bt = Button(text="Принять участие в голосовании", command=com1)
bt.pack(pady=10)
lb = Label()
lb.pack(pady=10)

bt1 = Button(text="Сгенерировать ключи", command=com2)
bt1.pack(pady=10)
lb1 = Label()
lb1.pack(pady=10)

app.mainloop()