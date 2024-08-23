import pyautogui as pg
import time
import subprocess
import os
import psutil
from datetime import datetime, timedelta
from pyWinActivate import win_activate, win_wait_active, check_win_exist

# MEUS ARQUIVOS #
import config
from user_model import usuario
from banco import get_id, extract_full_name, extract_name, login_sige, get_parameters

sige_path = r"\\servidor\sigewin\Arquivos de Programas\SIGEWin\sige.exe"
asstec_path = r"\\servidor\sigewin\Arquivos de Programas\SIGEWin\TemposAsstec.exe"

cwd_sige = os.path.dirname(sige_path)  # Pra trabalhar na pasta do sige, sem isso da erro devido ao db
cwd_asstec = os.path.dirname(asstec_path)

def open_sige(user,password):
    window_exist = check_win_exist("SIGEWin - Sistema Integrado de Gestão Empresarial")
    if window_exist:
        return True # SE JA TIVER ABERTO APENAS VOLTA
    
    else: 
        subprocess.Popen([sige_path], cwd=cwd_sige)  # Abrir o executável
        for proc in psutil.process_iter(['name']): # Verifica todos os processos do PC
            if proc.info['name'] == 'sige.exe': # Caso tenha o processo
                menu = True
                while menu:
                    try:
                        sige = pg.locateOnScreen(r'assets\sige_password.png',confidence=0.8,)
                        pg.move(sige)
                        pg.click(sige)
                        break
                    except:
                        window_exist = check_win_exist("SIGEWin - Sistema Integrado de Gestão Empresarial")
                win_wait_active("SIGEWin - Senha")
                if user == "":
                    return True
                pg.typewrite(user)
                pg.press('tab')
                pg.typewrite(password)
                pg.hotkey('alt','o')
                return True
    return False

def open_time():
    window_exist = check_win_exist("SIGEWin - Entrada de Tempos")
    if window_exist:
        config.flag_first = False
        win_activate(window_title="SIGEWin - Entrada de Tempos",partial_match=True) 
        return
    
    subprocess.Popen([asstec_path], cwd=cwd_asstec)  # Abrir o executável
    config.flag_first = True
    login_time()    

def close_time():
    pg.press('alt')
    pg.press('a')
    pg.press('s')
    return

def get_time(user):
    
    if config.flag_first:
        tab_number = 1
        config.flag_first = False
    else:
        tab_number = 4
        
    time.sleep(2)
    pg.hotkey('alt','v')
    pg.press('tab',presses=tab_number)
    pg.write("rafael")
    pg.press('tab')
    pg.write("r1990")
    pg.press('enter')
    
    while win_wait_active(win_to_wait="Tempos Lidos - SIGEWin"):
        if check_win_exist("Tempos Lidos - SIGEWin"): # Se aparecer sai do loop e coloca credencial
            break
        
    pg.hotkey('alt',' ','x')
    id = get_id(user)
    full_name = extract_full_name(id)
    time.sleep(500/1000)
    operador = pg.locateOnScreen(r'assets\operador.png',confidence=0.3,region=(500,500,1800,900))
    pg.move(operador)
    pg.click(operador)
    time.sleep(500/1000)
    pg.typewrite(full_name)
    pg.press('enter')
    pg.hotkey('alt','a')
    
def look_workman(asstec_number):
    menu = True
    while menu:
        try:
            sige = pg.locateOnScreen(r'utils\menu_sige.png',confidence=0.8,)
            pg.move(sige)
            pg.click(sige)
            break
        except:
            time.sleep(100/1000)
                
    pg.press('alt')
    pg.press(' ')
    pg.press('x')
    pg.press('alt')
    pg.press('v')
    pg.press('a')
    time.sleep(2)
    pg.write('01012001')
    pg.press('tab')
    pg.write('01012050')
    pg.press('tab')
    pg.press('enter')
    pg.press('tab',presses=3)
    pg.write(asstec_number)
    pg.press('tab',presses=3)
    pg.press('right',presses=4)
    return

def login_time():
    # Esperar aparecer a tela de login
    waiting = True
    while waiting:
        try:
            operador = pg.locateOnScreen(r'assets\database.png',confidence=0.8)
            print(operador)
            pg.move(operador)
            pg.click(operador)
            waiting= False
        except:
            time.sleep(200/1000)
    login = "sige"
    pg.write(login)
    pg.press('tab', presses=3)
    pg.write(login)
    pg.press('enter')

# FUNCAO Q ENTRA NO TEMPO COM OS DADOS COLETADOS
def send_time_info(key: str, my_time: str, date: str):

    if config.flag_first:
        tab_number = 1
        config.flag_first = False
    else:
        tab_number = 4
        
    win_wait_active("SIGEWin - Entrada de Tempos")      
    pg.write(usuario.asstec)   
    pg.press('tab')
    pg.write(usuario.etapa)
    pg.press('tab', presses=2)
    pg.write(usuario.workstation)
    pg.press('tab')
    pg.write(usuario.id)
    pg.hotkey('ctrl','h')
    pg.press('tab', presses=tab_number)
    pg.write(config.sige_default_user)
    pg.press('tab')
    pg.write(config.sige_default_password)
    pg.press('enter')
    pg.write(date)
    pg.press('tab')
    pg.write(my_time)
    pg.press(key)
    pg.hotkey('alt','o')
    
