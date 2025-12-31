# -*- coding: utf-8 -*-
# generate_csv_files.py - Génération des fichiers CSV environnementaux

import csv
import random
import os
from datetime import datetime, timedelta
from config import *

random.seed(42)

class CSVEnvironnementalGenerator:
    def __init__(self, batiments, regions):
        self.batiments = batiments
        self.regions = regions
    
    def generer_rapport_mensuel(self, mois, annee, output_dir='output/csv'):
        """Génère un rapport environnemental mensuel"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Dernier jour du mois
        if mois == 12:
            date_rapport = datetime(annee + 1, 1, 1) - timedelta(days=1)
        else:
            date_rapport = datetime(annee, mois + 1, 1) - timedelta(days=1)
        
        filename = f"env_reports_{str(mois).zfill(2)}_{annee}.csv"
        filepath = os.path.join(output_dir, filename)
        
        rows = []
        
        for batiment in self.batiments:
            # Émissions CO2 basées sur le type de bâtiment
            type_bat = batiment.get('type_batiment', 'Commercial')
            surface = abs(batiment.get('surface_m2', 1000))  # abs pour gérer les erreurs
            
            # Base d'émission par m² selon le type
            emission_base = {
                'Résidentiel': 0.15,
                'Commercial': 0.25,
                'Industriel': 0.45,
                'Mixte': 0.20
            }
            
            base = emission_base.get(type_bat, 0.20)
            
            # Variation saisonnière (plus d'émissions en hiver)
            if mois in [11, 12, 1, 2, 3]:
                facteur_saison = random.uniform(1.3, 1.8)
            else:
                facteur_saison = random.uniform(0.8, 1.2)
            
            emission_co2 = round(surface * base * facteur_saison * random.uniform(0.8, 1.2), 2)
            taux_recyclage = round(random.uniform(0.45, 0.85), 2)
            
            row = {
                'id_region': batiment['id_region'],
                'id_batiment': batiment['id_batiment'],
                'date_rapport': date_rapport.strftime('%Y-%m-%d'),
                'emission_CO2_kg': emission_co2,
                'taux_recyclage': taux_recyclage
            }
            
            # Introduire des défauts de qualité
            
            # Valeur manquante
            if random.random() < DEFAUTS_QUALITE['taux_valeurs_manquantes']:
                row['emission_CO2_kg'] = ''
            
            # Valeur incohérente (négative ou très élevée)
            if random.random() < DEFAUTS_QUALITE['taux_valeurs_incoherentes']:
                if random.random() < 0.5:
                    row['emission_CO2_kg'] = -abs(emission_co2)
                else:
                    row['taux_recyclage'] = round(random.uniform(1.5, 2.0), 2)  # >100%
            
            # Format de date incorrect
            if random.random() < DEFAUTS_QUALITE['taux_format_date_incorrect']:
                row['date_rapport'] = date_rapport.strftime('%d/%m/%Y')
            
            # Espaces inutiles
            if random.random() < DEFAUTS_QUALITE['taux_espaces_inutiles']:
                row['id_batiment'] = f"  {row['id_batiment']}  "
            
            rows.append(row)
        
        # Ajouter quelques doublons
        nb_doublons = int(len(rows) * DEFAUTS_QUALITE['taux_doublons'])
        for _ in range(nb_doublons):
            rows.append(random.choice(rows).copy())
        
        # Écrire le fichier CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id_region', 'id_batiment', 'date_rapport', 
                                                    'emission_CO2_kg', 'taux_recyclage'])
            writer.writeheader()
            writer.writerows(rows)
        
        return filepath, len(rows)
    
    def generer_tous_rapports(self, date_debut, date_fin, output_dir='output/csv'):
        """Génère tous les rapports mensuels pour une période"""
        print("\n" + "="*60)
        print("📄 GÉNÉRATION DES FICHIERS CSV ENVIRONNEMENTAUX")
        print("="*60 + "\n")
        
        fichiers_generes = []
        date_courante = date_debut
        
        while date_courante <= date_fin:
            filepath, nb_rows = self.generer_rapport_mensuel(
                date_courante.month,
                date_courante.year,
                output_dir
            )
            fichiers_generes.append(filepath)
            print(f"  ✓ {os.path.basename(filepath)} - {nb_rows} enregistrements")
            
            # Passer au mois suivant
            if date_courante.month == 12:
                date_courante = datetime(date_courante.year + 1, 1, 1)
            else:
                date_courante = datetime(date_courante.year, date_courante.month + 1, 1)
        
        print(f"\n✅ {len(fichiers_generes)} fichiers CSV générés dans {output_dir}")
        return fichiers_generes


def generer_exemple_csv():
    """Génère les fichiers CSV d'exemple"""
    from generate_mysql_data import GreenCityDataGenerator
    
    # Générer d'abord les données de base
    generator = GreenCityDataGenerator()
    generator.generer_regions()
    generator.generer_types_energie()
    generator.generer_batiments()
    
    # Générer les fichiers CSV pour 2024
    csv_gen = CSVEnvironnementalGenerator(
        generator.batiments,
        generator.regions
    )
    
    csv_gen.generer_tous_rapports(
        datetime(2024, 1, 1),
        datetime(2025, 1, 31),
        'output/csv'
    )


if __name__ == "__main__":
    generer_exemple_csv()
