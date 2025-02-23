FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8085

CMD ["fastapi", "dev", "src/app.py", "--port", "8085"]