import flet as ft
import os
from datetime import date
from controllers.despesa_geral import lancar_quota_mensal
from controllers.data_manager import guardar_moradores
from utils.storage import get_recibos_dir


def home_view(page, moradores, abrir_perfil, abrir_config):
    hoje = date.today()

    modo_visualizacao = {"valor": "lista"}
    lista_container_dinamico = ft.Container()

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

    def criar_card_lista(morador):
        tem_garagem = morador.get("tem_garagem", False)

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
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
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.DIRECTIONS_CAR,
                                size=18,
                                color=ft.Colors.GREEN if tem_garagem else ft.Colors.GREY,
                            ),
                            ft.Text(
                                "Tem garagem" if tem_garagem else "Sem garagem",
                                size=13,
                                color=ft.Colors.BLACK54,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=8,
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

    def criar_card_mosaico(morador):
        tem_garagem = morador.get("tem_garagem", False)

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        morador["apartamento"],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        morador["nome"] if morador["nome"] != "—" else "(sem nome)",
                        size=14,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Saldo: {morador['saldo']:.2f}€",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color="green" if morador["saldo"] >= 0 else "red",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.DIRECTIONS_CAR,
                                size=18,
                                color=ft.Colors.GREEN if tem_garagem else ft.Colors.GREY,
                            ),
                            ft.Text(
                                "Garagem" if tem_garagem else "Sem garagem",
                                size=12,
                                color=ft.Colors.BLACK54,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
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
            width=260,
            height=160,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_click=lambda e, m=morador: abrir_perfil(m),
            ink=True,
        )

        def on_hover(e, c=card):
            c.bgcolor = ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.WHITE
            page.update()

        card.on_hover = on_hover
        return ft.Column(
            [card],
            col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def renderizar_moradores():
        if modo_visualizacao["valor"] == "lista":
            lista = ft.Column(
                [criar_card_lista(morador) for morador in moradores],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            lista_container_dinamico.content = ft.Container(
                content=lista,
                alignment=ft.Alignment.TOP_CENTER,
                expand=True,
            )
        else:
            mosaico = ft.ResponsiveRow(
                [criar_card_mosaico(morador) for morador in moradores],
                alignment=ft.MainAxisAlignment.CENTER,
                run_spacing=12,
                spacing=12,
            )
            lista_container_dinamico.content = mosaico

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
        renderizar_moradores()

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

    def abrir_pasta_recibos(e):
        pasta = get_recibos_dir()
        os.startfile(pasta)

    def abrir_form_morador(page):
        nome_tf = ft.TextField(label="Nome", width=350)
        apartamento_tf = ft.TextField(label="Apartamento", width=200)
        garagem_cb = ft.Checkbox(label="Tem garagem", value=False)

        def fechar_form(e=None):
            form_dlg.open = False
            page.update()

        def guardar_morador(e):
            nome = (nome_tf.value or "").strip()
            apartamento = (apartamento_tf.value or "").strip()

            if not apartamento:
                page.snack_bar = ft.SnackBar(
                    ft.Text("O campo Apartamento é obrigatório."),
                    open=True,
                )
                page.update()
                return

            novo_morador = {
                "nome": nome if nome else "—",
                "apartamento": apartamento,
                "saldo": 0.0,
                "tem_garagem": garagem_cb.value or False,
                "movimentos": [],
            }

            moradores.append(novo_morador)
            guardar_moradores(moradores)

            form_dlg.open = False
            renderizar_moradores()

            page.snack_bar = ft.SnackBar(
                ft.Text("Condómino adicionado com sucesso."),
                open=True,
            )
            page.update()

        form_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Adicionar condómino"),
            content=ft.Column(
                [
                    nome_tf,
                    apartamento_tf,
                    garagem_cb,
                ],
                tight=True,
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_form),
                ft.ElevatedButton("Guardar", on_click=guardar_morador),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        if form_dlg not in page.overlay:
            page.overlay.append(form_dlg)

        form_dlg.open = True
        page.update()

    def mudar_visualizacao(e):
        modo_visualizacao["valor"] = e.control.value
        renderizar_moradores()

    seletor_visualizacao = ft.RadioGroup(
        value="lista",
        on_change=mudar_visualizacao,
        content=ft.Row(
            [
                ft.Radio(value="lista", label="Lista"),
                ft.Radio(value="mosaico", label="Mosaico"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
    ) 

    btn_quota = ft.ElevatedButton(
        "Adicionar quota mensal",
        icon=ft.Icons.EVENT_REPEAT,
        on_click=abrir_dialog,
    )

    btn_adicionar = ft.ElevatedButton(
        "Adicionar Condómino",
        icon=ft.Icons.PERSON_ADD,
        on_click=lambda e: abrir_form_morador(page),
    )
    
    btn_recibos = ft.ElevatedButton(
        "Abrir pasta dos recibos",
        icon=ft.Icons.FOLDER_OPEN,
        on_click=abrir_pasta_recibos,
    )

    renderizar_moradores()

    lista_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        btn_quota,
                        btn_adicionar,
                        btn_recibos,
                        seletor_visualizacao,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    wrap=True,
                ),
                lista_container_dinamico,
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
            expand=True,
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