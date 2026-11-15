# Application container only. The Executor sandbox must be separately isolated and more restricted.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt pyproject.toml ./
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
RUN pip install -e . \
    && useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p artifacts results/traces \
    && chown -R appuser:appuser /app

USER appuser
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
