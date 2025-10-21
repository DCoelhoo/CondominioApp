import flet as ft
from controllers.data_manager import carregar_dados, salvar_dados


def main(page: ft.Page):
    page.title = "Gestão de Condomínio"
    page.window_width = 900
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START

    moradores = carregar_dados()

    # ---------------------------------------------------------
    # Página principal
    # ---------------------------------------------------------
    def home_view():
        lista = ft.Column(scroll=ft.ScrollMode.AUTO)

        for morador in moradores:
            lista.controls.append(
                ft.ElevatedButton(
                    text=f"{morador['apartamento']} — {morador['nome'] if morador['nome'] != '—' else '(sem nome)'}  |  Saldo: {morador['saldo']:.2f}€",
                    on_click=lambda e, m=morador: abrir_perfil(m),
                    width=500,
                )
            )

        view = ft.View(
            route="/",
            controls=[
                ft.AppBar(
                    title=ft.Text("Gestão de Condomínio"),
                    center_title=True,
                ),
                ft.Container(content=lista, padding=20, expand=True),
            ],
        )
        return view

    # ---------------------------------------------------------
    # Página de perfil
    # ---------------------------------------------------------
    def abrir_perfil(morador):
        # limpa todas as views anteriores (para não herdar AppBar)
        page.views.clear()

        nome_field = ft.TextField(label="Nome", value=morador.get("nome", ""))
        nif_field = ft.TextField(label="NIF", value=morador.get("nif", ""))
        email_field = ft.TextField(label="Email", value=morador.get("email", ""))
        tel_field = ft.TextField(label="Telemóvel", value=morador.get("telemovel", ""))
        saldo_text = ft.Text(f"Saldo atual: {morador['saldo']:.2f}€", size=16, weight=ft.FontWeight.BOLD)

        def guardar_edicao(e):
            morador["nome"] = nome_field.value.strip() or "—"
            morador["nif"] = nif_field.value.strip()
            morador["email"] = email_field.value.strip()
            morador["telemovel"] = tel_field.value.strip()

            salvar_dados(moradores)
            page.go("/")  # volta para a principal

        def voltar(e):
            page.views.clear()
            page.views.append(home_view())
            page.go("/")

        perfil_view = ft.View(
            route="/perfil",
            controls=[
                ft.AppBar(
                    title=ft.Text(f"Perfil - {morador['apartamento']}"),
                    leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            nome_field,
                            nif_field,
                            email_field,
                            tel_field,
                            ft.Divider(),
                            saldo_text,
                            ft.ElevatedButton("Guardar alterações", on_click=guardar_edicao),
                        ],
                        spacing=10,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=20,
                    expand=True,
                ),
            ],
        )

        page.views.append(perfil_view)
        page.go("/perfil")

    # ---------------------------------------------------------
    # Inicialização
    # ---------------------------------------------------------
    page.views.clear()
    page.views.append(home_view())
    page.go("/")


ft.app(target=main)