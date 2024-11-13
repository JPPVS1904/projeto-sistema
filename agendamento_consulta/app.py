from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

# Configuração do banco de dados
def init_db():
    with sqlite3.connect("agendamentos.db") as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS consultas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, telefone TEXT, data TEXT, horario TEXT)"
        )

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/agendar", methods=["POST"])
def agendar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    telefone = request.form.get("telefone")
    data = request.form.get("data")
    horario = request.form.get("horario")

    with sqlite3.connect("agendamentos.db") as conn:
        cursor = conn.cursor()
        # Verificar se o horário já está reservado
        cursor.execute("SELECT * FROM consultas WHERE data = ? AND horario = ?", (data, horario))
        agendamento_existente = cursor.fetchone()
        
        if agendamento_existente:
            flash("Este horário já está reservado. Por favor, escolha outro horário.")
            return redirect(url_for("index"))
        
        # Inserir o novo agendamento se o horário estiver disponível
        conn.execute(
            "INSERT INTO consultas (nome, email, telefone, data, horario) VALUES (?, ?, ?, ?, ?)",
            (nome, email, telefone, data, horario),
        )
        flash("Agendamento realizado com sucesso!")

    return redirect(url_for("dashboard"))

@app.route("/admin")
def admin():
    # Conectando ao banco de dados para buscar todos os agendamentos
    with sqlite3.connect("agendamentos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultas")
        agendamentos = cursor.fetchall()
    
    return render_template("admin.html", agendamentos=agendamentos)

@app.route("/cancelar/<int:agendamento_id>")
def cancelar_agendamento(agendamento_id):
    # Conectar ao banco e deletar o agendamento pelo ID
    with sqlite3.connect("agendamentos.db") as conn:
        conn.execute("DELETE FROM consultas WHERE id = ?", (agendamento_id,))
        flash("Agendamento cancelado com sucesso!")
    
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
