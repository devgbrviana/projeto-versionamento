import requests
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


conn = sqlite3.connect('projeto_rpa.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS piadas_chuck (
    id TEXT PRIMARY KEY,
    piada TEXT,
    categoria TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dados_processados (
    id TEXT PRIMARY KEY,
    piada TEXT,
    palavra_chave TEXT
)
''')

conn.commit()

def coletar_piadas(qtd=100):
    piadas = []
    for _ in range(qtd):
        response = requests.get("https://api.chucknorris.io/jokes/random")
        if response.status_code == 200:
            data = response.json()
            id = data['id']
            piada = data['value']
            categoria = data.get('categories')
            categoria = categoria[0] if categoria else 'Sem categoria'
            piadas.append((id, piada, categoria))
    return piadas


def salvar_piadas(piadas):
    for id, piada, categoria in piadas:
        cursor.execute('''
            INSERT OR IGNORE INTO piadas_chuck (id, piada, categoria)
            VALUES (?, ?, ?)
        ''', (id, piada, categoria))
    conn.commit()


def processar_piadas():
    cursor.execute('SELECT id, piada FROM piadas_chuck')
    todas_piadas = cursor.fetchall()

    for id, texto in todas_piadas:
        if re.search(r'\bChuck\b', texto, re.IGNORECASE):
            cursor.execute('''
                INSERT OR IGNORE INTO dados_processados (id, piada, palavra_chave)
                VALUES (?, ?, ?)
            ''', (id, texto, 'Chuck'))
    conn.commit()


def enviar_email():
    try:
       
        remetente = "gbr.vianas@gmail.com"
        senha = "cmqb vjhe tefb cbwk" 
        destinatario = "gbr.vianas@gmail.com"
        assunto = "Relatório - Projeto RPA (Chuck Norris)"

        cursor.execute('SELECT COUNT(*) FROM piadas_chuck')
        total_coletadas = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM dados_processados')
        total_processadas = cursor.fetchone()[0]
        cursor.execute('SELECT piada FROM dados_processados')
        piadas = cursor.fetchall()
        piadas_texto = "\n\n".join([f"- {p[0]}" for p in piadas])

        corpo_email = f"""
Relatório do Projeto RPA

Total de piadas coletadas: {total_coletadas}
Total de piadas com a palavra "Chuck": {total_processadas}

Piadas processadas:
{piadas_texto}
"""

        print("📤 Enviando e-mail...")

       
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto
        mensagem.attach(MIMEText(corpo_email, 'plain'))

       
        servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_email.starttls()
        servidor_email.login(remetente, senha)
        servidor_email.send_message(mensagem)
        servidor_email.quit()

        print("✅ Email enviado com sucesso!")

    except Exception as erro:
        print(f"❌ Erro ao enviar o e-mail: {erro}")

if __name__ == "__main__":
    print("🔄 Coletando piadas...")
    piadas = coletar_piadas(10)
    salvar_piadas(piadas)
    print("✅ Piadas salvas no banco.")

    print("🔍 Processando com regex...")
    processar_piadas()
    print("✅ Dados processados salvos.")

    enviar_email()
