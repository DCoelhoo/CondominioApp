import flet as ft
from controllers.data_manager import carregar_dados
from ui.home_view import home_view
from ui.perfil_view import perfil_view


def main(page: ft.Page):
    page.title = "Gestão de Condomínio"
    page.window_width = 950
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START

    moradores = carregar_dados()

    # Função chamada quando se abre o perfil
    def abrir_perfil(morador):
        page.views.clear()
        perfil = perfil_view(page, morador, moradores, home_view)
        page.views.append(perfil)
        page.go("/perfil")

    # Função que atualiza a página principal (refresh)
    def carregar_home():
        page.views.clear()
        page.views.append(home_view(page, moradores, abrir_perfil))
        page.go("/")

    # Carrega a home ao iniciar
    carregar_home()


ft.app(target=main)