# main.py - Script principal de génération

import os
from datetime import datetime
from generate_mysql_data import GreenCityDataGenerator
from generate_json_files import JSONConsommationGenerator
from generate_csv_files import CSVEnvironnementalGenerator
from config import DATE_DEBUT, DATE_FIN

def main():
    print("\n" + "="*70)
    print("🌿 GREENCITY - SYSTÈME DE GÉNÉRATION DE DONNÉES")
    print("="*70)
    print(f"📅 Période: {DATE_DEBUT.strftime('%Y-%m-%d')} → {DATE_FIN.strftime('%Y-%m-%d')}")
    print("="*70 + "\n")
    
    # Créer les dossiers de sortie
    for folder in ['output/sql', 'output/json', 'output/csv']:
        os.makedirs(folder, exist_ok=True)
    
    # ============================================
    # ÉTAPE 1: Générer les données MySQL
    # ============================================
    print("\n📦 ÉTAPE 1: Génération des données MySQL...")
    mysql_generator = GreenCityDataGenerator()
    mysql_generator.generer_toutes_donnees()
    mysql_generator.generer_sql_inserts()
    
    # ============================================
    # ÉTAPE 2: Générer les fichiers JSON IoT
    # ============================================
    print("\n📦 ÉTAPE 2: Génération des fichiers JSON (consommation IoT)...")
    json_generator = JSONConsommationGenerator(
        mysql_generator.batiments,
        mysql_generator.compteurs,
        mysql_generator.regions
    )
    
    # Générer pour une période réduite (1 mois pour l'exemple)
    # Vous pouvez étendre à toute la période en production
    json_generator.generer_tous_fichiers_json(
        datetime(2025, 1, 1),
        datetime(2025, 1, 14),  # 2 semaines pour l'exemple
        'output/json'
    )
    
    # ============================================
    # ÉTAPE 3: Générer les fichiers CSV environnementaux
    # ============================================
    print("\n📦 ÉTAPE 3: Génération des fichiers CSV (rapports environnementaux)...")
    csv_generator = CSVEnvironnementalGenerator(
        mysql_generator.batiments,
        mysql_generator.regions
    )
    
    csv_generator.generer_tous_rapports(
        DATE_DEBUT,
        DATE_FIN,
        'output/csv'
    )
    
    # ============================================
    # RÉSUMÉ FINAL
    # ============================================
    print("\n" + "="*70)
    print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
    print("="*70)
    print("\n📁 Fichiers générés:")
    print("   • output/sql/insert_data.sql     - Script SQL INSERT")
    print("   • output/json/                    - Fichiers JSON consommation")
    print("   • output/csv/                     - Fichiers CSV environnementaux")
    print("\n🔧 Défauts de qualité introduits:")
    print("   • Valeurs manquantes: ~2%")
    print("   • Doublons: ~1%")
    print("   • Espaces inutiles: ~3%")
    print("   • Formats de date incorrects: ~2%")
    print("   • Valeurs incohérentes: ~2%")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
