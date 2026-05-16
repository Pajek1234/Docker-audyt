# GastroShop — Projekt edukacyjny (Audyt Bezpieczeństwa)

Aplikacja webowa celowo zawierająca podatności bezpieczeństwa do celów dydaktycznych.

## Uruchomienie

**Wymagania:** Docker + Docker Compose

```bash
# 1. Uruchom wszystkie kontenery
docker compose up --build

# 2. Otwórz przeglądarkę
http://localhost:8080
```

## Konta testowe

| E-mail                   | Hasło      | Rola   |
|--------------------------|------------|--------|
| admin@gastroshop.pl      | Admin123!  | admin  |
| jan@gastroshop.pl        | haslo123   | klient |
| anna@gastroshop.pl       | qwerty     | klient |

## Funkcje

- Logowanie / wylogowanie (połączone z MySQL)
- Rejestracja nowych użytkowników (zapisywani do MySQL)
- Koszyk zakupowy (sesja Flask)
- Panel audytu z listą 9 podatności
- Zakładka "Użytkownicy w DB" — tylko dla admina, pobiera dane z MySQL przez /users

## Podatności (celowe)

| ID      | Poziom   | Opis |
|---------|----------|------|
| VULN-01 | CRITICAL | SQL Injection w logowaniu i rejestracji |
| VULN-02 | CRITICAL | Hasła plaintext w MySQL (brak bcrypt) |
| VULN-03 | CRITICAL | Wrażliwe dane w ENV Dockerfile |
| VULN-04 | CRITICAL | SSH Root Login z hasłem password123 |
| VULN-05 | HIGH     | chmod -R 777 na plikach aplikacji |
| VULN-06 | HIGH     | Obraz bazowy EOL (Debian 9 Stretch) |
| VULN-07 | HIGH     | XSS — email bez escapowania w HTML |
| VULN-08 | MEDIUM   | Zbędne porty (22, 23, 21, 3306) |
| VULN-09 | MEDIUM   | Stare zależności z known CVE |

## Demo SQL Injection (VULN-01)

W polu e-mail wpisz: `' OR '1'='1`
W polu hasło wpisz: cokolwiek

Zapytanie staje się: `WHERE email='' OR '1'='1' AND password='x'`
Warunek zawsze prawdziwy → zalogowanie bez znajomości hasła.

## Architektura

```
Przeglądarka
     ↕ HTTP :8080
Flask (app.py)
     ↕ PyMySQL :3306
MySQL 5.7 (gastroshop.users)
     ↕
Redis 6.0 (opcjonalnie)
```
