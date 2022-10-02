from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from telegraph import Telegraph, upload_file
import os.path
import time
from tkinter import scrolledtext
import os
import pyperclip
import webbrowser

global title_root
global folder

def save_last_data():
    last_data_f = open("lastdata.txt", "w")
    last_data = usernamew.get() + "\n"
    last_data = last_data + usernamesw.get() + "\n"
    last_data = last_data + urlw.get() + "\n"
    last_data = last_data + "0" + "\n"
    last_data = last_data + folder + "\n"
    last_data = last_data + titlew.get()
    last_data_f.write(last_data)

def clicked_ex():
    messagebox.showinfo('Заголовок', 'Текст')
    messagebox.showwarning('Заголовок', 'Текст')
    messagebox.showerror('Заголовок', 'Текст')
    res = messagebox.askquestion('Заголовок', 'Текст')
    res = messagebox.askyesno('Заголовок', 'Текст')
    res = messagebox.askyesnocancel('Заголовок', 'Текст')
    res = messagebox.askokcancel('Заголовок', 'Текст')
    res = messagebox.askretrycancel('Заголовок', 'Текст')
    print()

def title_gen(text):
    window.title("Telegra.ph gen - " + text)

def save_token(tlph):
    if os.path.isfile('token.txt'):
        pass
    else:
        token = tlph.get_access_token()
        open("token.txt", "w").write(token)

def select_folder():
    global folder
    folder = str(filedialog.askdirectory())
    folderw.configure(text=folder)
    btnok['state'] = 'normal'
    title_gen("Готово")

def main_start():
    btnok['state'] = 'disabled'
    title_gen("Иницилизация")
    save_last_data()
    if combotype.get() == "mix":
        type_file = ["png", "jpg", "jpeg", "gif"]
    else:
        type_file = [combotype.get()]
    username = usernamew.get()
    usernames = usernamesw.get()
    url_credit = urlw.get()
    if os.path.isfile(folder+'/info.txt'):
        info = open(folder+'/info.txt', "r").read()
    else:
        info = ""
    title = titlew.get()
    title_gen("Генерация файлов")
    list_file = os.listdir(path=folder)
    list_file.sort()
    list_file_ready = []
    for ii in list_file:
        if ii.split(".")[-1] in type_file:
            list_file_ready.append(folder+"/"+ii)
    title_gen("Загрузка файлов "+str(len(list_file_ready)))
    list_url_ready = []
    count = 1
    for tt in list_file_ready:
        print("Загрузка файла "+str(count)+"/"+str(len(list_file_ready)))
        list_url_ready.append("https://te.legra.ph"+str(upload_file(tt)[0]))
        count += 1
    title_gen("Генерация страницы")
    htmlc = "<p>" + info.replace("\n", "<br/>") + "</p>"
    for nn in list_url_ready:
        add_page = '''<img src="'''+nn+'''" alt="Page">'''
        htmlc += add_page
    title_gen("Публикация страницы")
    if os.path.isfile('token.txt'):
        telegraph = Telegraph(access_token=open("token.txt", "r").read())
    else:
        telegraph = Telegraph()
    telegraph.create_account(short_name=usernames, author_name=username, author_url=url_credit)
    save_token(telegraph)
    response = telegraph.create_page(
        title,
        html_content=htmlc
    )
    link = "https://telegra.ph/{}".format(response['path'])
    open(folder+"/link.txt", "w").write(link)
    title_gen("Публикация завершена")
    res = messagebox.askquestion('Внимание', 'Cкопировать ссылку?')
    if res == False:
        pyperclip.copy(link)

def open_author():
    webbrowser.open("https://github.com/Hell13Cat/telegra.ph-manga-gener")



window = Tk()
window.title("Telegra.ph gen - Ожидание ввода")
window.geometry('450x175')

lbl = Label(window, text="Username")
lbl.grid(column=0, row=1)
usernamew = Entry(window, width=50)
usernamew.grid(column=1, row=1)

lbl = Label(window, text="Username short")
lbl.grid(column=0, row=0)
usernamesw = Entry(window, width=50)
usernamesw.grid(column=1, row=0)

lbl = Label(window, text="URL")
lbl.grid(column=0, row=2)
urlw = Entry(window, width=50)
urlw.grid(column=1, row=2)

lbl = Label(window, text="Заголовок")
lbl.grid(column=0, row=3)
titlew = Entry(window, width=50)
titlew.grid(column=1, row=3)

folderw = Label(window, width=50, text="Не выбрано")
folderw.grid(column=1, row=6)
btnf = Button(window, text="Выбрать папку", command=select_folder)
btnf.grid(column=0, row=6)

lbl = Label(window, text="Тип файла")
lbl.grid(column=0, row=5)
combotype = Combobox(window, state="readonly", width=50)
combotype['values'] = ("mix", "png", "jpg", "jpeg", "gif")
combotype.current(0)
combotype.grid(column=1, row=5)

btnok = Button(window, text="Начать", command=main_start, state='disabled')
btnok.grid(column=0, row=7)
btnok = Button(window, text="Telegra.ph gen v0.1 beta", command=open_author)
btnok.grid(column=1, row=7)

if os.path.isfile('lastdata.txt'):
    last_data = open("lastdata.txt", "r").readlines()
    usernamew.insert(0, last_data[0].replace("\n", ""))
    usernamesw.insert(0, last_data[1].replace("\n", ""))
    urlw.insert(0, last_data[2].replace("\n", ""))
    combotype.current(int(last_data[3].replace("\n", "")))
    folder = last_data[4].replace("\n", "")
    folderw.configure(text=folder)
    btnok['state'] = 'normal'
    titlew.insert(0, last_data[5].replace("\n", ""))

window.mainloop()