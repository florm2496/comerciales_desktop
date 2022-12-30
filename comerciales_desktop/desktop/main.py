
from tkinter import Tk,NORMAL,Toplevel,DISABLED
from api import get_request,post_request
from ui_styles import *
from functions import start_proccess
import threading
import sys

class UserInformation:
    token = '8e8e1adb57d8ab03c66fc39843fe90a65f938400'
    user = 'admin'

class LoteActual:
    lote_activo = None
    ultimo_lote_finalizado =None
    
class Dashboard:
    window = None
    
class Scrapper:
    start_proccess = True

def prueba():
    data={}
    response=post_request(UserInformation.token,'prueba',data)


def login():
    params={
        'username':username.get(),
        'clave':clave.get(),
          }
    if params['username'] != '' and params['clave'] != '':
        response=get_request('login',params)
        if response['code'] == 200:
        
            if response['logged'] is True:
                
                UserInformation.token = response['token']
                UserInformation.user = username.get()
                open_window()
                
            else:
                show_message('warning','Inicio de sesion',response['mensaje'])
                
        elif response['code'] == 500:
            show_message('error','Error de sistema:avisar al programador',response['mensaje'])
        
    else:
        show_message('error','Usuario o clave vacios','Ingrese correctamente la clave y el usuario')

# def login():
    
#     open_window()



    
def refresh_dashboard():
    response=get_request('getloteactual',{'token':UserInformation.token})
    if response['code'] == 500:
        show_message('error','Error',response['mensaje'])
    else:
        LoteActual.lote_activo = response['lote'] 
        
    response=get_request('getultimolotefinalizado',{'token':UserInformation.token})
    if response['code'] == 500:
        show_message('error','Error',response['mensaje'])
    else:
        LoteActual.ultimo_lote_finalizado=response['lote'] 


def refresh_dashboard2():
    Dashboard.window.destroy()
    open_window()
    
    response=get_request('getloteactual',{'token':UserInformation.token})
    if response['code'] == 500:
        show_message('error','Error',response['mensaje'])
    else:
        LoteActual.lote_activo = response['lote'] 
        
    response=get_request('getultimolotefinalizado',{'token':UserInformation.token})
    if response['code'] == 500:
        show_message('error','Error',response['mensaje'])
    else:
        LoteActual.ultimo_lote_finalizado=response['lote'] 

def call_scrapper():
    if Scrapper.start_proccess == True:
        start_proccess(Scrapper.start_proccess,
                    UserInformation.token,
                    LoteActual.lote_activo)
  
  
def crear_lote():
    response=post_request(UserInformation.token,'crearlote',{'cantidad_expedientes':cant_exp_lote_nuevo.get()})
    if response['code'] == 500:
        show_message('error','Error',response['mensaje'])
    elif response['code'] == 1:
        
        show_message('info','Exito','El lote fue creado')
    elif response['code'] == 0:
        show_message('warning','Creacion cancelada','No se pudo crear el lote porque ya hay uno activo sin terminar')
        response['info_lotes'] 

    refresh_dashboard()

    

