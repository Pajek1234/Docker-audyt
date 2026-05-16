CREATE DATABASE IF NOT EXISTS gastroshop;
USE gastroshop;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL DEFAULT '',
    email VARCHAR(255) NOT NULL UNIQUE,
    -- BŁĄD VULN-02: Hasło zapisane czystym tekstem (Plaintext) — brak bcrypt/argon2
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'klient'
);

-- Dane testowe — hasła plaintext (VULN-02)
INSERT IGNORE INTO users (name, email, password, role) VALUES
    ('Administrator',  'admin@gastroshop.pl', 'Admin123!',  'admin'),
    ('Jan Kowalski',   'jan@gastroshop.pl',   'haslo123',   'klient'),
    ('Anna Nowak',     'anna@gastroshop.pl',  'qwerty',     'klient');
