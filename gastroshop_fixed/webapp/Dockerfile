# 1. BŁĄD: Stary, niewspierany obraz bazowy (EOL - End of Life)
FROM python:3.12-slim
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -u 1001 -m appuser

# NAPRAWA REPOZYTORIÓW

# 2. BŁĄD: Ujawnienie danych autora

# 3. BŁĄD: Wrażliwe dane w ENV (VULN-03)

# 4 i 5. BŁĄD: Instalacja zbędnych narzędzi i brak czyszczenia cache

WORKDIR /app
COPY --chown=appuser:appuser . .

# 6. BŁĄD: Instalacja bibliotek jako ROOT
RUN pip3 install -r requirements.txt

# 7. BŁĄD: Nadmierne uprawnienia (777) — VULN-05

# 8. BŁĄD: Konfiguracja SSH (Root login) — VULN-04

# 9. BŁĄD: Ekspozycja zbędnych portów — VULN-08
EXPOSE 22 8080 23 21 3306

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

USER appuser
# Start
CMD ["python3", "/app/app.py"]
