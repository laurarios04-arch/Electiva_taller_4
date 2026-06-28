FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888
EXPOSE 8501

CMD bash
