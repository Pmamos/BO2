
FROM python:3.12-slim

# Instalujemy uv wewnątrz kontenera
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki z zależnościami
COPY pyproject.toml uv.lock ./

# Instalujemy zależności systemowe bez tworzenia wirtualnego środowiska w Dockerze
RUN uv pip install --system -r pyproject.toml

# Kopiujemy resztę kodu
COPY ./src/backend ./src/backend

# Odpalamy serwer FastAPI
CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]