# FUNCAO QUE ORGANIZA AS INFORMAÇÕES COLETADAS NA ENTRADA DE TEMPO
def receive_sige_keys(status: str):
    
    if status == "entrou":
        send_time_info("F2",config.time,config.init_date)
        
    elif status == "saiu":
        send_time_info("F3",config.time,config.init_date)
        
    elif status == "manha": # MANHA COMPLETA 7:00/11:50
        send_time_info("F2",config.time,config.init_date) #7
        pg.press('enter')
        my_time = edit_time("11:50")
        send_time_info("F3",my_time,config.init_date)
        
    elif status == "tarde": # TARDE COMPLETA 12:50/16:48
        my_time = edit_time("12:50")
        send_time_info("F2",my_time,config.init_date)
        pg.press('enter')
        send_time_info("F3",config.f_time,config.init_date)
        
    elif status == "dia_completo" or status == "varios_dias": # 07:00/11:50/12:50/16:48
        send_time_info("F2",config.time,config.init_date)
        pg.press('enter')
        my_time = edit_time("11:50")
        send_time_info("F3",my_time,config.init_date)
        pg.press('enter')
        my_time = edit_time("12:50")
        send_time_info("F2",my_time,config.init_date)
        pg.press('enter')
        send_time_info("F3",config.f_time,config.init_date)

    window_exist = check_win_exist("Information") # Verifica se deu certo
    if window_exist:
        pg.press('enter')
        close_time()
        return True
    else:
        return False
 
################# OUTRAS FUNÇÕES DE CONTROLE #################

def get_user(username):
    config.logged_in_user = username
    return username

def get_login_info():
    usuario.name = extract_name(usuario.id) # Pega o ID e procura o primeiro nome
    get_user(usuario.name)
    config.sige_user, config.sige_password = login_sige(usuario.id)
    usuario.asstec, usuario.etapa, usuario.status, usuario.I_time, usuario.F_time = get_parameters(usuario.id)

def user_parameters():
    usuario.id = get_id(usuario.name) # Pega o ID e procura o primeiro nome
    usuario.asstec, usuario.etapa, usuario.status, usuario.I_time, usuario.F_time = get_parameters(usuario.id)

def order_infos(status: str): # Organizar o radiogroup pra mandar a informação certa
    # sE ENTROU OU SAIU MANDA HORA DA INTERFACE E VAZIO
    if status == "entrou" or status == "saiu":
        return config.time, None
    # SE MANHA MANDA HORARIO DO USUARIO E 11:50
    elif status == "manha":
        return usuario.I_time, "11:50" # retorna 07:00 e 11:50
    # SE TARDE MANDA 12:50 E HORARIO FINAL USUARIO
    elif status == "tarde":
        return "12:50", usuario.F_time
    # MANDA EXPEDIENTE INTEIRO DO USUARIO
    elif status == "dia_completo":
        if config.extra_time == True: # SE FOR HORA EXTRA
            if usuario.F_time <= get_current_time(): # HORA DO USER MENOR Q HORA ATUAL
                config.f_time = get_current_time() # F_TIME = HORA ATUAL
        else:
            config.f_time = usuario.F_time
        return usuario.I_time, config.f_time
    elif status == "varios_dias":
        return usuario.I_time, usuario.F_time

def edit_time(my_time):
    if my_time == None: 
        return
    
    my_time = str(my_time) # transforma em string
    
    my_time = my_time.replace(":","") # tira os :
    if len(my_time) > 5: # Se for data com segundos (data do usuario)
        return my_time

    now = datetime.now()
    seconds = now.strftime("%S")
    return my_time + seconds # Adiciona segundos ao tempo
    
def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M")

def get_current_date():
    now = datetime.now()
    return now.strftime("%d-%m-%Y")

def format_time(my_time): #TODO MELHORAR ESSA LOGICA, MUITAS POSSIVEIS FALHAS E ERRO
    cleaned = ''.join(char for char in my_time if char.isdigit() or char == ':')
    # Garantir que o texto esteja no formato HH:MM
    if len(cleaned) > 2 and cleaned[2] != ':':
        cleaned = cleaned[:2] + ':' + cleaned[2:]

    if len(cleaned) > 5:
        cleaned = cleaned[:5]
    
    if len(cleaned) == 5:
        hour = int(cleaned[:2]) # pega os 2 primeiros caracters
        minute = int(cleaned[3:]) # seleciona a partir do indice 3 ate o final

    print(hour)
    print(minute)
    if hour > 23:
        hour = 0
    if minute > 59:
        minute = 0
        
    formatted_time = f'{hour:02}:{minute:02}'
    return formatted_time

def process_multiple_days(initial_date_str, final_date_str):
    # Transforma a string recebida em datas
    initial_date = datetime.strptime(initial_date_str, '%d-%m-%Y') 
    final_date = datetime.strptime(final_date_str, '%d-%m-%Y')
    
    current_date = initial_date

    while current_date <= final_date:
        if current_date.weekday() not in [5,6]: #Se for dia util ele entra
            config.init_date = current_date.strftime("%d-%m-%Y")
            receive_sige_keys("varios_dias")
        current_date += timedelta(days=1) # Aumenta um dia
    return



def verify_request_to_join():
    return

def main():
    
    if open_sige(): # Esperar o SIGEWin abrir
        print("SIGEWin está aberto.")
        user = get_user()
        if user:
            print(user)
            pg.write(user)
            pg.press('tab')   
        else:
            print("Nenhum usuario logado")
        # pg.press('enter')
    else:
        print("O SIGEWin não conseguiu abrir dentro do tempo limite.")


        
if __name__ == "__main__":
    main()