import flet as ft
import os

# MEUS ARQUIVOS #
from user_model import usuario
from banco import *
import config
from controls import get_login_info
#               #
USER_FILE_PATH = os.path.expanduser("~/Documents/autopyme_user.txt") # Caminho onde armazena ultimo login

class LoginPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        self.username_field = ft.TextField(
            label="Cracha", 
            width=150,
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=8,
            prefix_icon=ft.icons.BADGE_OUTLINED,
            autofocus=True,
        )
        
        self.password_field = ft.TextField(
            label="Senha", 
            password=True,
            width=150,
            prefix_icon=ft.icons.LOCK,
            can_reveal_password=True,
        )
        
        self.login_button = ft.FilledButton(
            text="Fazer login",
            width=150,
            on_click=self.verify_login
        )
        
        self.exit_button = ft.IconButton(
            icon=ft.icons.EXIT_TO_APP,
            on_click=self.gotoapp,
            tooltip="Voltar ao menu"
        )
        
        self.login_content = ft.Container(
            alignment=ft.alignment.center,
            height=600,
            #bgcolor=ft.colors.DEEP_PURPLE_700,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                 ft.Text("Fazer login", size = 30, text_align=ft.TextAlign.CENTER),
                 self.username_field,
                 self.password_field,
                 self.login_button,   
                 self.exit_button            
                ]
            ),
        )
        
        self.content = self.login_content
    
    def gotoapp(self,e):
        self.page.clean()
        from app import App
        self.page.add(App(page=self.page))
        self.page.update()
    
    def verify_login(self,e):
        username = self.username_field.value
        password = self.password_field.value
        
        self.username_field.error_text = "" # Pra "resetar" o campo de erro se nao ele permanece fixo apos primeiro erro
        self.password_field.error_text = ""
        
        if len(self.username_field.value) <= 7:
            self.username_field.error_text = "Deve ter 8 digitos"
            self.page.update()
            return
        
        if not self.password_field.value:
            self.password_field.error_text = "Campo Obrigatório"
            self.page.update()
            return
        
        try:
            credential_sucess, password_str = login_user_db(username, password)
            if credential_sucess:
                with open(USER_FILE_PATH, "w") as f:
                    f.write(password_str)
                    first_name = extract_name(username)
                    config.logged_in_user = first_name
                    usuario.id = username
                    join_settings(self.page,first_name)
            else:
                return
        except:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(value="USUARIO NÃO ENCONTRADO",text_align=ft.TextAlign.CENTER),bgcolor=ft.colors.RED,)
            self.page.snack_bar.open = True
            self.page.update()     
            
        get_login_info()  
        
class UserSettingsPage(ft.Container):
    def __init__(self, page: ft.Page, ): #on_save_callback
        super().__init__()
        self.page = page
        #self.on_save_callback = on_save_callback
        self.settings_label = ft.Text("Configurações do Usuário", size=30, text_align=ft.TextAlign.CENTER)
        
        self.settings_content = ft.Column(
            controls=[
                self.settings_label,
                ft.FilledButton(text="Sair", on_click=self.save_settings)
            ]
        )
        
        self.content = self.settings_content
    
    
    
    def save_settings(self,e):
        self.page.clean()
        from app import App
        self.page.add(App(page=self.page))
        self.page.update()

window_size_height = 750
window_size_width = 450

def join_settings(page:ft.Page,username):
    page.clean()
    page.add(ft.Text(f"Olá, {username}", size=25, text_align=ft.TextAlign.CENTER))
    page.add(UserSettingsPage(page))
    
def init_parameters() -> bool:
    if os.path.exists(USER_FILE_PATH): # SE TIVER ARQUIVO TXT
        with open(USER_FILE_PATH, 'r') as f:
            crypt_password = f.read().strip() # LE A SENHA DO TXT
            usuario.id = verify_password(crypt_password) # Verifica se a senha do bloco de notas esta correta e retorna o ID
            if usuario.id is not None:
                get_login_info()
                return True
            else:
                return False
    return False
            
def init_user_settings(page:ft.Page):
    logged = init_parameters()
    first_name = config.logged_in_user
    if logged:
        join_settings(page,first_name)
    else:
        page.add(LoginPage(page)) # Caso mudem a senha no bloco de notas ele volta pro login
        
# def main(page:ft.Page):
#     page.window.height = window_size_height
#     page.window.width = window_size_width
#     page.window.max_height = window_size_height+5
#     page.window.max_width = window_size_width+5
#     page.window.min_height = window_size_height-5
#     page.window.min_width = window_size_width-5
#     page.theme_mode = "dark"
#     page.title = "AutoPyme - Entrada de tempos"

#     if os.path.exists(USER_FILE_PATH):
#         with open(USER_FILE_PATH, 'r') as f:
#             crypt_password = f.read().strip() # LE A SENHA DO TXT
#             str(crypt_password) 
#             my_id = verify_password(crypt_password) # Verifica se a senha do bloco de notas esta correta e retorna o ID
#             if my_id is not None:
#                 first_name = extract_name(my_id) # Pega o ID e procura o primeiro nome
#                 join_settings(page,first_name)
#             else:
#                 page.add(LoginPage(page)) # Caso mudem a senha no bloco de notas ele volta pro login
#     else:
#         page.add(LoginPage(page))
        
        
# ft.app(main)