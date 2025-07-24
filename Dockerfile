FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 🧱 Copiar requirements primero (mejor uso de caché)
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y dos2unix && \
    pip install --no-cache-dir -r requirements.txt

# 📜 Copiar entrypoint antes de manipularlo
COPY entrypoint.sh /app/

# 🧼 Asegurar formato y permisos del script
RUN dos2unix /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# 📦 Copiar el resto del código
COPY . /app/

# 🚀 Punto de entrada y comando por defecto
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000