import flet as ft

from app import App

window_size_height = 750
window_size_width = 450

def main(page:ft.Page):
    page.window.height = window_size_height
    page.window.width = window_size_width
    page.window.max_height = window_size_height+5
    page.window.max_width = window_size_width+5
    page.window.min_height = window_size_height-5
    page.window.min_width = window_size_width-5
    page.theme_mode = "dark"
    page.title = "AutoPyme - Entrada de tempos"
    page.add(App(page=page))


ft.app(main)
