-- ============================================
-- GREENCITY DATA WAREHOUSE - CRÉATION DES DATA MARTS
-- Date: 2026-01-01
-- Description: Script de création des trois Data Marts
--   1. Consommation énergétique (dm_consommation)
--   2. Rentabilité économique (dm_rentabilite)
--   3. Impact environnemental (dm_environnement)
-- Architecture: Schéma en étoile (Star Schema)
-- ============================================

-- Création de la base de données du Data Warehouse
DROP DATABASE IF EXISTS greencity_dw;
CREATE DATABASE greencity_dw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE greencity_dw;

-- ============================================
-- DIMENSIONS COMMUNES (partagées entre Data Marts)
-- ============================================

-- Dimension Temps (commune à tous les Data Marts)
CREATE TABLE dim_temps (
    id_temps INT AUTO_INCREMENT PRIMARY KEY,
    date_complete DATE NOT NULL UNIQUE,
    annee INT NOT NULL,
    trimestre INT NOT NULL,
    mois INT NOT NULL,
    nom_mois VARCHAR(20) NOT NULL,
    semaine INT NOT NULL,
    jour INT NOT NULL,
    jour_semaine INT NOT NULL,
    nom_jour VARCHAR(20) NOT NULL,
    est_weekend BOOLEAN NOT NULL,
    est_ferie BOOLEAN DEFAULT FALSE,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Dimension Région (commune à tous les Data Marts)
CREATE TABLE dim_region (
    id_region_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_region VARCHAR(10) NOT NULL,
    nom_region VARCHAR(100) NOT NULL,
    ville VARCHAR(50) NOT NULL,
    pays VARCHAR(50) NOT NULL,
    code_postal VARCHAR(10),
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

-- Dimension Bâtiment (commune à tous les Data Marts)
CREATE TABLE dim_batiment (
    id_batiment_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment VARCHAR(10) NOT NULL,
    nom_batiment VARCHAR(100) NOT NULL,
    adresse VARCHAR(200),
    surface_m2 DECIMAL(12,2),
    type_batiment VARCHAR(50) NOT NULL,
    nb_etages INT,
    annee_construction INT,
    id_region VARCHAR(10) NOT NULL,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- DATA MART 1: CONSOMMATION ÉNERGÉTIQUE
-- ============================================

-- Dimension Type d'énergie
CREATE TABLE dim_type_energie (
    id_type_energie_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_type_energie INT NOT NULL,
    libelle VARCHAR(50) NOT NULL,
    unite VARCHAR(10) NOT NULL,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Dimension Compteur
CREATE TABLE dim_compteur (
    id_compteur_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_compteur VARCHAR(20) NOT NULL,
    id_batiment VARCHAR(10) NOT NULL,
    id_type_energie INT NOT NULL,
    date_installation DATE,
    statut VARCHAR(20),
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table de faits: Consommation Énergétique
CREATE TABLE fait_consommation (
    id_consommation INT AUTO_INCREMENT PRIMARY KEY,
    -- Clés étrangères vers les dimensions
    id_temps_fk INT NOT NULL,
    id_batiment_fk INT NOT NULL,
    id_region_fk INT NOT NULL,
    id_type_energie_fk INT NOT NULL,
    id_compteur_fk INT NOT NULL,
    -- Mesures
    consommation DECIMAL(15,4) NOT NULL,
    heure_mesure INT,
    temperature_moyenne DECIMAL(5,2),
    -- Timestamps
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Clés étrangères
    FOREIGN KEY (id_temps_fk) REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_batiment_fk) REFERENCES dim_batiment(id_batiment_sk),
    FOREIGN KEY (id_region_fk) REFERENCES dim_region(id_region_sk),
    FOREIGN KEY (id_type_energie_fk) REFERENCES dim_type_energie(id_type_energie_sk),
    FOREIGN KEY (id_compteur_fk) REFERENCES dim_compteur(id_compteur_sk),
    -- Index pour performances
    INDEX idx_fait_conso_temps (id_temps_fk),
    INDEX idx_fait_conso_batiment (id_batiment_fk),
    INDEX idx_fait_conso_region (id_region_fk),
    INDEX idx_fait_conso_energie (id_type_energie_fk)
);

-- ============================================
-- DATA MART 2: RENTABILITÉ ÉCONOMIQUE
-- ============================================

-- Dimension Client
CREATE TABLE dim_client (
    id_client_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_client VARCHAR(20) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100),
    type_client VARCHAR(50) NOT NULL,
    email VARCHAR(150),
    telephone VARCHAR(30),
    adresse VARCHAR(200),
    id_region VARCHAR(10),
    date_inscription DATE,
    statut VARCHAR(20),
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Dimension Contrat
CREATE TABLE dim_contrat (
    id_contrat_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_contrat VARCHAR(20) NOT NULL,
    id_client VARCHAR(20) NOT NULL,
    id_compteur VARCHAR(20) NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    statut VARCHAR(20) NOT NULL,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Dimension Statut Paiement
CREATE TABLE dim_statut_paiement (
    id_statut_sk INT AUTO_INCREMENT PRIMARY KEY,
    code_statut VARCHAR(20) NOT NULL,
    libelle_statut VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table de faits: Rentabilité Économique (basée sur les factures)
CREATE TABLE fait_rentabilite (
    id_rentabilite INT AUTO_INCREMENT PRIMARY KEY,
    -- Clés étrangères vers les dimensions
    id_temps_fk INT NOT NULL,
    id_client_fk INT NOT NULL,
    id_batiment_fk INT NOT NULL,
    id_region_fk INT NOT NULL,
    id_type_energie_fk INT NOT NULL,
    id_contrat_fk INT NOT NULL,
    id_statut_paiement_fk INT NOT NULL,
    -- Identifiant facture source
    id_facture VARCHAR(20) NOT NULL,
    -- Mesures financières
    montant_ht DECIMAL(12,2) NOT NULL,
    tva DECIMAL(5,2) NOT NULL,
    montant_ttc DECIMAL(12,2) NOT NULL,
    cout_energie DECIMAL(12,2) NOT NULL,
    consommation DECIMAL(15,4) NOT NULL,
    marge DECIMAL(12,2) NOT NULL,  -- marge = montant_ttc - cout_energie
    -- Dates de la période
    periode_debut DATE,
    periode_fin DATE,
    date_echeance DATE,
    -- Timestamps
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Clés étrangères
    FOREIGN KEY (id_temps_fk) REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_client_fk) REFERENCES dim_client(id_client_sk),
    FOREIGN KEY (id_batiment_fk) REFERENCES dim_batiment(id_batiment_sk),
    FOREIGN KEY (id_region_fk) REFERENCES dim_region(id_region_sk),
    FOREIGN KEY (id_type_energie_fk) REFERENCES dim_type_energie(id_type_energie_sk),
    FOREIGN KEY (id_contrat_fk) REFERENCES dim_contrat(id_contrat_sk),
    FOREIGN KEY (id_statut_paiement_fk) REFERENCES dim_statut_paiement(id_statut_sk),
    -- Index pour performances
    INDEX idx_fait_rent_temps (id_temps_fk),
    INDEX idx_fait_rent_client (id_client_fk),
    INDEX idx_fait_rent_batiment (id_batiment_fk),
    INDEX idx_fait_rent_region (id_region_fk),
    INDEX idx_fait_rent_contrat (id_contrat_fk)
);

-- Table de faits: Paiements (pour le suivi du recouvrement)
CREATE TABLE fait_paiement (
    id_paiement_fait INT AUTO_INCREMENT PRIMARY KEY,
    -- Clés étrangères vers les dimensions
    id_temps_fk INT NOT NULL,
    id_client_fk INT NOT NULL,
    id_region_fk INT NOT NULL,
    -- Identifiants sources
    id_paiement VARCHAR(20) NOT NULL,
    id_facture VARCHAR(20) NOT NULL,
    -- Mesures
    montant_paye DECIMAL(12,2) NOT NULL,
    mode_paiement VARCHAR(50),
    -- Timestamps
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Clés étrangères
    FOREIGN KEY (id_temps_fk) REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_client_fk) REFERENCES dim_client(id_client_sk),
    FOREIGN KEY (id_region_fk) REFERENCES dim_region(id_region_sk),
    -- Index
    INDEX idx_fait_paie_temps (id_temps_fk),
    INDEX idx_fait_paie_client (id_client_fk)
);

-- ============================================
-- DATA MART 3: IMPACT ENVIRONNEMENTAL
-- ============================================

-- Table de faits: Impact Environnemental
CREATE TABLE fait_environnement (
    id_environnement INT AUTO_INCREMENT PRIMARY KEY,
    -- Clés étrangères vers les dimensions
    id_temps_fk INT NOT NULL,
    id_batiment_fk INT NOT NULL,
    id_region_fk INT NOT NULL,
    -- Mesures environnementales
    emission_co2_kg DECIMAL(12,2),
    taux_recyclage DECIMAL(5,4),
    -- Mesures calculées (ratio CO2/consommation)
    consommation_totale_kwh DECIMAL(15,4),
    ratio_co2_consommation DECIMAL(10,6),
    -- Timestamps
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Clés étrangères
    FOREIGN KEY (id_temps_fk) REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_batiment_fk) REFERENCES dim_batiment(id_batiment_sk),
    FOREIGN KEY (id_region_fk) REFERENCES dim_region(id_region_sk),
    -- Index pour performances
    INDEX idx_fait_env_temps (id_temps_fk),
    INDEX idx_fait_env_batiment (id_batiment_fk),
    INDEX idx_fait_env_region (id_region_fk)
);

-- ============================================
-- PROCÉDURE: Génération de la dimension temps
-- ============================================

DELIMITER //

CREATE PROCEDURE sp_generer_dim_temps(IN date_debut DATE, IN date_fin DATE)
BEGIN
    DECLARE v_date DATE;
    DECLARE v_nom_jour VARCHAR(20);
    DECLARE v_nom_mois VARCHAR(20);
    
    SET v_date = date_debut;
    
    WHILE v_date <= date_fin DO
        -- Déterminer le nom du jour
        SET v_nom_jour = CASE DAYOFWEEK(v_date)
            WHEN 1 THEN 'Dimanche'
            WHEN 2 THEN 'Lundi'
            WHEN 3 THEN 'Mardi'
            WHEN 4 THEN 'Mercredi'
            WHEN 5 THEN 'Jeudi'
            WHEN 6 THEN 'Vendredi'
            WHEN 7 THEN 'Samedi'
        END;
        
        -- Déterminer le nom du mois
        SET v_nom_mois = CASE MONTH(v_date)
            WHEN 1 THEN 'Janvier'
            WHEN 2 THEN 'Février'
            WHEN 3 THEN 'Mars'
            WHEN 4 THEN 'Avril'
            WHEN 5 THEN 'Mai'
            WHEN 6 THEN 'Juin'
            WHEN 7 THEN 'Juillet'
            WHEN 8 THEN 'Août'
            WHEN 9 THEN 'Septembre'
            WHEN 10 THEN 'Octobre'
            WHEN 11 THEN 'Novembre'
            WHEN 12 THEN 'Décembre'
        END;
        
        INSERT IGNORE INTO dim_temps (
            date_complete, annee, trimestre, mois, nom_mois,
            semaine, jour, jour_semaine, nom_jour, est_weekend
        ) VALUES (
            v_date,
            YEAR(v_date),
            QUARTER(v_date),
            MONTH(v_date),
            v_nom_mois,
            WEEKOFYEAR(v_date),
            DAY(v_date),
            DAYOFWEEK(v_date),
            v_nom_jour,
            DAYOFWEEK(v_date) IN (1, 7)
        );
        
        SET v_date = DATE_ADD(v_date, INTERVAL 1 DAY);
    END WHILE;
END //

DELIMITER ;

-- ============================================
-- INITIALISATION: Données de référence
-- ============================================

-- Générer la dimension temps pour la période 2022-2026
CALL sp_generer_dim_temps('2022-01-01', '2026-12-31');

-- Insérer les statuts de paiement
INSERT INTO dim_statut_paiement (code_statut, libelle_statut, description) VALUES
('Payée', 'Payée', 'Facture entièrement réglée'),
('En attente', 'En attente', 'Facture en attente de paiement'),
('En retard', 'En retard', 'Facture non payée après la date d''échéance'),
('Partiel', 'Paiement partiel', 'Facture partiellement réglée');

-- ============================================
-- VUES POUR L'ANALYSE (optionnel mais utile)
-- ============================================

-- Vue: Consommation par région et mois
CREATE VIEW v_consommation_region_mois AS
SELECT 
    r.nom_region,
    t.annee,
    t.nom_mois,
    te.libelle AS type_energie,
    SUM(fc.consommation) AS consommation_totale,
    AVG(fc.temperature_moyenne) AS temperature_moyenne
FROM fait_consommation fc
JOIN dim_region r ON fc.id_region_fk = r.id_region_sk
JOIN dim_temps t ON fc.id_temps_fk = t.id_temps
JOIN dim_type_energie te ON fc.id_type_energie_fk = te.id_type_energie_sk
GROUP BY r.nom_region, t.annee, t.mois, t.nom_mois, te.libelle;

-- Vue: Rentabilité par client
CREATE VIEW v_rentabilite_client AS
SELECT 
    c.id_client,
    c.nom,
    c.type_client,
    t.annee,
    SUM(fr.montant_ttc) AS chiffre_affaires,
    SUM(fr.marge) AS marge_totale,
    SUM(fr.consommation) AS consommation_totale,
    COUNT(DISTINCT fr.id_facture) AS nb_factures
FROM fait_rentabilite fr
JOIN dim_client c ON fr.id_client_fk = c.id_client_sk
JOIN dim_temps t ON fr.id_temps_fk = t.id_temps
GROUP BY c.id_client, c.nom, c.type_client, t.annee;

-- Vue: Taux de paiement
CREATE VIEW v_taux_paiement AS
SELECT 
    t.annee,
    t.nom_mois,
    sp.libelle_statut,
    COUNT(*) AS nb_factures,
    SUM(fr.montant_ttc) AS montant_total
FROM fait_rentabilite fr
JOIN dim_temps t ON fr.id_temps_fk = t.id_temps
JOIN dim_statut_paiement sp ON fr.id_statut_paiement_fk = sp.id_statut_sk
GROUP BY t.annee, t.mois, t.nom_mois, sp.libelle_statut;

-- Vue: Impact environnemental par bâtiment
CREATE VIEW v_environnement_batiment AS
SELECT 
    b.id_batiment,
    b.nom_batiment,
    b.type_batiment,
    r.nom_region,
    t.annee,
    t.nom_mois,
    SUM(fe.emission_co2_kg) AS emissions_co2_totales,
    AVG(fe.taux_recyclage) AS taux_recyclage_moyen,
    AVG(fe.ratio_co2_consommation) AS ratio_co2_conso_moyen
FROM fait_environnement fe
JOIN dim_batiment b ON fe.id_batiment_fk = b.id_batiment_sk
JOIN dim_region r ON fe.id_region_fk = r.id_region_sk
JOIN dim_temps t ON fe.id_temps_fk = t.id_temps
GROUP BY b.id_batiment, b.nom_batiment, b.type_batiment, r.nom_region, t.annee, t.mois, t.nom_mois;

-- ============================================
-- FIN DU SCRIPT
-- ============================================

SELECT 'Data Warehouse GreenCity créé avec succès!' AS message;
SELECT 'Tables créées:' AS info;
SELECT '  - Dimensions communes: dim_temps, dim_region, dim_batiment' AS tables;
SELECT '  - DM Consommation: dim_type_energie, dim_compteur, fait_consommation' AS tables;
SELECT '  - DM Rentabilité: dim_client, dim_contrat, dim_statut_paiement, fait_rentabilite, fait_paiement' AS tables;
SELECT '  - DM Environnement: fait_environnement' AS tables;
