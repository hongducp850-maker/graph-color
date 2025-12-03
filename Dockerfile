FROM python:3.10-slim
RUN apt-get update && apt-get install -y build-essential libfreetype6-dev libpng-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
ENV PORT=8080
EXPOSE 8080
CMD ["gunicorn","--bind","0.0.0.0:8080","app:app","--workers","1"]
