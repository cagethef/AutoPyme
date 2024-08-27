import pyautogui as pg
import time
import subprocess
import os
import psutil
from datetime import datetime, timedelta
from pyWinActivate import win_activate, win_wait_active, check_win_exist

# MEUS ARQUIVOS #
import parameters
from user_model import usuario
from banco import get_id, extract_full_name, extract_first_name, parameters_db_login_sige, get_parameters

sige_path = r"\\servidor\sigewin\Arquivos de Programas\SIGEWin\sige.exe"
asstec_path = r"\\servidor\sigewin\Arquivos de Programas\SIGEWin\TemposAsstec.exe"

cwd_sige = os.path.dirname(sige_path)  # Pra trabalhar na pasta do sige, sem isso da erro devido ao db
cwd_asstec = os.path.dirname(asstec_path)

def open_sige(user: str,password: str) -> bool:
    """ Verifica se o sige esta aberto e abre caso necessário.
        Se tiver usuario logado no app ele coloca o usuario e senha, se não, ele deixa em branco.
    """
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
    """ Abre a entrada de tempos se não tiver aberta. """
    window_exist = check_win_exist("SIGEWin - Entrada de Tempos")
    if window_exist:
        parameters.is_already_open = False
        win_activate(window_title="SIGEWin - Entrada de Tempos",partial_match=True) 
        return
    
    subprocess.Popen([asstec_path], cwd=cwd_asstec)  # Abrir o executável
    parameters.is_already_open = True
    login_time_db_sige()    

def close_time():
    pg.press('alt')
    pg.press('a')
    pg.press('s')
    return

def verify_my_time(user: str):
    """ Verifica o tempo do usuario. """
    if parameters.is_already_open:
        tab_number = 1
        parameters.is_already_open = False
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
    
def open_workman(asstec_number: str):
    """ Abre a aba de mão de obra do sige. """
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

def login_time_db_sige():
    """ Faz login no database da entrada de tempos."""
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

def send_time_info(key: str, my_time: str, date: str):
    """ Entra no tempo com os dados coletados. """

    if parameters.is_already_open:
        tab_number = 1
        parameters.is_already_open = False
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
    pg.write(parameters.sige_default_user)
    pg.press('tab')
    pg.write(parameters.sige_default_password)
    pg.press('enter')
    pg.write(date)
    pg.press('tab')
    pg.write(my_time)
    pg.press(key)
    pg.hotkey('alt','o')
    
def receive_sige_keys(status: str) -> bool:
    """ Verifica o status para definir os horarios e se precisa entrar/sair. """
    if status == "entrou":
        send_time_info("F2",parameters.start_time,parameters.start_date)
        parameters.stop_join_time = True
        
    elif status == "saiu":
        send_time_info("F3",parameters.start_time,parameters.start_date)
        parameters.stop_join_time = True
        
    elif status == "manha": # MANHA COMPLETA 7:00/11:50
        send_time_info("F2",parameters.start_time,parameters.start_date) #7
        pg.press('enter')
        my_time = edit_time("11:50")
        send_time_info("F3",my_time,parameters.start_date)
        parameters.stop_join_time = True
        
    elif status == "tarde": # TARDE COMPLETA 12:50/16:48
        my_time = edit_time("12:50")
        send_time_info("F2",my_time,parameters.start_date)
        pg.press('enter')
        send_time_info("F3",parameters.f_time,parameters.start_date)
        parameters.stop_join_time = True
        
    elif status == "dia_completo": # 07:00/11:50/12:50/16:48
        send_time_info("F2",parameters.start_time,parameters.start_date)
        pg.press('enter')
        my_time = edit_time("11:50")
        send_time_info("F3",my_time,parameters.start_date)
        pg.press('enter')
        my_time = edit_time("12:50")
        send_time_info("F2",my_time,parameters.start_date)
        pg.press('enter')
        send_time_info("F3",parameters.f_time,parameters.start_date)
        parameters.stop_join_time = True
        
    elif status == "varios_dias":
        send_time_info("F2",parameters.start_time,parameters.start_date)
        pg.press('enter')
        my_time = edit_time("11:50")
        send_time_info("F3",my_time,parameters.start_date)
        pg.press('enter')
        my_time = edit_time("12:50")
        send_time_info("F2",my_time,parameters.start_date)
        pg.press('enter')
        send_time_info("F3",parameters.f_time,parameters.start_date)
    elif status == "fechar":
        parameters.stop_join_time = True
        close_time()
        parameters.stop_join_time = False
        return True
    window_exist = check_win_exist("Information") # Verifica se deu certo
    if window_exist:
        pg.press('enter')
        if parameters.stop_join_time:
            close_time()
        parameters.stop_join_time = False
        return True
    else:
        return False
 
################# OUTRAS FUNÇÕES DE CONTROLE #################

def get_login_info():
    """ Pega os parametros do usuario. """
    usuario.name = extract_first_name(usuario.id) # Pega o ID e procura o primeiro nome
    parameters.user_first_name = usuario.name
    parameters.sige_username, parameters.sige_password = parameters_db_login_sige(usuario.id)
    usuario.asstec, usuario.etapa, usuario.status, usuario.I_time, usuario.F_time = get_parameters(usuario.id)

def user_parameters():
    """ Com base no id retorna os parametros do usuario. """
    usuario.id = get_id(usuario.name) # Pega o ID e procura o primeiro nome
    usuario.asstec, usuario.etapa, usuario.status, usuario.I_time, usuario.F_time = get_parameters(usuario.id)

def order_infos(status: str) -> str:
    """ Organizar o radiogroup pra mandar a informação certa. """
    # sE ENTROU OU SAIU MANDA HORA DA INTERFACE E VAZIO
    if status == "entrou" or status == "saiu":
        return parameters.start_time, None
    # SE MANHA MANDA HORARIO DO USUARIO E 11:50
    elif status == "manha":
        return usuario.I_time, "11:50" # retorna 07:00 e 11:50
    # SE TARDE MANDA 12:50 E HORARIO FINAL USUARIO
    elif status == "tarde":
        return "12:50", usuario.F_time
    # MANDA EXPEDIENTE INTEIRO DO USUARIO
    elif status == "dia_completo":
        if parameters.extra_time == True: # SE FOR HORA EXTRA
            if usuario.F_time <= get_current_time(): # HORA DO USER MENOR Q HORA ATUAL
                parameters.f_time = get_current_time() # F_TIME = HORA ATUAL
        else:
            parameters.f_time = usuario.F_time
        return usuario.I_time, parameters.f_time
    elif status == "varios_dias":
        return usuario.I_time, usuario.F_time

def edit_time(my_time) -> datetime:
    """ Formata o tempo pra não ter ":" e adiciona os segundos. """
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

def format_time(my_time):
    """ Formata o tempo. """
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

def process_multiple_days(initial_date_str: str, final_date_str: str):
    """ Transforma a string recebida em datas. 
        Entra no tempo diversos dias. """
    initial_date = datetime.strptime(initial_date_str, '%d-%m-%Y') 
    final_date = datetime.strptime(final_date_str, '%d-%m-%Y')
    
    current_date = initial_date

    while current_date <= final_date:
        if current_date.weekday() not in [5,6]: #Se for dia util ele entra
            parameters.start_date = current_date.strftime("%d-%m-%Y")
            receive_sige_keys("varios_dias")
        current_date += timedelta(days=1) # Aumenta um dia
    receive_sige_keys("fechar")
    return