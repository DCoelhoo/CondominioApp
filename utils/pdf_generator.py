from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os
from controllers.config_manager import carregar_config


def gerar_recibo(morador, transacoes_mes, mes, ano):
    config = carregar_config()

    pasta_recibos = "recibos"
    os.makedirs(pasta_recibos, exist_ok=True)

    caminho_pdf = os.path.join(
        pasta_recibos,
        f"recibo_{morador['apartamento'].replace(' ', '_')}_{ano}_{mes:02d}.pdf"
    )

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    elementos = []
    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "Titulo",
        parent=estilos["Heading1"],
        fontSize=14,
        alignment=1,  # Centralizado na página
        spaceAfter=12,
        leading=16
    )

    estilo_info = ParagraphStyle(
        "Info",
        parent=estilos["Normal"],
        fontSize=10,
        leading=13,
    )

    estilo_admin = ParagraphStyle(
        "Admin",
        parent=estilos["Normal"],
        fontSize=10,
        leading=13,
        alignment=2  # Alinhado à direita
    )

    # ---------- CABEÇALHO ----------
    logo_path = config.get("logo")
    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5 * cm, height=2.5 * cm, kind="proportional")
    else:
        logo = Paragraph("<b>LOGO</b>", estilos["Normal"])

    # Tabela só com o logo à esquerda
    cabecalho = Table([[logo]], colWidths=[3 * cm])
    cabecalho.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elementos.append(cabecalho)

    # Título e data centrados em toda a página
    elementos.append(Paragraph("<b>Recibo de Condomínio</b>", estilo_titulo))
    elementos.append(Paragraph(f"Data de emissão: {datetime.now().strftime('%d-%m-%Y')}", estilo_info))
    elementos.append(Spacer(1, 0.7 * cm))

    # ---------- BLOCO CONDOMÍNIO E MORADOR ----------
    bloco_condominio = f"""
    <b>{config.get('nome_condominio', 'Condomínio')}</b><br/>
    {config.get('morada', '')}<br/>
    {config.get('codigo_postal', '')} {config.get('localidade', '')}<br/>
    NIF: {config.get('nif', '')}<br/>
    Tel: {config.get('telefone', '')}<br/>
    Email: {config.get('email', '')}
    """

    bloco_morador = f"""
    <b>Unidade:</b> {morador.get('apartamento')}<br/>
    <b>Nome:</b> {morador.get('nome', '')}<br/>
    <b>NIF:</b> {morador.get('nif', '')}<br/>
    <b>Email:</b> {morador.get('email', '')}<br/>
    <b>Telemóvel:</b> {morador.get('telemovel', '')}
    """

    blocos = Table(
        [[Paragraph(bloco_condominio, estilo_info),
          Paragraph(bloco_morador, estilo_info)]],
        colWidths=[8 * cm, 8 * cm]
    )
    blocos.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.append(blocos)
    elementos.append(Spacer(1, 0.8 * cm))

    # ---------- TABELA DE TRANSAÇÕES ----------
    dados_tabela = [["Data", "Tipo", "Valor (€)"]]
    total = 0.0
    for t in sorted(transacoes_mes, key=lambda x: x["data"]):
        dados_tabela.append([
            t["data"],
            t["tipo"].capitalize(),
            f"{t['valor']:.2f}"
        ])
        total += t["valor"]

    dados_tabela.append(["", "Total", f"{total:.2f} €"])

    tabela = Table(dados_tabela, colWidths=[5 * cm, 7 * cm, 3 * cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (1, -1), (-1, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 1 * cm))

    # ---------- TOTAL ----------
    elementos.append(Paragraph(f"<b>Total Liquidado:</b> {total:.2f} €", estilo_info))
    elementos.append(Spacer(1, 1.2 * cm))

    # ---------- ASSINATURA À DIREITA ----------
    assinatura_path = config.get("assinatura")
    assinatura_table_data = []

    assinatura_table_data.append([Paragraph("<b>O Administrador</b>", estilo_admin)])

    if assinatura_path and os.path.exists(assinatura_path):
        assinatura_img = Image(assinatura_path, width=4 * cm, height=2 * cm, kind="proportional")
        assinatura_table_data.append([assinatura_img])
        assinatura_table_data.append([Spacer(1, 0.2 * cm)])

    assinatura_table_data.append([
        Paragraph(f"<b>{config.get('nome_condominio', 'Condomínio')}</b>", estilo_admin)
    ])

    assinatura_table = Table(assinatura_table_data, colWidths=[16 * cm])  # move tudo à direita
    assinatura_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elementos.append(assinatura_table)

    doc.build(elementos)
    return caminho_pdf