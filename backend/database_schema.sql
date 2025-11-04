-- ============================================
-- SCHÉMA DE BASE DE DONNÉES - OLYMPICS
-- ============================================

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS olympics_db;
USE olympics_db;

-- ============================================
-- TABLE: countries (Pays)
-- ============================================
CREATE TABLE countries (
    country_id INT PRIMARY KEY AUTO_INCREMENT,
    country_code CHAR(3) UNIQUE NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_flag VARCHAR(10),
    first_participation YEAR,
    total_participations INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE: olympics (Jeux Olympiques)
-- ============================================
CREATE TABLE olympics (
    olympic_id INT PRIMARY KEY AUTO_INCREMENT,
    year YEAR NOT NULL,
    season ENUM('Summer', 'Winter') NOT NULL,
    city VARCHAR(100) NOT NULL,
    host_country_id INT,
    start_date DATE,
    end_date DATE,
    total_athletes INT,
    total_events INT,
    total_countries INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_country_id) REFERENCES countries(country_id),
    UNIQUE KEY unique_olympics (year, season)
);

-- ============================================
-- TABLE: sports (Sports)
-- ============================================
CREATE TABLE sports (
    sport_id INT PRIMARY KEY AUTO_INCREMENT,
    sport_name VARCHAR(100) UNIQUE NOT NULL,
    sport_category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    first_year YEAR,
    last_year YEAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE: athletes (Athlètes)
-- ============================================
CREATE TABLE athletes (
    athlete_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    country_id INT,
    birth_date DATE,
    gender ENUM('M', 'F', 'X') NOT NULL,
    height_cm INT,
    weight_kg INT,
    total_medals INT DEFAULT 0,
    gold_medals INT DEFAULT 0,
    silver_medals INT DEFAULT 0,
    bronze_medals INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    INDEX idx_country (country_id),
    INDEX idx_name (last_name, first_name)
);

-- ============================================
-- TABLE: events (Épreuves)
-- ============================================
CREATE TABLE events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(200) NOT NULL,
    sport_id INT,
    olympic_id INT,
    gender ENUM('M', 'F', 'Mixed') NOT NULL,
    event_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sport_id) REFERENCES sports(sport_id),
    FOREIGN KEY (olympic_id) REFERENCES olympics(olympic_id),
    INDEX idx_sport (sport_id),
    INDEX idx_olympic (olympic_id)
);

-- ============================================
-- TABLE: medals (Médailles)
-- ============================================
CREATE TABLE medals (
    medal_id INT PRIMARY KEY AUTO_INCREMENT,
    athlete_id INT,
    event_id INT,
    country_id INT,
    medal_type ENUM('Gold', 'Silver', 'Bronze') NOT NULL,
    medal_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    INDEX idx_athlete (athlete_id),
    INDEX idx_country (country_id),
    INDEX idx_medal_type (medal_type),
    INDEX idx_event (event_id)
);

-- ============================================
-- TABLE: results (Résultats)
-- ============================================
CREATE TABLE results (
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    athlete_id INT,
    event_id INT,
    country_id INT,
    rank_position INT,
    performance_value VARCHAR(50),
    is_record BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    INDEX idx_athlete (athlete_id),
    INDEX idx_event (event_id),
    INDEX idx_rank (rank_position)
);

