import flet as ft
from datetime import date
from controllers.despesa_geral import lancar_quota_mensal


def home_view(page, moradores, abrir_perfil, abrir_config):
    hoje = date.today()

    # LISTA DE CARDS
    lista = ft.Column(spacing=10)

    mes_dd = ft.Dropdown(
        label="Mês",
        value=str(hoje.month),
        options=[ft.dropdown.Option(str(i)) for i in range(1, 13)],
        width=120,
    )
    ano_tf = ft.TextField(
        label="Ano",
        value=str(hoje.year),
        width=120,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def fechar_dialog(e=None):
        dlg.open = False
        page.update()

    def confirmar_lancamento(e):
        try:
            mes = int(mes_dd.value)
            ano = int(ano_tf.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Mês/Ano inválidos."), open=True)
            page.update()
            return

        adicionadas, ignoradas = lancar_quota_mensal(moradores, ano, mes)
        fechar_dialog()

        page.snack_bar = ft.SnackBar(
            ft.Text(f"Quotas lançadas: {adicionadas}. Já existiam: {ignoradas}."),
            open=True,
        )
        page.update()

        # atualizar lista
        lista.controls.clear()
        for morador in moradores:
            lista.controls.append(criar_card(morador))
        lista.update()

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Adicionar quota mensal"),
        content=ft.Column([mes_dd, ano_tf], tight=True, spacing=10),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_dialog),
            ft.ElevatedButton("Lançar", on_click=confirmar_lancamento),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_dialog(e):
        if dlg not in page.overlay:
            page.overlay.append(dlg)
        dlg.open = True
        page.update()

    btn_quota = ft.ElevatedButton(
        "Adicionar quota mensal",
        icon=ft.Icons.EVENT_REPEAT,
        on_click=abrir_dialog,
    )

    def criar_card(morador):
        card = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        f"{morador['apartamento']} — {morador['nome'] if morador['nome'] != '—' else '(sem nome)'}",
                        size=16,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        f"Saldo: {morador['saldo']:.2f}€",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color="green" if morador["saldo"] >= 0 else "red",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                blur_radius=5,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
            padding=15,
            width=600,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_click=lambda e, m=morador: abrir_perfil(m),
            ink=True,
        )

        def on_hover(e, c=card):
            c.bgcolor = ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.WHITE
            page.update()

        card.on_hover = on_hover
        return card

    # preencher lista inicial
    for morador in moradores:
        lista.controls.append(criar_card(morador))

    # Container centralizado com scroll
    lista_container = ft.Container(
        content=ft.Column(
            [
                btn_quota,  # botão visível na home
                lista,
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
        ),
        alignment=ft.Alignment.TOP_CENTER,
        padding=20,
        expand=True,
    )

    main_container = ft.Container(
        content=lista_container,
        bgcolor=ft.Colors.GREY_100,
        expand=True,
    )

    return ft.View(
        route="/",
        padding=0,
        spacing=0,
        controls=[
            ft.AppBar(
                title=ft.Text("Gestão de Condomínio", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.BLUE_100,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        tooltip="Configurações do Condomínio",
                        on_click=lambda e: abrir_config(),
                    ),
                ],
            ),
            main_container,
        ],
    )
