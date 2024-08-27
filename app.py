import flet as ft
import time

""" MEUS ARQUIVOS """
from user_model import usuario
from banco import *
from ler_etapa import *
from usersettings import *
from controls import *
"""               """

class App(ft.Container):
    """ Página principal """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
    
        init_parameters()
        self.show_home_page()
        
    def initialize_pages(self):
        self.home_page = ft.Container()
        self.user_settings_page_container = ft.Container
    
    def show_home_page(self):
        self.page.controls.clear()
        self.etapas_data = load_etapas_from_ods()
        
        lv = ft.ListView(spacing=2,divider_thickness=1,) # List View que mostra todas as etapas
        for value in load_full_from_ods():
            value_str = str(value).replace(',', ' - ')
            lv.controls.append(ft.Text(value_str))
            
        self.page.appbar=ft.AppBar(
            leading=ft.Icon(ft.icons.CRUELTY_FREE_OUTLINED), # Logo do programa
            title=ft.Text("AutoPyme",size=35, text_align="START", font_family="SEMonotxt",weight=ft.FontWeight.BOLD,),
            center_title=True,
            bgcolor=ft.colors.DEEP_PURPLE_800,
            toolbar_height=50,
            actions=[
                ft.IconButton( 
                    icon=ft.icons.MANAGE_HISTORY, 
                    tooltip="Ver tempo",
                    on_click=self.look_user_time,
                ),
                ft.PopupMenuButton(
                    items=[ 
                        ft.PopupMenuItem(text="Adicionar Usuário",on_click=self.open_newuser_dialog,),
                        ft.PopupMenuItem(text="Remover Usuário",on_click=self.open_removeuser_dialog),
                    ]
                )
            ],
        )
        
        """ Campos para criação objetos """
        
        self.new_user_name=ft.TextField(
            label="Nome Completo conforme SIGE",
            width=300,
            input_filter=ft.InputFilter(allow=False,regex_string=r"[0-9]",), #Bloqueia por numeros nesse campo
            capitalization=ft.TextCapitalization.WORDS,
            prefix_icon=ft.icons.ACCOUNT_BOX,
            on_change=self.clear_error,
        )
        
        self.new_user_id=ft.TextField(
            label="Cracha",
            width=300,
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=8,
            prefix_icon=ft.icons.BADGE_OUTLINED,
            on_change=self.clear_error,
        )
        
        self.new_user_start_time_picker = ft.TimePicker(
            confirm_text="OK",
            cancel_text="Sair",
            hour_label_text="Hora",
            minute_label_text="Minutos",
            error_invalid_text="Tempo errado",
            time_picker_entry_mode="input",
            help_text="Selecione o inicio de expediente",
            value="07:00",
        )
        
        self.new_user_end_time_picker = ft.TimePicker(
            confirm_text="OK",
            cancel_text="Sair",
            hour_label_text="Hora",
            minute_label_text="Minutos",
            error_invalid_text="Tempo errado",
            time_picker_entry_mode="input",
            help_text="Selecione o fim de expediente",
            value="16:48",
        )
        
        self.new_user_start_time_label = ft.Text("Hora Inicial", text_align=ft.TextAlign.CENTER)
        
        self.new_user_end_time_label = ft.Text("Hora Final", text_align=ft.TextAlign.CENTER)
        
        self.remove_user_id=ft.TextField(
            label="Cracha",
            width=300,
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=8,
            prefix_icon=ft.icons.BADGE_OUTLINED,
            on_change=self.clear_error,
        )
        
        self.remove_user_password = ft.TextField(
            label="Senha",
            width=300,
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
        )
        
        """     Construção dos itens     """
        
        self.new_user_start_time_button=ft.ElevatedButton(
            text="Inicio",
            icon=ft.icons.ACCESS_TIME,
            width=300,
            on_click=self.open_start_time_picker,
        )
        
        self.new_user_end_time_button=ft.ElevatedButton(
            text="Fim",
            icon=ft.icons.ACCESS_TIME,
            width=300,
            on_click=self.open_end_time_picker,
        )
        
        self.new_user_login_sige = ft.TextField(
            label="Login",
            width=300,
            input_filter=ft.TextOnlyInputFilter(),
            prefix_icon=ft.icons.PERSON,
        )
        
        self.new_user_password_sige = ft.TextField(
            label="Senha",
            width=300,
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
        )
        
        self.new_user_add_button=ft.FilledButton(
            text="Adicionar Usuario",
            style=ft.ButtonStyle(bgcolor="BLUE"),
            on_click=self.add_user
        )
        
        """       CAMPOS DO MENU        """
        
        self.asstec=ft.TextField(
            width=300,
            label="Numero da AssTec",
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=5,
            prefix_icon=ft.icons.ONETWOTHREE_OUTLINED,
            on_change=self.clear_error,
            value = usuario.asstec,
        )
        
        self.workman=ft.IconButton(
        icon=ft.icons.WORK_HISTORY_SHARP,
        on_click = self.look_workman,
        tooltip="Mão de obra",
        )
        
        self.etapa=ft.TextField(
            label="Etapa",
            width=300,
            prefix_icon=ft.icons.WORK,
            max_length=4,
            capitalization=ft.TextCapitalization.CHARACTERS,
            value = usuario.etapa,
        )
        
        self.etapa_dropdown=ft.Dropdown(   # LISTA DROPDOWN DAS ETAPAS (SETINHA)
        options=[
            ft.dropdown.Option(text=value)
            for value in self.etapas_data
        ],
        border_width=0,
        max_menu_height=250,
        on_change=self.on_etapa_dropdown_change,
        prefix_icon=ft.icons.ARROW_DROP_DOWN,
        width=30,       # Largura pequena para mostrar apenas a seta
        height=50       # Altura pequena tbm
        )
        
        self.etapa_help=ft.IconButton(
        icon=ft.icons.HELP,
        on_click = self.open_etapa_help_dialog,
        tooltip="Etapas de trabalho"
        )
        
        self.etapa_help_dialog = ft.AlertDialog(
            title=ft.Text("Etapas de Trabalho",text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                height=520,
                width=400,
                content=lv
            )
        )
        
        self.time_join=ft.TextField( # TEXTFIELD SELECIONAR HORA
            value=get_current_time(),
            visible=False,
            width=75,
            height=32,
            text_vertical_align=ft.VerticalAlignment.START,
            text_align=ft.TextAlign.CENTER,
            on_change=self.refresh_time,
        )
        
        self.time_exit=ft.TextField( # TEXTFIELD SELECIONAR HORA
            value=get_current_time(),
            visible=False,
            width=70,
            height=32,
            text_vertical_align=ft.VerticalAlignment.START,
            text_align=ft.TextAlign.CENTER,
            on_change=self.refresh_time,
        )
        
        self.extra_time=ft.Checkbox(
            label="Hora extra",
            active_color="BLUE",
            check_color="black",
            on_change=self.extra_time_changed
        )
        
        self.initial_calendar = ft.ElevatedButton(
            "Data Inicial",
            visible=False,
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime(year=2024,month=1,day=1),
                    last_date=datetime(year=2030,month=12,day=31),
                    confirm_text="OK",
                    cancel_text="Sair",
                    error_format_text="Formato invalido",
                    error_invalid_text="Fora dos limites",
                    field_label_text="Insira a data",
                    help_text="Insira a data",
                    on_change=self.my_initial_date,
                )
            )
        )
        
        self.final_calendar = ft.ElevatedButton(
            "Data Final",
            visible=False,
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime(year=2024,month=1,day=1),
                    last_date=datetime(year=2030,month=12,day=31),
                    confirm_text="OK",
                    cancel_text="Sair",
                    error_format_text="Formato invalido",
                    error_invalid_text="Fora dos limites",
                    field_label_text="Insira a data",
                    help_text="Insira a data",
                    on_change=self.my_final_date,
                )
            )
        )
        
        self.initial_date = ft.Text(value=f"        {get_current_date()}",visible=False,weight=ft.FontWeight.BOLD,italic=True)
        self.final_date = ft.Text(value=f"        {get_current_date()}",visible=False,weight=ft.FontWeight.BOLD,italic=True)
        
        self.radio_time_select = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Row(
                        width=130,
                        controls=[
                            ft.Radio(value="entrou", label="Entrar", fill_color=ft.colors.BLUE),
                            self.time_join,
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Radio(value="saiu", label="Sair", fill_color=ft.colors.BLUE),
                            self.time_exit,
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Radio(value="manha", label="Manhã completa", fill_color=ft.colors.BLUE),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Radio(value="tarde", label="Tarde completa", fill_color=ft.colors.BLUE),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Radio(value="dia_completo", label="Dia completo", fill_color=ft.colors.BLUE),
                            self.extra_time
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Radio(value="varios_dias", label="Vários dias", fill_color=ft.colors.BLUE),
                        ]
                    ),
                ]
            ),
            on_change=self.radio_time_changed,
        )
        
        self.message_label = ft.Text("", text_align=ft.TextAlign.CENTER, color=ft.colors.RED) # snack bar aba usuario
        
        self.message_label_sucess = ft.Text("", text_align=ft.TextAlign.CENTER, color=ft.colors.GREEN) # snack bar aba usuario sucesso
        
        """    ABA PESSOA    """
        
        self.user=ft.TextField(
            label="Pessoa",
            width=300,
            prefix_icon=ft.icons.ASSIGNMENT_IND,
            capitalization=ft.TextCapitalization.WORDS,
            value = usuario.name,
            on_blur = self.user_changed,
        )

        self.user_dropdown=ft.Dropdown(   # LISTA DROPDOWN NOMES (SETINHA)
        options=[
            ft.dropdown.Option(text=value)
            for value in extract_first_name_all_users()
        ],
        border_width=0,
        max_menu_height=250,
        on_change=self.on_user_dropdown_change,
        prefix_icon=ft.icons.ARROW_DROP_DOWN,
        width=130,       # Largura pequena para mostrar apenas a seta
        height=20,       # Altura pequena tbm
        )

        """ ABA NOVO USUARIO """
        
        self.newuser_dialog = ft.AlertDialog(   
            title=ft.Text("ADICIONAR USUARIO",text_align="CENTER"),
            content=ft.Container(
                height=550,
                content=ft.Column(
                controls=[
                    self.new_user_name,
                    self.new_user_id,
                    ft.Divider(), # divisoria
                    ft.Text("EXPEDIENTE", text_align=ft.TextAlign.CENTER),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Column(
                                    controls=[
                                        self.new_user_start_time_button,
                                        self.new_user_start_time_label,
                                        self.new_user_end_time_button,
                                        self.new_user_end_time_label,
                                    ]
                                ),
                            ]
                        ),
                        ft.Divider(),
                        ft.Text("SIGE",text_align=ft.TextAlign.CENTER),
                        self.new_user_login_sige,
                        self.new_user_password_sige,
                        ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.new_user_add_button,
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                self.message_label,
                                self.message_label_sucess,
                            ]
                        ),
                ]
            ),
            )
        )
        
        """ REMOVER USUARIO """
        
        self.removeuser_dialog = ft.AlertDialog(
            title=ft.Text("Remover Usuário",text_align="CENTER"),
            content=ft.Container(
                height=200,
                content=ft.Column(
                controls=[
                    self.remove_user_id,
                    self.remove_user_password,
                    ft.Divider(),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.FilledButton(
                                text="Remover",
                                style=ft.ButtonStyle(bgcolor="BLUE"),
                                on_click=self.remove_user
                            ),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.message_label,
                            self.message_label_sucess,
                        ]
                    ),
                ]
            )
            )
        )
        
        self.home_page = ft.Column( # Construção do conteudo do menu PRINCIPAL
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("REGISTROS DE TRABALHO",style=ft.TextStyle(size=18,)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        self.asstec,
                        self.workman,
                    ]
                ),
                ft.Row(
                    controls=[
                        self.etapa,
                        self.etapa_dropdown,
                        self.etapa_help,
                    ]
                ),
                ft.Row(
                    controls=[
                        self.user,
                        self.user_dropdown,
                    ]
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Text("HORARIOS",style=ft.TextStyle(size=18,)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.Container(content=self.radio_time_select,),
                        ft.Container(
                            alignment=ft.alignment.top_left,
                            height=150,
                            width=180,
                            content=ft.Column(
                                controls=[
                                    self.initial_calendar,
                                    self.initial_date,
                                    self.final_calendar,
                                    self.final_date,
                                ],
                            ),
                        ),
                    ]
                ),
                
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            text="ENTRAR NO TEMPO",
                            style=ft.ButtonStyle(bgcolor="BLUE"),
                            on_click=self.execute_time,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE,on_click=self.show_user_settings_page,tooltip="Meu usuário"), # ICONE DE USUARIO LOGADO 
                        ft.IconButton(icon=ft.icons.LENS_BLUR,on_click=self.try_open_sige,tooltip="Abrir SIGE"), # ICONE DE SIGE
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ]
        )
        
        self.page.add(self.home_page)
        
    ################## Funcoes dialog ##################
    
    def my_initial_date(self, e):
        """ Define a data inicial do usuário quando alterada. """
        
        parameters.start_date = e.control.value.strftime('%d-%m-%Y')
        self.initial_date.value = f"        {parameters.start_date}"
        self.page.update()
    
    def my_final_date(self,e):
        """ Define a data final do usuário quando alterada. """
        
        parameters.final_date = e.control.value.strftime('%d-%m-%Y')
        self.final_date.value = f"        {parameters.final_date}"
        self.page.update()

        
    def show_user_settings_page(self, e):
        """ Altera para a janela de configuração de usuário. """
        self.page.clean()
        init_user_settings(self.page)
        self.page.update()
    
    def try_open_sige(self, e):
        """ Tenta abrir o sige. 
        Caso não tenha usuário logado vai ficar na tela esperando o usuário digitar algo. 
        """
        
        if parameters.user_first_name is not None:
            sige_user = parameters.sige_username
            sige_password = parameters.sige_password
            
        else:
            sige_user = ""
            sige_password = ""
            
        if not open_sige(sige_user,sige_password):
            self.text_snack_bar("ERRO AO ABRIR O SIGE","erro")
          
    def open_etapa_help_dialog(self, e):
        """ Abre a popup de etapas. """
        self.page.open(self.etapa_help_dialog)
                       
    def open_newuser_dialog(self, e):
        """ Abre o popup de adicionar usuário. """
        self.page.open(self.newuser_dialog)        

    def open_removeuser_dialog(self, e):
        """ Abre o popup de remover usuário. """
        self.page.open(self.removeuser_dialog)

    """     MENU DEFS      """
    
    def look_user_time(self, e):
        """ Verifica se os campos estão corretos para abrir o tempo no sige. """
        if self.user.value == "": # SE NAO TIVER "PESSOA" APARECE ERRO
            self.user.error_text = "Campo obrigatório"
            self.page.update()
            return
        else:
            open_time()
            verify_my_time(self.user.value)
            
    def look_workman(self, e):
        """ Verifica se os campos estão corretos para abrir a mão de obra no sige. """
        
        if self.asstec.value == "":
            self.asstec.error_text = "Campo obrigatório"
            self.page.update()
            return
        
        if parameters.user_first_name is not None:
            sige_user = parameters.sige_username
            sige_password = parameters.sige_password
            
        else:
            sige_user = ""
            sige_password = ""
            
        if open_sige(sige_user,sige_password):
           open_workman(self.asstec.value) #Abre mao de obra
        else:  
            self.text_snack_bar("ERRO AO ABRIR MÃO DE OBRA","erro")
            return
        
    
    def refresh_time(self, e):
        """ Atualiza o textfield de tempo. """
        
        formatted_text = format_time(e.control.value)
        e.control.value = formatted_text
        parameters.start_time = e.control.value
        self.page.update()
    
    def on_etapa_dropdown_change(self, e): 
        """ Atualiza valor do campo de texto com base no dropdown. """
        
        selected_value = self.etapa_dropdown.value
        self.etapa.value = selected_value
        self.page.update()
    
    def on_user_dropdown_change(self, e): 
        """ Atualiza valor do campo de texto com base no dropdown. """
        
        selected_value = self.user_dropdown.value
        self.user.value = selected_value
        user_parameters()
        self.page.update()
        
    def update_user_dropdown(self):
        """ Atualiza o dropdown com os nomes. """
        
        user_options = [
            ft.dropdown.Option(text=value)
                        for value in extract_first_name_all_users()
            ]
        self.user_dropdown.options = user_options
        self.page.update()    
    
    def radio_time_changed(self, e):
        """ Define o que irá aparecer na tela baseado no "radio" selecionado. """
        
        escolha = self.radio_time_select.value
        
        self.time_join.visible = False
        self.time_exit.visible = False
        self.initial_calendar.visible = False
        self.initial_date.visible = False
        self.final_calendar.visible = False
        self.final_date.visible = False
        
        if escolha == "entrou":
            self.time_join.visible = True
            self.initial_calendar.visible = True
            self.initial_date.visible = True
            self.time_join.value = get_current_time()
            parameters.start_time = self.time_join.value
        elif escolha == "saiu":
            self.time_exit.visible = True
            self.initial_calendar.visible = True
            self.initial_date.visible = True
            self.time_exit.value = get_current_time()
            parameters.start_time = self.time_join.value
        elif escolha == "manha":
            self.initial_calendar.visible = True
            self.initial_date.visible = True
        elif escolha == "tarde":
            self.initial_calendar.visible = True
            self.initial_date.visible = True
        elif escolha == "dia_completo":
            self.initial_calendar.visible = True
            self.initial_date.visible = True
        elif escolha == "varios_dias":
            self.initial_calendar.visible = True
            self.initial_date.visible = True
            self.final_calendar.visible = True
            self.final_date.visible = True
            
        self.page.update()
    
    def user_changed(self, e):
        """ Ao perder o desfoque atualiza o nome do usuário. """
        usuario.name = self.user.value
        user_parameters()
    
    def extra_time_changed(self, e):
        """ Resgata o valor lógico do tempo extra. """
        parameters.extra_time = self.extra_time.value
    
    """ NOVO USUARIO DEFS """
    
    def add_user(self, e):
        """ Função que verifica os parâmetros ao tentar adicionar um usuário.
            Se estiver tudo certo, envia as informações para o banco de dados.
        """
        
        if verify_exist_id(self.new_user_id.value):
            self.message_label.value = "Cracha já existe."
            self.page.update()
            return        
        elif len(self.new_user_id.value) <= 7:
            self.new_user_id.error_text = "Deve ter 8 digitos"
            self.page.update()
            return
        elif not self.new_user_name.value:
            self.new_user_name.error_text = "Campo Obrigatório"
            self.page.update()
            return
        elif not self.new_user_id.value:
            self.new_user_id.error_text = "Campo Obrigatório"
            self.page.update()
            return
        elif not self.new_user_start_time_picker.value:
            self.new_user_start_time_picker.error_text = "Campo Obrigatório"
            self.page.update()
            return
        elif not self.new_user_end_time_picker.value:
            self.new_user_end_time_picker.error_text = "Campo Obrigatório"
            self.page.update()
            return
        
        if self.new_user_start_time_picker.value and self.new_user_end_time_picker.value:
            if self.new_user_end_time_picker.value <= self.new_user_start_time_picker.value:
                self.message_label.value = "Hora Final deve ser maior que a Hora Inicial."
                self.page.update()
                return

        self.message_label.value = ""
        new_user = Usuario(self.new_user_id.value, self.new_user_name.value, 
                           str(self.new_user_start_time_picker.value), 
                           str(self.new_user_end_time_picker.value), 
                           self.new_user_login_sige.value, 
                           self.new_user_password_sige.value, None, None, None, None)
        add_user_to_db(new_user)
        self.message_label_sucess.value = "Úsuario adicionado."
        self.page.update()
        self.new_user_id.value = ""
        self.new_user_name.value = ""
        self.new_user_start_time_picker.value = ""
        self.new_user_end_time_picker.value = ""
        self.message_label_sucess.value = ""
        self.new_user_password_sige.value = ""
        self.new_user_login_sige.value = ""
        time.sleep(1)
        self.page.close(self.newuser_dialog)
        self.update_user_dropdown()
        
    def open_start_time_picker(self, e):
        """ Abre o relógio de inicio de expediente. """
        
        self.page.open(self.new_user_start_time_picker)
        self.new_user_start_time_picker.on_change=self.update_start_time_label

    def open_end_time_picker(self, e):
        """ Abre o relógio do fim de expediente. """
        
        self.page.open(self.new_user_end_time_picker)
        self.new_user_end_time_picker.on_change = self.update_end_time_label
    
    def update_start_time_label(self, e):
        """ Atualiza o texto com a hora do expediente. """
        
        if self.new_user_start_time_picker.value:
            self.new_user_start_time_label.value = f"Hora Inicial: {self.new_user_start_time_picker.value}"
            self.page.update()
    
    def update_end_time_label(self, e):
        """ Atualiza o texto com a hora do expediente. """
        
        if self.new_user_end_time_picker.value:
            self.new_user_end_time_label.value = f"Hora Final: {self.new_user_end_time_picker.value}"
            self.page.update()
    
    """ REMOVER USUARIO DEFS """
    
    def remove_user(self, e):
        """ Função que verifica os parâmetros ao tentar remover um usuário.
            Se estiver tudo certo, envia as informações para o banco de dados e deleta.
        """
        
        if not verify_exist_id(self.remove_user_id.value):
            self.message_label.value = "Cracha não existe."
            self.page.update()
            return  

        #if not validate_user_credentials(user_id,password):
        if self.remove_user_password.value != "desenv0912":
            self.message_label.value = "Senha incorreta."
            self.page.update()
            
        remove_user_info(self.remove_user_id.value)
        self.message_label.value = ""
        self.message_label_sucess.value = "Usuario removido."
        self.page.update()
        time.sleep(1)
        self.page.close(self.removeuser_dialog)
        self.remove_user_id.value = ""
        self.remove_user_password.value = ""
        self.message_label_sucess.value = ""
        self.update_user_dropdown()
            
    def clear_error(self, e):
        e.control.error_text = ""
        self.page.update()
    
    """       DEF GERAL   """
    
    def blank_value(self) -> bool: 
        """ Verifica os valores vazios ao tentar entrar no tempo. """
        
        options = [self.asstec, self.etapa, self.user]
        self.etapa.error_text = ""
        self.user.error_text = ""
        self.asstec.error_text = ""
        
        for option in options:
            if option.value == "":
                option.error_text = "Campo obrigatório"
                self.page.update()
                return True
        return False
    
    def text_snack_bar(self,text,message_type):
        """ Define o estilo da snack bar com os seguintes parâmetros.
            text: Mensagem que irá aparecer na snack bar.
            message_type: Pode receber "erro" ou "ok" e irá mudar a cor do bg da snackbar.
        """
        
        if message_type == "erro":
            color = ft.colors.RED_400
        elif message_type == "ok":
            color = ft.colors.GREEN_ACCENT_400
            
        self.snack_bar = ft.SnackBar(
            content=ft.Text(
                value=text,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLACK
                ),
            bgcolor=color
            )
        self.page.snack_bar = self.snack_bar
        self.page.snack_bar.open = True
        self.page.update()
    
    def is_error_status_to_db(self) -> bool: 
        """ Verifica se o usuário ja está em algum tempo."""

        values = ["entrou", "manha", "tarde", "dia_completo", "varios_dias"]
        
        if usuario.status == "entrou":
            for value in values:
                if self.radio_time_select.value == value:
                    self.text_snack_bar("VOCÊ JA ESTA EM UM TEMPO, SAIA ANTES DE ENTRAR","erro")
                    return True         
        elif usuario.status == "saiu":
            if self.radio_time_select.value == "saiu":
                self.text_snack_bar("VOCÊ NÃO ENTROU EM NENHUM TEMPO","erro")
                return True
        return False
    
    def is_error(self) -> bool: 
        """ Verifica possiveis campos vazios e 
        também se ja entrou em outra asstec ou etapa. 
        """

        if usuario.etapa != self.etapa.value and usuario.status == "entrou": # ERRO ENTROU EM OUTRA ETAPA
            self.etapa.error_text = "Entrou em outra etapa"
            self.page.update()
            return True
        
        elif usuario.asstec != self.asstec.value and usuario.status == "entrou": # ERRO ENTROU EM OUTRA ASSTEC 
            self.asstec.error_text = "Entrou em outra asstec"
            self.page.update()
            return True
        
        elif self.blank_value(): return True# SE TIVER CAMPO EM BRANCO RETORNA
        
        elif self.radio_time_select.value == None: # ERRO HORARIO VAZIO
            self.text_snack_bar("PREENCHA O CAMPO DE HORARIO","erro")
            return True
        
        usuario.asstec = self.asstec.value
        usuario.etapa = self.etapa.value
        usuario.name = self.user.value
        
        if self.is_error_status_to_db(): return True
        
        usuario.status = self.radio_time_select.value # SETA STATUS DO USUARIO
        return False
    
    def execute_time(self, e):
        """ Função executada ao tentar entrar no tempo.
            Chama as funções pra verificar se tem algo incoerente.
            Caso esteja tudo certo, entra no tempo e atualiza o banco de dados.
        """
        
        if self.is_error(): return # SE TIVER ALGO INCOERENTE NOS CAMPOS N ENTRA NO TEMPO E AVISA
        
        usuario.id = get_id(usuario.name) # pega o cracha
        workstation = int(search_workstation_from_ods(usuario.etapa)) # Busca a bancada da etapa
        usuario.workstation = str(workstation)
        if parameters.start_date == None:
            parameters.start_date = get_current_date()
        
        if parameters.start_time == None:
            parameters.start_time = get_current_time()

        # PEGA A HORA DO USUARIO ATUAL
        usuario.I_time, usuario.F_time = get_time_from_id(usuario.id)
        # MANDA O STATUS E DEFINE A HORA QUE SERA ENVIADA    
        parameters.start_time, parameters.f_time = order_infos(usuario.status)
        
        parameters.start_time = edit_time(parameters.start_time) # TRANSFORMA EM STRING SEM :
        parameters.f_time = edit_time(parameters.f_time)
        
        open_time() # ABRE A ENTRADA DE TEMPOS SE NAO ESTIVER ABERTA E LOGIN
        
        if usuario.status == "varios_dias":
            is_sucess = process_multiple_days(parameters.start_date,parameters.final_date)
        
        else:
            is_sucess = receive_sige_keys(usuario.status) # MANDA AS INFORMAÇOES
        
        # SE O TEMPO FOR FEITO CORRETO ATUALIZA AS INFORMAÇÕES NO DATABASE
        if is_sucess:
            if usuario.status != "entrou":
                usuario.status = "saiu"
            #if not edituser_info:
            edit_user_infos(usuario.id,"Asstec",usuario.asstec) # atualiza db
            edit_user_infos(usuario.id,"Etapa",usuario.etapa)
            edit_user_infos(usuario.id,"Status",usuario.status)
            
            self.text_snack_bar("TEMPO ADICIONADO COM SUCESSO","ok")

            #TODO QUANDO N POEM SENHA N DA PRA FAZER LOGIN
            #TODO PROBLEMA AO ENTRAR VARIOS DIAS (SE PERDE?)
            #TODO AO ABRIR O SIGE ABRIR ABA ESTOQUE
            #TODO AO ABRIR O SIGE OU TEMPO, PRIMEIRO FECHAR SE JA TIVER ABERTO PRA EVITAR ERROS