-- ============================================
-- TABLE: predictions_2024 (Prédictions Paris 2024)
-- ============================================
CREATE TABLE predictions_2024 (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    country_id INT,
    predicted_gold INT DEFAULT 0,
    predicted_silver INT DEFAULT 0,
    predicted_bronze INT DEFAULT 0,
    predicted_total INT DEFAULT 0,
    predicted_rank INT,
    model_name VARCHAR(100),
    confidence_score DECIMAL(4,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    INDEX idx_country (country_id)
);

-- ============================================
-- VUES (Views)
-- ============================================

-- Vue: Médailles par pays
CREATE VIEW medals_by_country AS
SELECT 
    c.country_code,
    c.country_name,
    COUNT(*) as total_medals,
    SUM(CASE WHEN m.medal_type = 'Gold' THEN 1 ELSE 0 END) as gold,
    SUM(CASE WHEN m.medal_type = 'Silver' THEN 1 ELSE 0 END) as silver,
    SUM(CASE WHEN m.medal_type = 'Bronze' THEN 1 ELSE 0 END) as bronze
FROM countries c
LEFT JOIN medals m ON c.country_id = m.country_id
GROUP BY c.country_id, c.country_code, c.country_name
ORDER BY total_medals DESC;

-- Vue: Médailles par sport
CREATE VIEW medals_by_sport AS
SELECT 
    s.sport_name,
    COUNT(*) as total_medals,
    SUM(CASE WHEN m.medal_type = 'Gold' THEN 1 ELSE 0 END) as gold,
    SUM(CASE WHEN m.medal_type = 'Silver' THEN 1 ELSE 0 END) as silver,
    SUM(CASE WHEN m.medal_type = 'Bronze' THEN 1 ELSE 0 END) as bronze
FROM sports s
LEFT JOIN events e ON s.sport_id = e.sport_id
LEFT JOIN medals m ON e.event_id = m.event_id
GROUP BY s.sport_id, s.sport_name
ORDER BY total_medals DESC;

-- Vue: Top athlètes
CREATE VIEW top_athletes AS
SELECT 
    a.full_name,
    c.country_name,
    a.total_medals,
    a.gold_medals,
    a.silver_medals,
    a.bronze_medals
FROM athletes a
JOIN countries c ON a.country_id = c.country_id
WHERE a.total_medals > 0
ORDER BY a.total_medals DESC, a.gold_medals DESC
LIMIT 100;

-- ============================================
-- DONNÉES D'EXEMPLE
-- ============================================

-- Pays
INSERT INTO countries (country_code, country_name, country_flag, first_participation) VALUES
('FRA', 'France', '🇫🇷', 1896),
('USA', 'United States', '🇺🇸', 1896),
('GBR', 'Great Britain', '🇬🇧', 1896),
('CHN', 'China', '🇨🇳', 1952),
('JPN', 'Japan', '🇯🇵', 1912),
('GER', 'Germany', '🇩🇪', 1896),
('AUS', 'Australia', '🇦🇺', 1896),
('RUS', 'Russia', '🇷🇺', 1896);

-- Jeux Olympiques
INSERT INTO olympics (year, season, city, host_country_id, total_athletes, total_events, total_countries) VALUES
(1896, 'Summer', 'Athens', 1, 241, 43, 14),
(1900, 'Summer', 'Paris', 1, 997, 95, 24),
(1924, 'Summer', 'Paris', 1, 3089, 126, 44),
(1924, 'Winter', 'Chamonix', 1, 258, 16, 16),
(2020, 'Summer', 'Tokyo', 5, 11656, 339, 206),
(2024, 'Summer', 'Paris', 1, 10500, 329, 206);

-- Sports
INSERT INTO sports (sport_name, sport_category, first_year) VALUES
('Athletics', 'Individual', 1896),
('Swimming', 'Individual', 1896),
('Gymnastics', 'Individual', 1896),
('Fencing', 'Individual', 1896),
('Cycling', 'Individual', 1896),
('Football', 'Team', 1900),
('Basketball', 'Team', 1936),
('Judo', 'Individual', 1964);

-- ============================================
-- REQUÊTES UTILES
-- ============================================

-- Médailles de la France
SELECT 
    o.year,
    o.season,
    COUNT(*) as total,
    SUM(CASE WHEN m.medal_type = 'Gold' THEN 1 ELSE 0 END) as gold,
    SUM(CASE WHEN m.medal_type = 'Silver' THEN 1 ELSE 0 END) as silver,
    SUM(CASE WHEN m.medal_type = 'Bronze' THEN 1 ELSE 0 END) as bronze
FROM medals m
JOIN events e ON m.event_id = e.event_id
JOIN olympics o ON e.olympic_id = o.olympic_id
JOIN countries c ON m.country_id = c.country_id
WHERE c.country_code = 'FRA'
GROUP BY o.olympic_id, o.year, o.season
ORDER BY o.year DESC;

-- Top 10 pays par nombre de médailles
SELECT * FROM medals_by_country LIMIT 10;

-- Sports français dominants
SELECT 
    s.sport_name,
    COUNT(*) as medals_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM medals WHERE country_id = 
        (SELECT country_id FROM countries WHERE country_code = 'FRA')), 2) as percentage
FROM medals m
JOIN events e ON m.event_id = e.event_id
JOIN sports s ON e.sport_id = s.sport_id
WHERE m.country_id = (SELECT country_id FROM countries WHERE country_code = 'FRA')
GROUP BY s.sport_id, s.sport_name
ORDER BY medals_count DESC
LIMIT 10;

-- ============================================
-- INDEX POUR PERFORMANCE
-- ============================================

CREATE INDEX idx_medals_country_date ON medals(country_id, medal_date);
CREATE INDEX idx_athletes_country_medals ON athletes(country_id, total_medals);
CREATE INDEX idx_events_olympic_sport ON events(olympic_id, sport_id);

-- ============================================
-- TRIGGERS (optionnel)
-- ============================================

-- Mettre à jour le total de médailles d'un athlète
DELIMITER //
CREATE TRIGGER update_athlete_medals_after_insert
AFTER INSERT ON medals
FOR EACH ROW
BEGIN
    UPDATE athletes 
    SET 
        total_medals = total_medals + 1,
        gold_medals = gold_medals + (CASE WHEN NEW.medal_type = 'Gold' THEN 1 ELSE 0 END),
        silver_medals = silver_medals + (CASE WHEN NEW.medal_type = 'Silver' THEN 1 ELSE 0 END),
        bronze_medals = bronze_medals + (CASE WHEN NEW.medal_type = 'Bronze' THEN 1 ELSE 0 END)
    WHERE athlete_id = NEW.athlete_id;
END//
DELIMITER ;
