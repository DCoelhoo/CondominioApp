import flet as ft
from controllers.config_manager import carregar_config, salvar_config

def config_view(page, home_view):
    dados = carregar_config()

    nome_field = ft.TextField(label="Nome do Condomínio", value=dados.get("nome_condominio", ""), width=400)
    morada_field = ft.TextField(label="Morada", value=dados.get("morada", ""), width=400)
    local_field = ft.TextField(label="Localidade", value=dados.get("localidade", ""), width=300)
    cp_field = ft.TextField(label="Código Postal", value=dados.get("codigo_postal", ""), width=200)
    nif_field = ft.TextField(label="NIF", value=dados.get("nif", ""), width=200)
    email_field = ft.TextField(label="Email", value=dados.get("email", ""), width=300)
    tel_field = ft.TextField(label="Telefone", value=dados.get("telefone", ""), width=200)
    fax_field = ft.TextField(label="Fax", value=dados.get("fax", ""), width=200)
    logo_field = ft.TextField(label="Caminho do Logotipo", value=dados.get("logo", ""), width=400)

    def guardar(e):
        novos_dados = {
            "nome_condominio": nome_field.value.strip(),
            "morada": morada_field.value.strip(),
            "localidade": local_field.value.strip(),
            "codigo_postal": cp_field.value.strip(),
            "nif": nif_field.value.strip(),
            "email": email_field.value.strip(),
            "telefone": tel_field.value.strip(),
            "fax": fax_field.value.strip(),
            "logo": logo_field.value.strip(),
        }
        salvar_config(novos_dados)
        page.snack_bar = ft.SnackBar(ft.Text("Configurações guardadas com sucesso!"))
        page.snack_bar.open = True
        page.update()

    def voltar(e):
        page.views.clear()
        page.views.append(home_view(page))
        page.go("/")

    return ft.View(
        route="/config",
        controls=[
            ft.AppBar(
                title=ft.Text("Configurações do Condomínio"),
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar),
                bgcolor=ft.Colors.BLUE_100,
            ),
            ft.Container(
                padding=30,
                bgcolor=ft.Colors.GREY_100,
                expand=True,
                content=ft.Column(
                    [
                        ft.Text("Dados do Condomínio", size=20, weight=ft.FontWeight.BOLD),
                        nome_field,
                        morada_field,
                        ft.Row([local_field, cp_field]),
                        ft.Row([nif_field, email_field]),
                        ft.Row([tel_field, fax_field]),
                        logo_field,
                        ft.ElevatedButton("Guardar Configurações", on_click=guardar, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        ],
    )   