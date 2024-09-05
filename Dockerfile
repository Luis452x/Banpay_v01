FROM python:latest

WORKDIR /app

COPY ./requeriments.txt /app/requeriments.txt

RUN pip install --no-cache-dir --upgrade -r /app/requeriments.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","8000"]