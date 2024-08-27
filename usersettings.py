import flet as ft
import os

# MEUS ARQUIVOS #
from user_model import usuario
from banco import *
import parameters
from controls import get_login_info
#               #

USER_FILE_PATH = os.path.expanduser("~/Documents/autopyme_user.txt") # Caminho onde armazena ultimo login

class LoginPage(ft.Container):
    """ Página de login do usuário."""
    
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
            on_click=self.go_to_app,
            tooltip="Voltar ao menu"
        )
        
        self.login_content = ft.Container(
            alignment=ft.alignment.center,
            height=600,
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
    
    def go_to_app(self, e):
        """ Vai para o menu principal novamente. """
        
        self.page.clean()
        from app import App
        self.page.add(App(page=self.page))
        self.page.update()
    
    def verify_login(self, e) -> bool:
        """ Verifica se o username e password estão de acordo com o database """
        
        self.username_field.error_text = "" 
        self.password_field.error_text = ""
        
        if len(self.username_field.value) <= 7:
            self.username_field.error_text = "Deve ter 8 digitos"
            self.page.update()
            return False
        
        if not self.password_field.value:
            self.password_field.error_text = "Campo Obrigatório"
            self.page.update()
            return False
        
        username = self.username_field.value
        password = self.password_field.value
        
        try:
            credential_sucess, password_str = login_user_db(username, password)
            if credential_sucess:
                with open(USER_FILE_PATH, "w") as f:
                    f.write(password_str)
                    parameters.user_first_name = extract_first_name(username)
                    usuario.id = username
                    join_settings(self.page,parameters.user_first_name)
            else:
                return False
        except:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(value="USUARIO NÃO ENCONTRADO",text_align=ft.TextAlign.CENTER,color=ft.colors.BLACK),bgcolor=ft.colors.RED_400,)
            self.page.snack_bar.open = True
            self.page.update()     
            
        get_login_info()  
        return True
        
class UserSettingsPage(ft.Container):
    """ Menu de configuração do usuário. """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.settings_label = ft.Text("Configurações do Usuário", size=30, text_align=ft.TextAlign.CENTER)
        
        self.settings_content = ft.Column(
            controls=[
                self.settings_label,
                ft.FilledButton(text="Sair", on_click=self.back_to_app)
            ]
        )
        
        self.content = self.settings_content
    
    def save_settings(self, e):
        """ Salvar as alterações """
        
        ...

    def back_to_app(self, e):
        """ Vai para o menu principal novamente. """
        
        self.page.clean()
        from app import App
        self.page.add(App(page=self.page))
        self.page.update()

def join_settings(page:ft.Page, username: str) -> bool:
    """ Vai para o menu de configuração do usuário. """
    
    page.clean()
    page.add(ft.Text(f"Olá, {username}", size=25, text_align=ft.TextAlign.CENTER))
    page.add(UserSettingsPage(page))
    
def init_parameters() -> bool:
    """ Inicialização do usuário. Caso tenha um arquivo ".txt" irá verificar qual usuário pertence e fazer login """
    
    if os.path.exists(USER_FILE_PATH):
        with open(USER_FILE_PATH, 'r') as f:
            crypt_password = f.read().strip()
            usuario.id = get_id_from_password(crypt_password)
            if usuario.id is not None:
                get_login_info()
                return True
            else:
                return False
    return False
            
def init_user_settings(page:ft.Page):
    """ Inicializa a página de configuração do usuário. """
    
    if init_parameters():
        join_settings(page,parameters.user_first_name)
    else:
        page.add(LoginPage(page)) # Caso mudem a senha no bloco de notas ele volta pro login