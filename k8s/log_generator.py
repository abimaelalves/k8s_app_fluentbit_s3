import time
import logging
import random

# Configurando o logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

messages = ["User logged in", "Data processed", "Error occurred", "Transaction completed", "Service started"]

while True:
    log_level = random.choice([logging.INFO, logging.WARNING, logging.ERROR])
    message = random.choice(messages)
    logging.log(log_level, message)
    time.sleep(random.randint(1, 5))  # Gera logs a cada 1 a 5 segundos
