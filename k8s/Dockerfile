# Usando uma imagem base leve do Python
FROM python:3.11-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o script para o container
COPY log_generator.py .

# Definindo o comando padrão ao iniciar o container
CMD ["python", "log_generator.py"]
