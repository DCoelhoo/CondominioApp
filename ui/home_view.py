import flet as ft

def home_view(page, moradores, abrir_perfil):
    lista = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    for morador in moradores:
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

        # Efeito hover
        def on_hover(e, c=card):
            c.bgcolor = ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.WHITE
            page.update()

        card.on_hover = on_hover
        lista.controls.append(card)

    # Container centralizado
    lista_container = ft.Container(
        content=lista,
        alignment=ft.alignment.top_center,
        padding=20,
        expand=True,
    )

    # Scroll vertical suave
    main_container = ft.Container(
        content=ft.ListView(
            controls=[lista_container],
            expand=True,
            spacing=10,
            padding=20,
        ),
        bgcolor=ft.Colors.GREY_100,
        expand=True,
    )

    return ft.View(
        route="/",
        controls=[
            ft.AppBar(
                title=ft.Text("Gestão de Condomínio", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.BLUE_100,
            ),
            main_container,
        ],
    )