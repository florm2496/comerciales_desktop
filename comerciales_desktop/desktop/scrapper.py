
import datetime as dt
from time import sleep
from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options



#logging.basicConfig( level=logging.DEBUG, filename='example.log')
#logging.basicConfig(level=logging.DEBUG)


#ep='drivers/ubuntu/101'
ep='chromedriver.exe'

class Scraper:

    def __init__(self) -> None:
        
        
        self.url='http://scw.pjn.gov.ar/scw/home.seam'
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")


        self.dv = wb.Chrome(executable_path=ep,chrome_options=self.chrome_options)

    def _scrapper(self,lote,user):
        dv=self.dv
        for i in range(5):
            dv.get(self.url)
            sleep(2)
        
    # def scrapper(self,id_lote,id_user):
    #     lote=Lotes.objects.get(pk=id_lote,usuario__pk=id_user)

    #     año = lote.config.año

    #     dv=self.dv
    #     juris='//*[@id="formPublica:camaraNumAni"]'
    #     exp_path='//*[@id="formPublica:numero"]'
    #     año_path='//*[@id="formPublica:anio"]'
    #     com='//*[@id="formPublica:camaraNumAni"]/option[12]'

    #     id_formpublica='formPublica:numero'

        
    
    #     dv.get(self.url)

    #     j=dv.find_element_by_xpath(com)

    #     #seleccionar jurisdiccion
    #     jurisdiccion=Select(dv.find_element_by_xpath(juris))

    #     jurisdiccion.select_by_visible_text(j.text)

    #     ####################################
    #     #escribir el numero

    #     input_numero=dv.find_element_by_xpath(exp_path)
    #     input_numero.click()

    #     uc=lote.ultimo_chequeado

    #     if uc==0:
    #         lote.ultimo_chequeado=lote.exp_inicio
    #         aux_expendiente = lote.ultimo_chequeado
            
    #     else:
    #         aux_expendiente = lote.ultimo_chequeado + 1
    #         lote.ultimo_chequeado=aux_expendiente
        

    #     lote.save()
    #     input_numero.send_keys(aux_expendiente)
    #     #escribir el año

    #     input_año=dv.find_element_by_xpath(año_path)
    #     input_año.click()
   
    #     input_año.send_keys(año)
    #     #sleep(20)

    #     xpath = '//*[@id="recaptcha-anchor"]/div[1]'

    #     #boton=dv.find_element_by_xpath(xpath).click()
    #     # try:
    #     #WebDriverWait(dv, 5).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    #     return año,aux_expendiente
    
    # def scrapper_revisiones(self,id_lote,id_user,aux_expendiente):

    #     print('scrapping reviews')
    #     lote=Lotes.objects.get(pk=id_lote,usuario__pk=id_user)

    #     año = lote.config.año

    #     dv=self.dv
    #     juris='//*[@id="formPublica:camaraNumAni"]'
    #     exp_path='//*[@id="formPublica:numero"]'
    #     año_path='//*[@id="formPublica:anio"]'
    #     com='//*[@id="formPublica:camaraNumAni"]/option[12]'

    #     id_formpublica='formPublica:numero'

        
    
    #     dv.get(self.url)

    #     j=dv.find_element_by_xpath(com)

    #     #seleccionar jurisdiccion
    #     jurisdiccion=Select(dv.find_element_by_xpath(juris))

    #     jurisdiccion.select_by_visible_text(j.text)

    #     ####################################
    #     #escribir el numero

    #     input_numero=dv.find_element_by_xpath(exp_path)
    #     input_numero.click()

    #     input_numero.send_keys(aux_expendiente)
    #     #escribir el año

    #     input_año=dv.find_element_by_xpath(año_path)
    #     input_año.click()
   
    #     input_año.send_keys(año)

    #     xpath = '//*[@id="recaptcha-anchor"]/div[1]'

    #     return año,aux_expendiente
        

    # def get_content(self):  
    #     print('GETTING CONTENT')
    #     dv=self.dv
    #     stop=False
    #     retries=0
    #     wait=4
    #     no_existente=False
        
    #     while stop == False and retries <= 5 and no_existente==False:
    #         sleep(wait)
    #         try:
     
    #             volver=dv.find_element_by_xpath('//*[@id="expediente:j_idt78"]/div/a')

    #             exp_xpath = '//*[@id="expediente:j_idt87:j_idt88"]/div/div[1]/div/div/div[2]/span'
    #             expediente=dv.find_element_by_xpath(exp_xpath)

    #             dep_xpath= '//*[@id="expediente:j_idt87:detailDependencia"]'
    #             dependencia = dv.find_element_by_xpath(dep_xpath)


    #             carat_xpath='//*[@id="expediente:j_idt87:detailCover"]'
    #             caratula = dv.find_element_by_xpath(carat_xpath)


    #             bodytable_xpath='//*[@id="expediente:action-table"]/tbody'


    #             siguiente = '//*[@id="expediente:j_idt217:j_idt224"]/span'

    #             sleep(3)

    #             flat=True
    #             while flat:

    #                 try:
    #                     #WebDriverWait(dv, 5).until(EC.element_to_be_clickable((By.XPATH, siguiente))).click()

    #                     dv.find_element_by_xpath(siguiente).click()

    #                     sleep(2)

    #                 except Exception as e:
    #                     print(1,e)
    #                     flat=False

    #                     elements = dv.find_elements_by_xpath(bodytable_xpath)

    #                     elements_list=[elm.text for elm in elements]

    #                     info_cleaned=elements_list[0].split('\n')

    #                     nuevo = []

    #                     print('INFO CLEANED',info_cleaned)

    #                     for i in info_cleaned:

    #                         if i != 'Descargar' and i!='Ver':

    #                             numbers = re.findall('[0-9]+', i)

    #                             if '/' in i:

    #                                 if i.count('/') == 1 and len(numbers) > 0:
    #                                     print(i)
    #                                 else:
    #                                     nuevo.append(i)

    #                             else:
                        
    #                                 nuevo.append(i)

    #                     el=8
    #                     filas = [nuevo[i:i+el] for i in range(0, len(nuevo), el)]
                        
    #                     print('FILAS TOTAL',filas)
    #                     #fecha inicio demanda
    #                     try:
    #                         print()
    #                         print('AQUI 1')
    #                         detalle= filas[-1][-1]
    #                         print('AQUI 2',detalle)
    #                         print('FILAS',filas[-1][3])
    #                         if detalle == 'INICIO / DEMANDA':

    #                             if filas[-1][0] == 'Oficina:':
    #                                 fecha=filas[-1][3]
    #                             else:
    #                                 fecha=filas[-1][2]
                                    
    #                             elements=fecha.split('/')

    #                             print('AQUI 2.5',detalle)
    #                             print('fecha:',fecha)
    #                             print(elements)

    #                             dia = elements[0]
    #                             mes=elements[1]
    #                             año=elements[2]
    #                             print('AQUI 3',detalle)
    #                             if len(dia) == 2:
    #                                 if dia[0] == 0:
    #                                     dia = dia[1]

    #                             if len(mes) == 2:
    #                                 if mes[0] == 0:
    #                                     mes = mes[1]
    #                             print('AQUI 4',detalle)

                                        
    #                             fechaid=dt.date(int(año),int(mes),int(dia))
                                

    #                         else:
    #                             fechaid = None

                                
    #                     except Exception as e:
                 
    #                         print(2,e)
                
    #             response={'expediente':expediente.get_attribute("innerHTML"),'dependencia':dependencia.get_attribute("innerHTML"),'caratula':caratula.get_attribute("innerHTML"),'fechaid':fechaid}
                
    #             stop=True
            
    #             print('ENCONTRO LOS DATOS')
    #         except Exception as e:


    #             print(4,e)
    #             print('REINTENTO',retries)
    #             retries +=1

    #             response={'ERROR': str(e)}
                
        
    #             try:
    #                 texto='Expediente inexistente o no disponible para su consulta pública'
    #                 xpath='//*[@id="messages"]/div/ul/li/span'
    #                 span_exp_inexistente=dv.find_element_by_xpath(xpath)
    #                 content=span_exp_inexistente.get_attribute("innerHTML")

    #                 if content == texto:

    #                     no_existente=True

    #             except Exception as e:
    #                 print(3,e)


    #             response['NO_EXISTENTE']=no_existente

                
    #     return response
        