def open_window():
    
    refresh_dashboard()
    
    ventana.withdraw()
    Dashboard.window = Toplevel()
    Dashboard.window.geometry('1000x900')
    #Dashboard.window.configure(background='grey')
    Dashboard.window.title(f"USUARIO: {UserInformation.user}")
    #Dashboard.window.resizable(False, False)
    
    
    
    #boton de salir
    get_little_button(Dashboard.window,'Actualizar',refresh_dashboard2,NORMAL,None,'green').grid(row=7,column=0)
    get_little_button(Dashboard.window,'Salir',Dashboard.window.destroy,NORMAL,None,'red').grid(row=7,column=1)
    


    
    #PARTE IZQUIERDA DE LA VENTANA
    get_label_title(Dashboard.window,'PANEL DE CONTROL').grid(row=0,column=0,pady=styles['pady'],padx=styles['padx'])
    
    get_label(Dashboard.window,'Lote en progreso').grid(row=1,column=0,pady=styles['pady'],padx=styles['padx'])


    if LoteActual.lote_activo ==None:
            text = 'No hay lotes en progreso'
            get_label_container(Dashboard.window,text).grid(row=2,column=0,pady=styles['pady'],padx=styles['padx'])
    else:
        numero = LoteActual.lote_activo['num_lote']
        estado = LoteActual.lote_activo['estado']
        get_label_container(Dashboard.window,f'Numero: {numero}').grid(row=2,column=0,pady=styles['pady'],padx=styles['padx'])
        get_label_container(Dashboard.window,f'Estado: {estado}').grid(row=3,column=0,pady=styles['pady'],padx=styles['padx'])
    

    relleno(Dashboard.window).grid(row=4,column=0,pady=styles['pady'],padx=styles['padx'])
    
    get_label(Dashboard.window,'Ultimo lote finalizado').grid(row=5,column=0,pady=styles['pady'],padx=styles['padx'])
    
    # if LoteActual.ultimo_lote_finalizado ==None:
    #     text = 'No hay lotes finalizados aun'
    # else:
    #     ulf = LoteActual.ultimo_lote_finalizado
        
    #     get_label(Dashboard.window,'Ultimo lote finalizado').grid(row=7,column=0,pady=styles['pady'],padx=styles['padx'])
        
    #     ultimo_row = 7
    #     for key,value in ulf.items():
    #         if key != 'id':
    #             print(key,value)
    #             ultimo_row += 1
    #             #contiene el ultimo lote finalizado
    #             get_label(Dashboard.window,key).grid(row=ultimo_row,column=0,pady=styles['pady'],padx=styles['padx'])
    #             get_label(Dashboard.window,value).grid(row=ultimo_row,column=1,pady=styles['pady'],padx=styles['padx'])
            

    if LoteActual.lote_activo is None:
        state= DISABLED
    else:
        state = NORMAL

    def prueba_hilo():
        hilo = threading.Thread(target=call_scrapper)
        hilo.start()

    get_button(Dashboard.window,'Comenzar',prueba_hilo,state,None).grid(row=5,column=0,pady=styles['pady'],padx=styles['padx'])
    
            
    relleno(Dashboard.window).grid(row=6,column=0,pady=styles['pady'],padx=styles['padx'])
    
    
    
    
    
    
    
    
    
    #PARTE DERECHA DE LA VENTANA
    
   
    get_label(Dashboard.window,'Crear un nuevo lote').grid(row=1,column=1,pady=styles['pady'],padx=styles['padx'])
    
    get_label(Dashboard.window,'Cantidad').grid(row=2,column=1,pady=styles['pady'],padx=styles['padx'])
    
    if LoteActual.lote_activo is None:
        state = NORMAL
    else:
        state= DISABLED
        
    
    global cant_exp_lote_nuevo
    cant_exp_lote_nuevo=get_entry(Dashboard.window,None,'normal')
    cant_exp_lote_nuevo.grid(row=3,column=1,pady=styles['pady'],padx=styles['padx'])


    get_label(Dashboard.window,'AÑO 2022').grid(row=4,column=1,pady=styles['pady'],padx=styles['padx'])
    get_button(Dashboard.window,'Crear lote',crear_lote,state,None).grid(row=5,column=1,pady=styles['pady'],padx=styles['padx'])
    
def close_window():
    ventana.destroy()
    
# def login():
#     open_window()

if __name__ == '__main__':
    
    def hilo_interfaz():
        hilo = threading.Thread(target=login())
        hilo.start()
        
       
    ventana = Tk()
    ventana.title("Inicio de sesion")
    ventana.geometry('500x500')
   

    get_label_login(ventana,'Usuario').grid(row=0,column=0,pady=styles['pady'],padx=15)
    username=get_entry_login(ventana,None,'normal')
    username.grid(row=1,column=0,pady=styles['pady'],padx=15)


    get_label_login(ventana,'Clave').grid(row=2,column=0,pady=styles['pady'],padx=15)
    clave=get_entry_login(ventana,None,'normal')
    clave.config(show="*")
    clave.grid(row=3,column=0,pady=styles['pady'],padx=15)



    get_button(ventana,'Ingresar',hilo_interfaz,NORMAL,None).grid(row=7,column=0,pady=styles['pady'],padx=15)



    ventana.mainloop()