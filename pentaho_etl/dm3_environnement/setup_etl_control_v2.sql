-- ============================================================
-- Script: setup_etl_control_v2.sql
-- Description: Configuration de la table etl_control pour DM3
--              Pattern adapté de DM1 avec suivi des lignes extraites
-- ============================================================

USE greencity_dw;

-- Supprimer l'ancienne table si elle existe
DROP TABLE IF EXISTS etl_control;

-- Créer la nouvelle table avec le pattern DM1
CREATE TABLE etl_control (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_source VARCHAR(100) NOT NULL UNIQUE COMMENT 'Identifiant de la source (ex: environnement, consommation)',
    derniere_extraction DATETIME DEFAULT '1900-01-01 00:00:00' COMMENT 'Date de la dernière extraction réussie',
    nb_lignes_extraites INT DEFAULT 0 COMMENT 'Nombre de lignes extraites lors de la dernière exécution',
    statut VARCHAR(50) DEFAULT 'PENDING' COMMENT 'Statut de la dernière exécution (SUCCESS, FAILED, PENDING, RUNNING)',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Date de dernière modification',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Date de création'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Table de contrôle ETL';

-- Insérer les entrées pour les différents data marts
INSERT INTO etl_control (nom_source, derniere_extraction, nb_lignes_extraites, statut) VALUES
('env_reports', '1900-01-01 00:00:00', 0, 'PENDING');
-- Vérification
SELECT * FROM etl_control;

