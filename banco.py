import sqlite3 as sq
from cryptography.fernet import Fernet
import base64
import hashlib

# MEUS ARQUIVOS #
from user_model import Usuario
#               #

# 

def generate_key():
    """ Gerar uma chave para o Fernet. """
    return Fernet.generate_key()

key = base64.urlsafe_b64encode(hashlib.sha256(b'secrect_key').digest())
cipher_suite = Fernet(key)

conn = sq.connect("files\\autopymeusers.db", check_same_thread=False)

def Create_Table():
    """ Cria a tabela usuarios se ela nao existir. """
    cursor = conn.cursor()
    conn.execute("""
    create table if not exists usuarios (
        ID text primary key,
        Name text,
        I_time text,
        F_time text,
        User text,
        Password text,
        Asstec text,
        Etapa text,
        Status text
    )
    """)
    conn.commit()

def edit_user_infos(user: str, value: str, new_value: str) -> bool:
    """ Edita a informação do usuario baseado no ID. """
    
    values = ['Name','I_time','F_time','User','Password',"Asstec","Etapa","Status"]
    if value in values:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE usuarios SET {value} = ? WHERE ID = ?",(new_value, user)) # Update usuario no campo de valor tal quando id for o correto
        conn.commit()
        return True
    else:
        return False

def remove_user_info(user: str):
    """ Remove um usuario baseado no ID. """
    
    cursor = conn.cursor()
    deleted_user = cursor.execute("DELETE FROM usuarios WHERE ID = ?",([user,]))
    conn.commit()

def validate_user_credentials(user_id: str, password: str) -> bool:
    """ Verifica se a senha digitada esta identifica a senha do banco de dados. """
    
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM usuarios WHERE ID = ?",(user_id,))
    my_pass = cursor.fetchone()
    my_pass = my_pass[0]
    decrypted_password = cipher_suite.decrypt(my_pass).decode()
    if password == decrypted_password:
        return True
    return False

def get_id_from_password(password: str):
    """ Coleta o ID com base na senha. """
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID FROM usuarios WHERE Password = ?",(password,))
        my_id = cursor.fetchone()
        if my_id:
            return my_id[0]
    except:
        return None
    
def get_time_from_id(user_id: str) -> str:
    " Coleta o tempo do usuario com base no ID. "
    
    cursor = conn.cursor() 
    cursor.execute("SELECT I_time FROM usuarios WHERE ID = ?",(user_id,)) # BUSCA TEMPO INICIAL DB
    I_time = cursor.fetchone()[0]

    cursor.execute("SELECT F_time FROM usuarios WHERE ID = ?",(user_id,)) # BUSCA TEMPO FINAL DB
    F_time = cursor.fetchone()[0]

    return I_time, F_time

def get_parameters(user_id: str) -> str:
    " Coleta os parametros com base no ID. "
    
    cursor = conn.cursor() 
    cursor.execute("SELECT Asstec FROM usuarios WHERE ID = ?",(user_id,)) # BUSCA ASSTES DB
    asstec = cursor.fetchone()[0]
    
    cursor.execute("SELECT Etapa FROM usuarios WHERE ID = ?",(user_id,)) # BUSCA ETAPA DB
    etapa = cursor.fetchone()[0]
    
    cursor.execute("SELECT Status FROM usuarios WHERE ID = ?",(user_id,)) # BUSCA STATUS DB
    status = cursor.fetchone()[0]
    
    cursor.execute("SELECT I_time FROM usuarios WHERE ID = ?",(user_id,)) # BUSCA TEMPO INICIAL DB
    I_time = cursor.fetchone()[0]
    
    cursor.execute("SELECT F_time FROM usuarios WHERE ID = ?",(user_id,)) # BUSCA TEMPO FINAL DB
    F_time = cursor.fetchone()[0]
    return asstec, etapa, status, I_time, F_time

