# 開発用ステージ
FROM python:3.11-bookworm AS developer

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    wget \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY . .

# ビルド用ステージ
FROM python:3.11-bookworm AS builder
WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --dev --system --deploy

RUN mkdir -p /app/assets/tmp/faiss && \
    chmod -R 755 /app/assets && \
    chown -R 1000:1000 /app/assets

COPY . .

# 最終用ステージ
FROM gcr.io/distroless/python3-debian12:nonroot AS production

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages
COPY --from=builder /app .
COPY --from=builder --chown=nonroot:nonroot /app .

EXPOSE 8000

USER nonroot

CMD ["/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]