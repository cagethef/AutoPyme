
"""
    CODIGO PARA EVITAR A DEMORA AO ABRIR O PROGRAMA. 
    BASICAMENTE O CODIGO PEGA OS ARQUIVOS DO AUTOPYME E COPIA PARA O "user/documents"
    SEMPRE QUE ABRIR ELE VERIFICA SE A DATA DE MODIFICAÇÃO É A MESMA E ABRE O CODIGO DE DOCUMENTS. MUITO EFICAZ
"""
import os
import shutil
import subprocess

server_path = r'\\servidor\desenv\SOFTWARE\AUTOPYME\files'
user_path = os.path.expanduser(r'~/Documents/AutoPyme')

def prepare_paths():
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    
    arquivos = ['AutoPyme.exe', '_internal', 'assets', 'utils']
    
    for arquivo in arquivos:
        src = os.path.join(server_path, arquivo)
        dst = os.path.join(user_path, arquivo)
        
        if os.path.isdir(src):
            if not os.path.exists(dst):
                shutil.copytree(src, dst)
        elif os.path.isfile(src):
            if not os.path.exists(dst):
                shutil.copy2(src, dst)

def execute_my_program():
    exe_file = os.path.join(user_path, 'AutoPyme.exe')
    
    if os.path.exists(exe_file):
        subprocess.run([exe_file], check=True)
    else:
        print("Erro: Executável não encontrado!")

def verificar_atualizacao():
    server_exec_path = os.path.join(server_path, 'AutoPyme.exe')
    local_exec_path = os.path.join(user_path, 'AutoPyme.exe')

    if os.path.exists(server_exec_path):
        server_data = os.path.getmtime(server_exec_path)
    else:
        print("Erro: Arquivo no servidor não encontrado!")
        return

    local_data = os.path.getmtime(local_exec_path) if os.path.exists(local_exec_path) else 0
    
    if server_data > local_data:
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        shutil.copy2(server_exec_path, local_exec_path)
        prepare_paths()
    
def main():
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    
    verificar_atualizacao()
    prepare_paths()
    execute_my_program()
    
if __name__ == '__main__':
    main()
