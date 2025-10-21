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
        lista = ft.Column(scroll=ft.ScrollMode.AUTO)

        for morador in moradores:
            lista.controls.append(
                ft.ElevatedButton(
                    text=f"{morador['apartamento']} — {morador['nome'] if morador['nome'] != '—' else '(sem nome)'}  |  Saldo: {morador['saldo']:.2f}€",
                    on_click=lambda e, m=morador: abrir_perfil(m),
                    width=550,
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
        page.views.clear()

        # campos de perfil
        nome_field = ft.TextField(label="Nome", value=morador.get("nome", ""))
        nif_field = ft.TextField(label="NIF", value=morador.get("nif", ""))
        email_field = ft.TextField(label="Email", value=morador.get("email", ""))
        tel_field = ft.TextField(label="Telemóvel", value=morador.get("telemovel", ""))
        saldo_text = ft.Text(f"Saldo atual: {morador['saldo']:.2f}€", size=16, weight=ft.FontWeight.BOLD)

        # -------------------- HISTÓRICO DE TRANSAÇÕES --------------------
        transacoes_list = ft.Column(scroll=ft.ScrollMode.AUTO)

        def atualizar_transacoes():
            transacoes_list.controls.clear()
            if not morador["transacoes"]:
                transacoes_list.controls.append(ft.Text("Sem transações registadas."))
            else:
                for t in sorted(morador["transacoes"], key=lambda x: x["data"], reverse=True):
                    cor = "green" if t["valor"] > 0 else "red"
                    transacoes_list.controls.append(
                        ft.Row(
                            [
                                ft.Text(t["data"], width=100),
                                ft.Text(t["tipo"].capitalize(), width=120),
                                ft.Text(f"{t['valor']:.2f}€", color=cor, width=100),
                            ]
                        )
                    )
            page.update()

        atualizar_transacoes()

        # -------------------- ADICIONAR TRANSAÇÃO --------------------
        tipo_dropdown = ft.Dropdown(
            label="Tipo",
            options=[ft.dropdown.Option("pagamento"), ft.dropdown.Option("despesa")],
            value="pagamento",
            width=200,
        )
        valor_field = ft.TextField(label="Valor (€)", width=150)
        data_field = ft.TextField(label="Data (YYYY-MM-DD)", value=str(date.today()), width=180)

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
            salvar_dados(moradores)
            saldo_text.value = f"Saldo atual: {morador['saldo']:.2f}€"
            valor_field.value = ""
            atualizar_transacoes()
            page.update()

        # -------------------- GERAR RECIBO --------------------
        mes_field = ft.TextField(label="Mês (1-12)", width=120)
        ano_field = ft.TextField(label="Ano (YYYY)", value=str(date.today().year), width=150)

        def gerar_pdf(e):
            try:
                mes = int(mes_field.value)
                ano = int(ano_field.value)
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Mês/Ano inválidos"))
                page.snack_bar.open = True
                page.update()
                return

            transacoes_mes = [
                t for t in morador["transacoes"]
                if t["data"].startswith(f"{ano}-{mes:02d}")
            ]

            caminho = gerar_recibo(morador, transacoes_mes, mes, ano)

            webbrowser.open(f"file://{caminho}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Recibo gerado: {caminho}"))
            page.snack_bar.open = True
            page.update()

        # -------------------- GUARDAR PERFIL --------------------
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
                            ft.Text("Dados do Morador", size=18, weight=ft.FontWeight.BOLD),
                            nome_field,
                            nif_field,
                            email_field,
                            tel_field,
                            ft.Divider(),
                            saldo_text,
                            ft.Divider(),
                            ft.Text("Adicionar Transação", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([tipo_dropdown, valor_field, data_field, ft.ElevatedButton("Adicionar", on_click=adicionar_transacao)]),
                            ft.Divider(),
                            ft.Text("Gerar Recibo Mensal", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([mes_field, ano_field, ft.ElevatedButton("Gerar PDF", on_click=gerar_pdf)]),
                            ft.Divider(),
                            ft.Text("Histórico de Transações", size=18, weight=ft.FontWeight.BOLD),
                            transacoes_list,
                            ft.Divider(),
                            ft.ElevatedButton("Guardar Alterações", on_click=guardar_edicao),
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