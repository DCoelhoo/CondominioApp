import flet as ft
from datetime import date
import webbrowser
from utils.pdf_generator import gerar_recibo
from controllers.data_manager import guardar_dados

def perfil_view(page, morador, moradores, home_view):
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

    # ---------- HISTÓRICO DE TRANSAÇÕES ----------
    transacoes_list = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO)

    def render_transacoes():
        transacoes_list.controls.clear()
        if not morador["transacoes"]:
            transacoes_list.controls.append(ft.Text("Sem transações registadas."))
        else:
            for idx, (index_real, transacao) in enumerate(
                sorted(enumerate(morador["transacoes"]), key=lambda x: x[1]["data"], reverse=True)
            ):
                cor = "green" if transacao["valor"] > 0 else "red"

                def remover_click(e, i=index_real):
                    apagar_transacao(i)

                btn_apagar = ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.RED_400,
                    tooltip="Apagar transação",
                    on_click=remover_click,
                )

                transacoes_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(transacao["data"], width=100),
                                ft.Text(transacao["tipo"].capitalize(), width=150),
                                ft.Text(f"{transacao['valor']:.2f}€", color=cor, width=100),
                                btn_apagar,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=10,
                        border_radius=8,
                        bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                    )
                )
        transacoes_list.update()

    def apagar_transacao(index):
        morador["saldo"] -= morador["transacoes"][index]["valor"]
        del morador["transacoes"][index]

        # ✅ Corrige possíveis -0.0€
        if abs(morador["saldo"]) < 0.005:
            morador["saldo"] = 0.0

        guardar_dados(moradores)

        saldo_text.value = f"Saldo atual: {morador['saldo']:.2f}€"
        saldo_text.color = "green" if morador["saldo"] >= 0 else "red"
        saldo_text.update()

        render_transacoes()

        page.snack_bar = ft.SnackBar(ft.Text("Transação apagada."))
        page.snack_bar.open = True
        page.update()

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

        nova_transacao = {
            "data": data_field.value.strip(),
            "tipo": tipo_dropdown.value,
            "valor": valor,
        }

        morador["transacoes"].append(nova_transacao)
        morador["saldo"] += valor

        # ✅ Corrige possíveis -0.0€
        if abs(morador["saldo"]) < 0.005:
            morador["saldo"] = 0.0

        guardar_dados(moradores)

        saldo_text.value = f"Saldo atual: {morador['saldo']:.2f}€"
        saldo_text.color = "green" if morador["saldo"] >= 0 else "red"
        saldo_text.update()

        valor_field.value = ""
        render_transacoes()

        page.snack_bar = ft.SnackBar(ft.Text("Transação adicionada."))
        page.snack_bar.open = True
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
        guardar_dados(moradores)

        page.snack_bar = ft.SnackBar(ft.Text("Alterações guardadas com sucesso!"))
        page.snack_bar.open = True

        # Voltar à home
        page.views.clear()
        page.views.append(home_view(page, moradores, abrir_perfil))
        page.go("/")

    def voltar(e):
        page.views.clear()
        page.views.append(home_view(page, moradores, abrir_perfil))
        page.go("/")

    def abrir_perfil(m):
        page.views.clear()
        page.views.append(perfil_view(page, m, moradores, home_view))
        page.go("/perfil")

    # ---------- VISUAL ----------
    perfil_page = ft.View(
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
                            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK)),
                            padding=20,
                            content=ft.Column(
                                [
                                    ft.Text("Dados do Morador", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                                    ft.Row([nome_field, nif_field]),
                                    ft.Row([email_field, tel_field]),
                                ],
                                spacing=10,
                            ),
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            padding=20,
                            content=ft.Column(
                                [
                                    saldo_text,
                                    ft.Text("Adicionar Transação", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                                    ft.Row([tipo_dropdown, valor_field, data_field, ft.ElevatedButton("Adicionar", on_click=adicionar_transacao)]),
                                ],
                                spacing=10,
                            ),
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
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

    # ✅ Adiciona a view normalmente
    page.add(perfil_page)
    page.update()

    # ✅ Renderiza as transações de forma segura após o ciclo atual
    async def post_mount():
        render_transacoes()
        page.update()

    page.run_task(post_mount)

    return perfil_page