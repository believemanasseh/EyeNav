FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry install

EXPOSE 8080

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8080"]