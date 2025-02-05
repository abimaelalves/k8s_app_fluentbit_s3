import time  # Biblioteca para manipulação de tempo
import logging  # Biblioteca para geração de logs
import random  # Biblioteca para gerar valores aleatórios

# 📌 Configuração do logger
logging.basicConfig(
    level=logging.INFO,  # Define o nível mínimo de log como INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # Formato do log: timestamp, nível e mensagem
)

# 📌 Lista de mensagens aleatórias para simular eventos de logs
messages = [
    "User logged in",
    "Data processed",
    "Error occurred",
    "Transaction completed",
    "Service started"
]

# 📌 Loop infinito que gera logs aleatórios continuamente
while True:
    log_level = random.choice([logging.INFO, logging.WARNING, logging.ERROR])  # Escolhe um nível de log aleatório
    message = random.choice(messages)  # Escolhe uma mensagem aleatória
    logging.log(log_level, message)  # Registra o log com o nível e mensagem escolhidos
    time.sleep(random.randint(1, 5))  # Aguarda um tempo aleatório entre 1 a 5 segundos antes de gerar o próximo log
