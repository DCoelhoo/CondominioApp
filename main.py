import flet as ft
from datetime import date
from controllers.data_manager import carregar_dados, salvar_dados
from utils.pdf_generator import gerar_recibo
import webbrowser



def main(page: ft.Page):
    page.title = "Gestão de Condomínio"
    page.window_width = 950
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START

    moradores = carregar_dados()

    # ---------------------------------------------------------
    # Página principal
    # ---------------------------------------------------------
    def home_view():
        lista = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
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
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                padding=15,
                width=600,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
                on_click=lambda e: abrir_perfil(morador),
            )

            # efeito hover
            def ao_hover(e):
                if e.data == "true":
                    card.bgcolor = ft.Colors.BLUE_50
                    card.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK))
                else:
                    card.bgcolor = ft.Colors.WHITE
                    card.shadow = ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
                card.update()

            card.on_hover = ao_hover
            return card

        for morador in moradores:
            lista.controls.append(criar_card(morador))

        view = ft.View(
            route="/",
            controls=[
                ft.AppBar(
                    title=ft.Text("Gestão de Condomínio", size=22, weight=ft.FontWeight.BOLD),
                    center_title=True,
                    bgcolor=ft.Colors.BLUE_100,
                ),
                ft.Container(
                    content=lista,
                    alignment=ft.alignment.center,
                    expand=True,
                    bgcolor=ft.Colors.GREY_100,
                ),
            ],
        )
        return view

    # ---------------------------------------------------------
    # Página de perfil
    # ---------------------------------------------------------
    def abrir_perfil(morador):
        page.views.clear()

        # ---------- CAMPOS DE PERFIL ----------
        nome_field = ft.TextField(label="Nome", value=morador.get("nome", ""), width=350)
        nif_field = ft.TextField(label="NIF", value=morador.get("nif", ""), width=250)
        email_field = ft.TextField(label="Email", value=morador.get("email", ""), width=350)
        tel_field = ft.TextField(label="Telemóvel", value=morador.get("telemovel", ""), width=250)

        saldo_text = ft.Text(
            f"Saldo atual: {morador['saldo']:.2f}€",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="green" if morador["saldo"] >= 0 else "red",
        )

        # ---------- HISTÓRICO ----------
        transacoes_list = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO)

        def atualizar_transacoes():
            transacoes_list.controls.clear()
            if not morador["transacoes"]:
                transacoes_list.controls.append(ft.Text("Sem transações registadas."))
            else:
                for t in sorted(morador["transacoes"], key=lambda x: x["data"], reverse=True):
                    cor = "green" if t["valor"] > 0 else "red"
                    transacoes_list.controls.append(
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(t["data"], width=100),
                                    ft.Text(t["tipo"].capitalize(), width=150),
                                    ft.Text(f"{t['valor']:.2f}€", color=cor, width=100),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=10,
                            border_radius=8,
                            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                        )
                    )
            page.update()

        atualizar_transacoes()

        # ---------- ADICIONAR TRANSAÇÃO ----------
        tipo_dropdown = ft.Dropdown(
            label="Tipo",
            options=[ft.dropdown.Option("pagamento"), ft.dropdown.Option("despesa")],
            value="pagamento",
            width=180,
        )
        valor_field = ft.TextField(label="Valor (€)", width=150)
        data_field = ft.TextField(label="Data", value=str(date.today()), width=150)

        def adicionar_transacao(e):
            try:
                valor = float(valor_field.value)
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Valor inválido."))
                page.snack_bar.open = True
                page.update()
                return

            if tipo_dropdown.value == "despesa":
                valor = -abs(valor)

            nova_transacao = {"data": data_field.value, "tipo": tipo_dropdown.value, "valor": valor}
            morador["transacoes"].append(nova_transacao)
            morador["saldo"] += valor
            salvar_dados(moradores)
            saldo_text.value = f"Saldo atual: {morador['saldo']:.2f}€"
            valor_field.value = ""
            atualizar_transacoes()
            page.update()

        # ---------- GERAR RECIBO ----------
        mes_field = ft.TextField(label="Mês (1-12)", width=100)
        ano_field = ft.TextField(label="Ano", value=str(date.today().year), width=120)

        def gerar_pdf(e):
            try:
                mes = int(mes_field.value)
                ano = int(ano_field.value)
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Mês/Ano inválidos"))
                page.snack_bar.open = True
                page.update()
                return

            transacoes_mes = [t for t in morador["transacoes"] if t["data"].startswith(f"{ano}-{mes:02d}")]
            caminho = gerar_recibo(morador, transacoes_mes, mes, ano)
            webbrowser.open(f"file://{caminho}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Recibo gerado: {caminho}"))
            page.snack_bar.open = True
            page.update()

        # ---------- GUARDAR ----------
        def guardar_edicao(e):
            morador["nome"] = nome_field.value.strip() or "—"
            morador["nif"] = nif_field.value.strip()
            morador["email"] = email_field.value.strip()
            morador["telemovel"] = tel_field.value.strip()
            salvar_dados(moradores)
            page.go("/")

        def voltar(e):
            page.views.clear()
            page.views.append(home_view())
            page.go("/")

        # ---------- ORGANIZAÇÃO VISUAL ----------
        perfil_view = ft.View(
            route="/perfil",
            controls=[
                ft.AppBar(
                    title=ft.Text(f"Perfil — {morador['apartamento']}"),
                    leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar),
                    bgcolor=ft.Colors.BLUE_100,
                ),
                ft.Container(
                    padding=30,
                    expand=True,
                    bgcolor=ft.Colors.GREY_100,
                    content=ft.Column(
                        [
                            ft.Container(
                                bgcolor=ft.Colors.WHITE,
                                border_radius=12,
                                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
                                padding=20,
                                content=ft.Column(
                                    [
                                        ft.Text("Dados do Morador", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                                        ft.Row([nome_field, nif_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                        ft.Row([email_field, tel_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ],
                                    spacing=10,
                                ),
                            ),
                            ft.Container(
                                bgcolor=ft.Colors.WHITE,
                                border_radius=12,
                                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK)),
                                padding=20,
                                content=ft.Column(
                                    [
                                        saldo_text,
                                        ft.Divider(),
                                        ft.Text("Adicionar Transação", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                                        ft.Row([tipo_dropdown, valor_field, data_field, ft.ElevatedButton("Adicionar", on_click=adicionar_transacao)]),
                                    ],
                                    spacing=10,
                                ),
                            ),
                            ft.Container(
                                bgcolor=ft.Colors.WHITE,
                                border_radius=12,
                                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK)),
                                padding=20,
                                content=ft.Column(
                                    [
                                        ft.Text("Gerar Recibo Mensal", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                                        ft.Row([mes_field, ano_field, ft.ElevatedButton("Gerar PDF", on_click=gerar_pdf)]),
                                    ],
                                    spacing=10,
                                ),
                            ),
                            ft.Container(
                                bgcolor=ft.Colors.WHITE,
                                border_radius=12,
                                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK)),
                                padding=20,
                                content=ft.Column(
                                    [
                                        ft.Text("Histórico de Transações", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                                        transacoes_list,
                                    ],
                                    spacing=10,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Guardar Alterações",
                                on_click=guardar_edicao,
                                bgcolor=ft.Colors.BLUE_400,
                                color=ft.Colors.WHITE,
                                width=200,
                            ),
                        ],
                        spacing=25,
                        scroll=ft.ScrollMode.AUTO,
                    ),
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