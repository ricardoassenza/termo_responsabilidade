from flask import Flask, request, render_template
import pandas as pd
from datetime import datetime
import os
from reportlab.pdfgen import canvas

ARQUIVO_EXCEL = r"data/Nomes.xlsx"

app = Flask(__name__)

# Criar pasta de PDFs se não existir
if not os.path.exists("pdfs"):
    os.makedirs("pdfs")


def gerar_pdf(nome, cpf, equipamento, data_hora):
    caminho_pdf = f"pdfs/{cpf}.pdf"
    c = canvas.Canvas(caminho_pdf)

    c.setFont("Helvetica", 12)
    c.drawString(50, 800, "Comprovante de Assinatura - Termo de Responsabilidade")
    c.drawString(50, 760, f"Nome: {nome}")
    c.drawString(50, 740, f"CPF: {cpf}")
    c.drawString(50, 720, f"Equipamento: {equipamento}")
    c.drawString(50, 700, f"Data/Hora da Confirmação: {data_hora}")

    c.save()
    return caminho_pdf


@app.route("/confirmar")
def confirmar():
    cpf = request.args.get("cpf")

    if not cpf:
        return "CPF não informado.", 400

    df = pd.read_excel(ARQUIVO_EXCEL)

    linha = df.index[df["Cpf"].astype(str) == str(cpf)]

    if len(linha) == 0:
        return "CPF não encontrado.", 404

    idx = linha[0]

    nome = df.at[idx, "Nome"]
    equipamento = df.at[idx, "Equipamento"]
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    df.at[idx, "Feita"] = data_hora
    df.to_excel(ARQUIVO_EXCEL, index=False)

    gerar_pdf(nome, cpf, equipamento, data_hora)

    return render_template("confirmado.html", nome=nome, data=data_hora)


@app.route("/")
def home():
    return "Servidor Funcionando!"


if __name__ == "__main__":
    app.run(debug=True)
