FROM python:3.11-slim

WORKDIR /app

# install system deps for psql and building wheels
RUN apt-get update && apt-get install -y gcc libqp-dev \ 
&& pip install --no-cache-dir -r requirements.txt \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
