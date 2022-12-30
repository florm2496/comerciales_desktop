from lib2to3.pgen2 import token
from scrapper import Scraper
from api import post_request ,get_request
import datetime as dt
from difflib import SequenceMatcher as SM
from distutils.command import config
from time import sleep
from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import Select
import re
from datetime import datetime
import json
import threading


'''
uc: ultimo expediente chequeado , se haya guardado o no
cge: cantidad de expedientes guardados
'''

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

class Scraper:

    def __init__(self) -> None:
        
        self.chromedriver_path='chromedriver.exe'
        self.url='http://scw.pjn.gov.ar/scw/home.seam'
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


        self.dv = wb.Chrome(executable_path=self.chromedriver_path,chrome_options=self.chrome_options)

    def _scrapper(self,id_lote: int,token: str):
        
        lote=get_info_lote(id_lote,token)


        config = get_config(token)
        año = config['año']

        dv=self.dv
        juris='//*[@id="formPublica:camaraNumAni"]'
        exp_path='//*[@id="formPublica:numero"]'
        año_path='//*[@id="formPublica:anio"]'
        com='//*[@id="formPublica:camaraNumAni"]/option[12]'

        id_formpublica='formPublica:numero'

        
    
        dv.get(self.url)

        j=dv.find_element('xpath',com)

        #seleccionar jurisdiccion
        jurisdiccion=Select(dv.find_element('xpath',juris))

        jurisdiccion.select_by_visible_text(j.text)


        input_numero=dv.find_element('xpath',exp_path)
        input_numero.click()

        uc=lote['ultimo_chequeado']

        if uc==0:
            aux_expendiente = lote['exp_inicio']
            data = {'token':token,'lote':lote['id'],'ultimo_chequeado':aux_expendiente}
            
        else:
            aux_expendiente = lote['ultimo_chequeado'] + 1
            
            data = {'token':token,'lote':lote['id'],'ultimo_chequeado':aux_expendiente}
        
        actualizar_lote(data=data)

        input_numero.send_keys(aux_expendiente)
    
        #escribir el año

        input_año=dv.find_element('xpath',año_path)
        input_año.click()
        input_año.send_keys(año)
        sleep(4)
        xpath = '//*[@id="recaptcha-anchor"]/div[1]'


        return año,aux_expendiente


    def _get_content(self):
        dv=self.dv
        stop=False
        retries=0
        no_existente=False
        
        while stop == False and retries <= 10 and no_existente==False:
    
            try:
                
                sleep(1)
     
                volver=dv.find_element('xpath','//*[@id="expediente:j_idt78"]/div/a')


                #expediente
                exp_xpath = '//*[@id="expediente:j_idt90:j_idt91"]/div/div[1]/div/div/div[2]/span'
                
                
                expediente=dv.find_element('xpath',exp_xpath)
                
                
                #expediente
                dep_xpath= '//*[@id="expediente:j_idt90:detailDependencia"]'
                dependencia = dv.find_element('xpath',dep_xpath)


                #caratula
                carat_xpath='//*[@id="expediente:j_idt90:detailCover"]'
                caratula = dv.find_element('xpath',carat_xpath)


                bodytable_xpath='//*[@id="expediente:action-table"]/tbody'


                siguiente = '//*[@id="expediente:j_idt220:j_idt227"]/span'
                
                avanza=True
                while avanza:

                    try:
                        
                        #WebDriverWait(dv, 5).until(EC.element_to_be_clickable((By.XPATH, siguiente))).click()

                        dv.find_element('xpath',siguiente).click()

                        sleep(1)

                    except Exception as e:
                        
                        avanza=False

                        elements = dv.find_elements('xpath',bodytable_xpath)

                        elements_list=[elm.text for elm in elements]

                        info_cleaned=elements_list[0].split('\n')

                        nuevo = []

                        for i in info_cleaned:

                            if i != 'Descargar' and i!='Ver':

                                numbers = re.findall('[0-9]+', i)

                                if '/' in i:

                                    if i.count('/') == 1 and len(numbers) > 0:
                                        pass
                                    else:
                                        nuevo.append(i)

                                else:
                        
                                    nuevo.append(i)

                        el=8
                        filas = [nuevo[i:i+el] for i in range(0, len(nuevo), el)]
                        
 
                        #fecha inicio demanda
                        try:

                            detalle= filas[-1][-1]

                            if detalle == 'INICIO / DEMANDA':

                                if filas[-1][0] == 'Oficina:':
                                    fecha=filas[-1][3]
                                else:
                                    fecha=filas[-1][2]
                                    
                                elements=fecha.split('/')

                                

                                dia = elements[0]
                                mes=elements[1]
                                año=elements[2]
                                
                                if len(dia) == 2:
                                    if dia[0] == 0:
                                        dia = dia[1]

                                if len(mes) == 2:
                                    if mes[0] == 0:
                                        mes = mes[1]
                                

                                        
                                fechaid=dt.date(int(año),int(mes),int(dia))
                                

                            else:
                                fechaid = None

                                
                        except Exception as e:
                            pass
                 
                            
                
                response={'expediente':expediente.get_attribute("innerHTML"),
                          'dependencia':dependencia.get_attribute("innerHTML"),
                          'caratula':caratula.get_attribute("innerHTML"),
                          'fechaid':fechaid}
                
                stop=True
            
                
                
            except Exception as e:
                response={'ERROR': str(e)}
                
        
                try:
                    texto='Expediente inexistente o no disponible para su consulta pública'
                    xpath='//*[@id="messages"]/div/ul/li/span'
                    span_exp_inexistente=dv.find_element('xpath',xpath)
                    content=span_exp_inexistente.get_attribute("innerHTML")

                    if content == texto:

                        no_existente=True

                except Exception as e:
                    pass
                    
                    
                    


                
                
                
                response['NO_EXISTENTE']=no_existente

            retries +=1
        
        return response
        
    

        
    def process_data(self,dependencia,caratula):

        dep_lista =  dependencia.split('-')

        datos_dependencia=[]

        for i,element in enumerate(dep_lista):

            result=re.search(r'\d', element)

            if result is not None:
                pos = result.span()
                pos_in=pos[0]
                pos_f=int(pos[1]) + 1
                value=element[int(pos_in):pos_f]

            elif 'CAMARA COMERCIAL ' in element and i == 0:
                value = 'CC'

            else:
                value=element
            datos_dependencia.append(str(value))

        if 'C/' in caratula:

            caratula_lista=caratula.split('C/')
            actor=caratula_lista[0]

            caratula_lista2=caratula_lista[1].split('S/')

        elif 'c/' in caratula:
            caratula_lista=caratula.split('c/')

            actor=caratula_lista[0]

            caratula_lista2=caratula_lista[1].split('s/')

    
        demandado = caratula_lista2[0]

        objeto = caratula_lista2[1]

        datos_caratula= {'actor':actor,'demandado':demandado,'objeto':objeto}
        juzgado=datos_dependencia[0]
        secretaria=datos_dependencia[1]
        
    
        return actor,demandado,objeto,juzgado,secretaria


    def save_data(self,expediente,caratula,actor,demandado,objeto,juzgado,secretaria,fecha_id,año,id_lote,token):
        
        data ={ 'caratula':caratula,
                'actor':actor,
                'juzgado':juzgado,
                'objeto':objeto,
                'expediente':expediente,
                'demandado':demandado,
                'fecha_inicio_demanda':str(fecha_id),
                'fecha':str(datetime.now()),
                'secretaria':secretaria,
                'año':año,
                'lote':id_lote,
                'token':token,
                }
        
        crear_juicio(
            data = data
        )
        
        



