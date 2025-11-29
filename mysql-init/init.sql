CREATE DATABASE IF NOT EXISTS trading_dashboard;
USE trading_dashboard;

CREATE TABLE IF NOT EXISTS market_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME(6) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(20, 10) NOT NULL,
    volume DECIMAL(20, 10),
    source VARCHAR(50) NOT NULL  -- <--- NOUVELLE COLONNE
);