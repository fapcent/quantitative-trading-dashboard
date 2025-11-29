CREATE TABLE market_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME(6) NOT NULL,       -- DATETIME(6) pour stocker les microsecondes
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(20, 10) NOT NULL,
    volume DECIMAL(20, 10)
);