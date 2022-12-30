   
from tkinter import Label,Entry,Button,messagebox 

styles = {'button':{'w':15,'bg':'lightblue','pady':5,'padx':20,},
          'button2':{'w':15,'bg':'green','pady':5,'padx':15,},
          'label':{'w':30,'h':10,'pady':5,'padx':20,},
          'label2':{'w':30,'h':10,'pady':5,'padx':20},
          'entry':{'w':30,'h':10,'pady':5,'padx':20},
          'padx':10,
          'pady':10,
          }


font=("Helvetica", 20)
font1=("Helvetica", 25)


def get_label_title(window,text):
    return Label(window,text=text,width=30,font=font1)


def get_label(window,text):
    return Label(window,text=text,width=25,font=font)

def relleno(window):
    return Label(window,text='',width=25)

def get_label_container(window,text):
    return Label(window,text=text,width=20,font=17, borderwidth=1, relief="solid")


def get_label_login(window,text):
    return Label(window,text=text,width=30,font=17)
    
def get_entry(window,textvariable,state):
    return Entry(window,
                 width=20,
                 font=font,
                 state=state,
                 textvariable=textvariable,
                 )
    
def get_entry_login(window,textvariable,state):
    return Entry(window,
                 width=30,
                 font=font,
                 state=state,
                 textvariable=textvariable,
                 )


def get_button(window,text,command,state,image):
    return Button(window,
                  text=text,
                  width=20,
                  background='#00ffff',
                  font=font,
                  command=command,
                  pady=10,
                  state=state,
                  image=image,
                  )
    
    
def get_little_button(window,text,command,state,image,color):
    return Button(window,
                  text=text,
                  width=10,
                  background=color,
                  font=font,
                  command=command,
                  pady=4,
                  state=state,
                  image=image,
                  )

def show_message(_type, title, message):
    
    if _type == 'warning':
        
        messagebox.showwarning(title,message)
        
    if _type == 'error':
        messagebox.showerror(title,message)
        
    if _type == 'info':
        messagebox.showinfo(title,message)
        
