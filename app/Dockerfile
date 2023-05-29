# Use uma imagem base adequada ao seu projeto, como Python 3.8
FROM python:3.8

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o código do seu projeto para o diretório de trabalho
COPY . /app

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a API está rodando (defina a porta corretamente)
EXPOSE 8000

# Comando para iniciar o servidor da API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
