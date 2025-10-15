FROM python:3.11-slim

ARG USER=appuser
RUN groupadd -r $USER && useradd -r -g $USER $USER

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
&& apt-get install -y --no-install-recommends \
   gcc \
   libpq-dev \
   build-essential \
   libjpeg-dev \
   zlib1g-dev \
&& pip install --no-cache-dir -r requirements.txt \
&& apt-get remove -y --purge build-essential \
&& apt-get autoremove -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

COPY . .

USER $USER

EXPOSE 8000

# Use Render's dynamic port if provided
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
