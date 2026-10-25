CREATE SCHEMA IF NOT EXISTS `fundamental_analyzer` DEFAULT CHARACTER SET utf8 ;
USE `fundamental_analyzer` ;

CREATE TABLE company (
    ticker VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    exchange VARCHAR(50)
);

CREATE TABLE score_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    calculated_date DATE NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    label VARCHAR(20) NOT NULL,
    company_ticker VARCHAR(10) NOT NULL,
    FOREIGN KEY (company_ticker) REFERENCES company(ticker)
);