def get_id(name: str):
    """ Coleta o ID baseado no nome. """
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID FROM usuarios WHERE Name LIKE ?",(name+"%",))
        my_id = cursor.fetchone()
        if my_id:
            return my_id[0]
    except:
        return None

def extract_full_name(user_id: str) -> str:
    """ Coleta o nome completo com base no ID. """
    
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM usuarios WHERE ID = ?",(user_id,))
    name = cursor.fetchone()[0]
    return name
    
def extract_first_name(user_id: str):
    """ Coleta o nome com base no id e splita apenas o primeiro nome. """
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM usuarios WHERE ID = ?",(user_id,))
    name = cursor.fetchone()
    first_name = str(name).split()[0]
    first_name_str = str(first_name).replace('(', '').replace("'","")
    return str(first_name_str)

def parameters_db_login_sige(user_id: str) -> str:
    """ Coleta o usuario e senha do sige com base no id. """
    
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM usuarios WHERE ID = ?",(user_id,))
    my_pass = cursor.fetchone()
    
    encrypted_password = my_pass[0]
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    
    cursor.execute("SELECT User FROM usuarios WHERE ID = ?",(user_id,))
    my_user = cursor.fetchone()
    return my_user[0], decrypted_password

def login_user_db(user_id: str, password: str): 
    """ VERIFICA SE A SENHA DIGITADA RETORNA BOOL E 
    A SENHA CRIPTOGRAFADA PRA ARMAZENAR TXT
    """ 
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Password FROM usuarios WHERE ID = ?",(user_id,))
        my_pass = cursor.fetchone()
        encrypted_password = my_pass[0]
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        if password == decrypted_password:
            return True, encrypted_password
    except:
        return False

def add_user_to_db(new_user: Usuario):
    """ Adiciona um novo usuario ao banco de dados. """
    encrypted_password = cipher_suite.encrypt(new_user.password.encode()).decode()
    cursor = conn.cursor()
    cursor.execute("Insert into usuarios (ID, Name, I_time, F_time, User, Password) values (?,?,?,?,?,?)",(new_user.id, new_user.name, new_user.I_time, new_user.F_time, new_user.user, encrypted_password))
    conn.commit()

def verify_exist_id(id: str) -> bool:
    """ Verifica se o id existe. """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ID = ?", (id,))
    count = cursor.fetchone()[0]
    return count > 0

def load_user_data(id: str):
    cursor = conn.cursor()
    cursor.execute("SELECT Name, I_time, F_time, User, Password FROM usuarios WHERE ID = ?",(id,))

def load_all_users():
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM usuarios")
    return cursor.fetchall()

def extract_first_name_all_users():
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM usuarios")
    rows = cursor.fetchall()
    first_names = [str(name).split()[0] for (name,) in rows]  # Divide o nome completo e pega o primeiro nome
    return first_names

def main():
    Create_Table()

    while True:
        print("Escolha uma opção:\n")
        print("1. Adicionar usuario")
        print("2. Editar usuario")
        print("3. Remover usuario")
        print("4. Sair")

        escolha = input("Digite a opcao: ")
        print(f"Opção é {escolha}\n")

        match escolha:
            case "1":
                ID = input("ID: ")
                Name = input("Name: ")
                I_time = input("I_time: ")
                F_time = input("F_time: ")
                User = input("User: ")
                Password = input("Password: ")
                new_user = Usuario(ID, Name, I_time, F_time, User, Password)
                add_user_to_db(new_user)
                print("\nUsuario adicionado.")

            case "2":
                ID = input("Digite o ID para editar: ")
                value = input("Digite o campo que quer editar (Name, I_time, F_time, User, Password): ")
                new_value = input("Digite o novo valor: ")
                user_edit = Usuario(ID,"","","","","")
                edit_user_infos(user_edit, value, new_value)

            case "3":
                ID = input("Digite o ID do usuario a ser removido: ")
                remove_user_info(ID)

            case "4":
                print("Saindo...")
                break

            case _:
                print("Opcao invalida")

if __name__ == "__main__":
    main()
