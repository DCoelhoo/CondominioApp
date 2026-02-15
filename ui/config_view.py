import flet as ft
from controllers.config_manager import carregar_config, guardar_config

def config_view(page, carregar_home):
    config = carregar_config()

    # Campos de entrada
    nome = ft.TextField(label="Nome do Condomínio", value=config.get("nome_condominio", ""))
    morada = ft.TextField(label="Morada", value=config.get("morada", ""))
    codigo_postal = ft.TextField(label="Código Postal", value=config.get("codigo_postal", ""))
    localidade = ft.TextField(label="Localidade", value=config.get("localidade", ""))
    nif = ft.TextField(label="NIF", value=config.get("nif", ""))
    telefone = ft.TextField(label="Telefone", value=config.get("telefone", ""))
    email = ft.TextField(label="Email", value=config.get("email", ""))
    logo = ft.TextField(label="Caminho do Logo", value=config.get("logo", ""))
    assinatura = ft.TextField(label="Caminho da Assinatura", value=config.get("assinatura", ""))

    numero_recibo = ft.TextField(
        label="Próximo número de recibo",
        value=str(config.get("numero_recibo", 0)),
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # Guardar alterações
    def guardar_alteracoes(e):
        config["nome_condominio"] = nome.value
        config["morada"] = morada.value
        config["codigo_postal"] = codigo_postal.value
        config["localidade"] = localidade.value
        config["nif"] = nif.value
        config["telefone"] = telefone.value
        config["email"] = email.value
        config["logo"] = logo.value
        config["assinatura"] = assinatura.value
        try:
            config["numero_recibo"] = int(numero_recibo.value)
        except ValueError:
            config["numero_recibo"] = 0

        guardar_config(config)
        page.snack_bar = ft.SnackBar(ft.Text("Configurações guardadas com sucesso!"), open=True)
        page.update()

    # Botões
    botoes = ft.Row(
        [
            ft.ElevatedButton(
                "Guardar alterações", 
                icon=ft.Icons.SAVE, 
                on_click=guardar_alteracoes
            ),
            ft.ElevatedButton(
                "Voltar",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: carregar_home(),
            ),     
       ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Layout
    conteudo = ft.Column(
        [
            ft.Text("Configurações do Condomínio", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            nome, morada, codigo_postal, localidade,
            nif, telefone, email,
            logo, assinatura,
            ft.Divider(),
            numero_recibo,
            ft.Divider(),
            botoes,
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        width=600,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route="/config",
        controls=[
            ft.AppBar(title=ft.Text("Configurações"), bgcolor=ft.Colors.BLUE_100, center_title=True),
            ft.Container(
                content=conteudo,
                alignment=ft.Alignment.TOP_CENTER,
                expand=True,
                padding=20,
            ),
        ],
    )