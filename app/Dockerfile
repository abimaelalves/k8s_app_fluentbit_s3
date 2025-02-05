# 📌 Usa a imagem base Python 3.11 minimalista para reduzir o tamanho do container
FROM python:3.11-slim  

# 📌 Define o diretório de trabalho dentro do container
WORKDIR /app  

# 📌 Copia o arquivo da aplicação para dentro do container
COPY app.py .  

# 📌 Comando que será executado ao iniciar o container (roda a aplicação)
CMD ["python", "app.py"]  
