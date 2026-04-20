from flask import Flask, render_template, request, session
import google.genai as genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.route('/')
def inicio():
    return render_template('index.html', historico = session.get('historico', []))

@app.route('/chat', methods=['POST'])
def chat():
    pergunta = request.form['mensagem']
    response = client.models.generate_content(
    model = "gemini-3-flash-preview",
    contents = pergunta,
    config = types.GenerateContentConfig(
        system_instruction = "Sempre responda em português, seja breve e educado nas respostas, se a pergunta for em outro idioma, responda que você só entende em português."
    )
    )
    if "historico" not in session:
        session['historico'] = []

    session['historico'].append({"autor": "usuario", "texto": pergunta})
    session['historico'].append({"autor": "IA", "texto": response.text})
    return render_template("index.html", historico = session["historico"])
    
if __name__ == '__main__':
    app.run(debug=True)
