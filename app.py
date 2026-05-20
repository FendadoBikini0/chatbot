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
    if "historico" not in session:
        session['historico'] = []

    if "contexto" not in session:
        session['contexto'] = []

    # create chat with model and existing context
    chat = client.chats.create(
        model="gemini-3-flash-preview",
        history=session['contexto']
    )

    # send the user's message and get response
    response = chat.send_message(pergunta)


    session['historico'].append({"autor": "usuario", "texto": pergunta})
    session['historico'].append({"autor": "IA", "texto": response.text})
    session['contexto'].append({"role": "user", "parts": [{"text": pergunta}]})
    session['contexto'].append({"role": "model", "parts": [{"text": response.text}]})
    session.modified = True
    return render_template("index.html", historico = session["historico"])
    
if __name__ == '__main__':
    app.run(debug=True)
