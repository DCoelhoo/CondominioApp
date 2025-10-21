from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


def gerar_recibo(morador, transacoes, mes, ano):
    """
    Gera um recibo em PDF para o morador e mês indicados.
    """
    os.makedirs("recibos", exist_ok=True)

    nome_ficheiro = f"recibo_{morador['apartamento']}_{ano}_{mes}.pdf"
    caminho = os.path.join("recibos", nome_ficheiro)

    doc = SimpleDocTemplate(caminho, pagesize=A4, topMargin=30, bottomMargin=20)
    elementos = []
    estilos = getSampleStyleSheet()

    # Cabeçalho
    titulo = Paragraph(f"<b>Recibo Mensal - {mes}/{ano}</b>", estilos["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 10))

    # Dados do morador
    info = (
        f"<b>Nome:</b> {morador['nome']}<br/>"
        f"<b>Apartamento:</b> {morador['apartamento']}<br/>"
        f"<b>NIF:</b> {morador['nif']}<br/>"
        f"<b>Email:</b> {morador['email']}<br/>"
        f"<b>Telemóvel:</b> {morador['telemovel']}"
    )
    elementos.append(Paragraph(info, estilos["Normal"]))
    elementos.append(Spacer(1, 15))

    # Tabela de transações
    if not transacoes:
        elementos.append(Paragraph("Sem transações neste mês.", estilos["Normal"]))
    else:
        dados = [["Data", "Tipo", "Valor (€)"]]
        total = 0
        for t in transacoes:
            dados.append([t["data"], t["tipo"].capitalize(), f"{t['valor']:.2f}"])
            total += t["valor"]

        tabela = Table(dados, colWidths=[70, 100, 100])
        tabela.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ALIGN", (2, 1), (2, -1), "RIGHT"),
                ]
            )
        )
        elementos.append(tabela)
        elementos.append(Spacer(1, 10))

        total_text = Paragraph(f"<b>Total no mês:</b> {total:.2f} €", estilos["Normal"])
        elementos.append(total_text)

    # Data de emissão
    data_emissao = datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph(f"<i>Gerado em {data_emissao}</i>", estilos["Normal"]))

    doc.build(elementos)
    return caminho