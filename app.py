from flask import Flask, request, render_template
import csv
from datetime import datetime
import os

app = Flask(__name__)

ARQUIVO = "confirmacoes.csv"

# Garante o CSV com cabeçalho
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cpf", "nome", "data_hora"])

@app.route("/confirmar")
def confirmar():
    cpf = request.args.get("cpf")
    nome = request.args.get("nome", "")
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Salvar no CSV
    with open(ARQUIVO, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([cpf, nome, data_hora])

    return render_template("confirmado.html", nome=nome or "Usuário", data=data_hora)

@app.route("/")
def home():
    return "Servidor Funcionando!"

if __name__ == "__main__":
    app.run()
