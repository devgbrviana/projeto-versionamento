🤖 Projeto RPA - Automação com Python e API Chuck Norris

Este repositório contém o projeto de automação desenvolvido para a disciplina de RPA, integrando coleta, armazenamento, processamento e envio de informações utilizando a API pública gratuita Chuck Norris API.

🚀 Tecnologias Utilizadas

- Python 3.x  
- Requests (para consumir a API Chuck Norris)  
- SQLite (banco de dados local)  
- Biblioteca re (para processamento de texto com expressões regulares)  
- smtplib (para envio automatizado de e-mails)  

▶️ Como Executar o Projeto

1. **Clone o repositório**  
git clone <url-do-repositorio>
cd <nome-da-pasta>
(Opcional) Crie um ambiente virtual

python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Instale as dependências

pip install -r requirements.txt
Execute os scripts na ordem:


python requisicao_api.py
python processamento.py
python envio_email.py
📝 O banco de dados SQLite projeto_rpa.db será criado automaticamente na primeira execução.

📡 Funcionalidades
Coleta: Faz requisições à API Chuck Norris para coletar piadas aleatórias.

Armazenamento: Salva as piadas em um banco de dados SQLite.

Processamento: Utiliza expressões regulares para extrair e validar informações nas piadas, armazenando os resultados em uma tabela separada.

Envio de Relatório: Envia automaticamente um e-mail com resumo dos dados coletados e processados.


🛠️ Futuras Melhorias
Interface gráfica para visualização dos dados


🧑‍💻 Autor
Gabriel de Souza Viana

