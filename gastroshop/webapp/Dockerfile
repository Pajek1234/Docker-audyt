# 1. BŁĄD: Stary, niewspierany obraz bazowy (EOL - End of Life)
FROM debian:stretch

# NAPRAWA REPOZYTORIÓW
RUN sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list && \
    sed -i s/security.debian.org/archive.debian.org/g /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list

# 2. BŁĄD: Ujawnienie danych autora
MAINTAINER jan.kowalski@gastroshop.pl

# 3. BŁĄD: Wrażliwe dane w ENV (VULN-03)
ENV DB_PASSWORD=SuperTajneHasloBazy123!
ENV SECRET_KEY=supersecret123
ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE

# 4 i 5. BŁĄD: Instalacja zbędnych narzędzi i brak czyszczenia cache
RUN apt-get update && apt-get install -y --allow-unauthenticated \
    openssh-server netcat nmap sudo curl wget telnet ftp python3 python3-pip apache2

WORKDIR /app
COPY . /app

# 6. BŁĄD: Instalacja bibliotek jako ROOT
RUN pip3 install -r requirements.txt

# 7. BŁĄD: Nadmierne uprawnienia (777) — VULN-05
RUN chmod -R 777 /app

# 8. BŁĄD: Konfiguracja SSH (Root login) — VULN-04
RUN echo 'root:password123' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN mkdir -p /run/sshd

# 9. BŁĄD: Ekspozycja zbędnych portów — VULN-08
EXPOSE 22 8080 23 21 3306

# Start
CMD service ssh start && python3 /app/app.py