def cambiar_estado_lote(nuevo_estado,id_user,token):
    data = {'estado':nuevo_estado,'id_user':id_user}
    post_request(token,'cambiarestadolote',data)
  
        
def actualizar_lote(data):
    post_request(data['token'],'actualizarlote',data)


def crear_juicio(data):
    post_request(data['token'],'crearjuicio',data)

    

def get_info_lote(id,token):
    params = {'id':id,'token':token}
    response = get_request('getloteactual',params)
    return response['lote']

def get_ultimo_lote_finalizado(id,token):
    params = {'id':id,'token':token}
    response = get_request('getultimolotefinalizado',params)
    return response['lote']

def get_config(token: str):
    response = get_request('getconfigactual',params={'token':token})
    return response['info']

def start_proccess(aux,user_token,id_lote_activo):
    proccess=Scraper()
    
    
    global token
    token = user_token
    
    #obtener info del lote actual
    lote_activo = get_info_lote(id_lote_activo,user_token)
    
    
    
    ultimo_chequeado=lote_activo['ultimo_chequeado']
    

    #se calculan ciclos que faltan para terminar el lote
    if  ultimo_chequeado == 0:
        ciclos=lote_activo['cant_expedientes']
    else:     
        ciclos = lote_activo['exp_fin'] - lote_activo['ultimo_chequeado']
    
    #se cambia el estado de lote en comienzo a lote en progreso 
    
    
    
    
    
    if lote_activo['estado'] == 'CREADO':
        data = {'token':user_token,'lote':lote_activo['id'],'activar':True}
        actualizar_lote(data=data)

    for ciclo in range(ciclos):
        

        año,aux_expendiente=proccess._scrapper(lote_activo['id'],token,)
        
        
        
        actualizar_lote(data={'token':user_token,
                              'lote':lote_activo['id'],
                              'num_ciclo':lote_activo['num_ciclo']+1,})
        
        
        content=proccess._get_content()
        
        
        
        try:
            
            lote_activo = get_info_lote(id_lote_activo,user_token)
            expediente,dependencia,caratula,fecha_id=content.values()
            actor,demandado,objeto,juzgado,secretaria=proccess.process_data(dependencia,caratula)
            
            
            proccess.save_data(expediente,caratula,actor,demandado,objeto,juzgado,secretaria,fecha_id,año,lote_activo['id'],token)
            
            
            cge = lote_activo['CGE'] + 1
            

            guardados=lote_activo['guardados']
          
            if len(guardados) == 0:
                guardados=f'{aux_expendiente}'
            else:
                guardados=f'{guardados},{aux_expendiente}'
                
            data = {'CGE': cge,'guardados':guardados,'token':token,'lote':lote_activo['id']}

            
            actualizar_lote(data=data)

        except Exception as exp:

            
            

            
            data={'lote':lote_activo['id'],
                  'expediente': aux_expendiente,
                  'ano_juicio':año,'error_type':type(exp),
                  'error_mens':str(exp),
                  'fecha_ejecucion':str(dt.date.today()),
                  'recuperacion':'NO'}
            
            lote_activo = get_info_lote(id_lote_activo,user_token)

            key='NO_EXISTENTE'


            if key in content and content[key]==True:
                
                no_existentes = lote_activo['no_existentes']
                if len(no_existentes) == 0:
                    
                    no_existentes=f'{aux_expendiente}'
 
                else:
                    no_existentes=f'{no_existentes},{aux_expendiente}'
                    
                data = {'no_existentes':no_existentes,
                            'token':token,
                            'lote':lote_activo['id'],
                            'CNE':lote_activo['CNE']+1}
    
                actualizar_lote(data=data)
                
            else:
                
                lote_activo = get_info_lote(id_lote_activo,user_token)
                no_guardados = lote_activo['no_guardados'] 
                
                if len(no_guardados) == 0:
                    no_guardados=f'{aux_expendiente}'
                else:
                    no_guardados=f'{no_guardados},{aux_expendiente}'
                
                data = {'no_guardados':no_guardados,
                            'token':token,
                            'lote':lote_activo['id'],
                            'CNG':lote_activo['CNG']+1
                            }
                
                actualizar_lote(data=data)
                
                
        
    lote_activo = get_info_lote(id_lote_activo,user_token)

    if lote_activo['CNG'] == 0:
        estado = 'FINALIZADO'
            
    elif lote_activo['CNG'] != 0:
        estado = 'REVISION_PENDIENTE'
        
    #fecha_finalizacion= dt.datetime.now()
    
    data = {'finalizar':True,
            'estado':estado,
            'lote':lote_activo['id'],
            'token':token}
    
    actualizar_lote(data=data)
    
    instance=Scraper()
    instance.dv.close()

