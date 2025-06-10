import requests
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

conexao = sqlite3.connect('chuck_norris.db')
cursor = conexao.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS piadas (
        id TEXT PRIMARY KEY,
        piada TEXT,
        categoria TEXT
    )
''')


for _ in range(10):
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        id = data['id']
        piada = data['value']
        categoria = ', '.join(data.get('categories', [])) or 'Sem categoria'

        print('PIADA COLETADA:')
        print(f'ID: {id}')
        print(f'Categoria: {categoria}')
        print(f'Texto: {piada}')
        print('-' * 50)

        cursor.execute('''
            INSERT OR REPLACE INTO piadas (
                id, piada, categoria
            ) VALUES (?, ?, ?)
        ''', (id, piada, categoria))
    else:
        print('Erro ao buscar piada.')

conexao.commit()


cursor.execute("SELECT * FROM piadas WHERE piada LIKE '%Chuck%'")
piadas_chuck = cursor.fetchall()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS piadas_chuck (
        id TEXT PRIMARY KEY,
        piada TEXT,
        categoria TEXT
    )
''')


for piada in piadas_chuck:
    cursor.execute('''
        INSERT OR REPLACE INTO piadas_chuck (
            id, piada, categoria
        ) VALUES (?, ?, ?)
    ''', piada)

conexao.commit()
conexao.close()


try:
    print('Aguarde... seu email está sendo enviado.')

    servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_email.starttls()
    servidor_email.login('gbr.vianas@gmail.com', 'cmqb vjhe tefb cbwk')  

    remetente = 'gbr.vianas@gmail.com'
    destinatarios = ['professorvandersonbossi@gmail.com']
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = ', '.join(destinatarios)
    mensagem['Subject'] = 'Relatório - Piadas Chuck Norris (Projeto RPA)'

    corpo = "Segue abaixo as piadas coletadas da API Chuck Norris:\n\n"
    for piada in piadas_chuck:
        corpo += f"- {piada[1]}\n\n"

    if not piadas_chuck:
        corpo += "Nenhuma piada com 'Chuck' foi encontrada."

    mensagem.attach(MIMEText(corpo, 'plain'))
    servidor_email.sendmail(remetente, destinatarios, mensagem.as_string())

    print('Email enviado com sucesso!')
except Exception as e:
    print(f'Erro ao enviar e-mail: {e}')
