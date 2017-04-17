from tkinter import *


class AuthWindow():
    def __init__(self):
        pass

    def Signup(self):
        global roots

        roots = Tk()
        roots.title('Signup')
        intruction = Label(roots,
                           text='Please Enter new Credidentials\n')
        intruction.grid(row=0, column=0, sticky=E)
        name_label = Label(roots, text='New Username: ')
        pwd_label = Label(roots, text='New Password: ')
        pwd_re_label = Label(roots, text='Re-enter Password: ')
        name_label.grid(row=1, column=0, sticky=W)
        pwd_label.grid(row=2, column=0, sticky=W)
        pwd_re_label.grid(row=3, column=0, sticky=W)

        name_entry = Entry(roots)
        pwd_entry = Entry(roots, show='*')
        pwd_re_entry = Entry(roots, show='*')
        name_entry.grid(row=1, column=1)
        pwd_entry.grid(row=2, column=1)
        pwd_re_entry.grid(row=2, column=1)

        signupButton = Button(roots, text='Signup')
        signupButton.grid(columnspan=2, sticky=W)
        roots.mainloop()



