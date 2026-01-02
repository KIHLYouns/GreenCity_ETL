# -*- coding: utf-8 -*-
# generate_json_files.py - Génération des fichiers JSON de consommation IoT

import json
import random
import os
from datetime import datetime, timedelta
from config import *

random.seed(42)

class JSONConsommationGenerator:
    def __init__(self, batiments, compteurs, regions):
        self.batiments = batiments
        self.compteurs = compteurs
        self.regions = regions
        
    def generer_mesures_horaires(self, compteur_id, type_energie, date_mesure, nb_heures=24):
        """Génère des mesures horaires pour un compteur"""
        mesures = []
        
        for heure in range(nb_heures):
            datetime_mesure = date_mesure.replace(hour=heure, minute=0, second=0)
            
            # Valeurs de consommation réalistes par type
            if type_energie == 'electricite':
                base_conso = random.uniform(80, 200)
                # Plus de consommation en journée (8h-18h)
                if 8 <= heure <= 18:
                    base_conso *= random.uniform(1.2, 1.8)
                cle_conso = 'consommation_kWh'
            elif type_energie == 'eau':
                base_conso = random.uniform(0.5, 3.0)
                # Plus de consommation le matin et soir
                if heure in [7, 8, 9, 18, 19, 20]:
                    base_conso *= random.uniform(1.5, 2.5)
                cle_conso = 'consommation_m3'
            else:  # gaz
                base_conso = random.uniform(2.0, 8.0)
                # Plus de consommation en hiver (basé sur le mois)
                if date_mesure.month in [11, 12, 1, 2, 3]:
                    base_conso *= random.uniform(1.5, 2.5)
                cle_conso = 'consommation_m3'
            
            # Introduire des défauts de qualité
            mesure = {
                'compteur_id': compteur_id,
                'date_mesure': datetime_mesure.isoformat()
            }
            
            # Parfois valeur manquante
            if random.random() < DEFAUTS_QUALITE['taux_valeurs_manquantes']:
                mesure[cle_conso] = None
            # Parfois valeur incohérente (négative ou très élevée)
            elif random.random() < DEFAUTS_QUALITE['taux_valeurs_incoherentes']:
                mesure[cle_conso] = round(-base_conso if random.random() < 0.5 else base_conso * 100, 2)
            else:
                mesure[cle_conso] = round(base_conso, 2)
            
            mesures.append(mesure)
        
        # Ajouter quelques doublons
        if random.random() < DEFAUTS_QUALITE['taux_doublons'] * 5:  # 5% de chance de doublon
            mesures.append(random.choice(mesures).copy())
        
        return mesures
    
    def generer_fichier_json_journalier(self, type_energie, date, output_dir='output/json'):
        """Génère un fichier JSON pour un type d'énergie et une date"""
        
        type_map = {
            'electricite': {'prefixe': 'ELEC', 'unite': 'kWh', 'id': 1},
            'eau': {'prefixe': 'EAU', 'unite': 'm3', 'id': 2},
            'gaz': {'prefixe': 'GAZ', 'unite': 'm3', 'id': 3}
        }
        
        config_type = type_map[type_energie]
        data = []
        
        # Grouper par région
        for region in self.regions:
            region_id = region['id_region']
            
            # Trouver les bâtiments de cette région
            batiments_region = [b for b in self.batiments if b['id_region'] == region_id]
            
            for batiment in batiments_region:
                # Trouver les compteurs de ce bâtiment pour ce type d'énergie
                compteurs_batiment = [
                    c for c in self.compteurs 
                    if c['id_batiment'] == batiment['id_batiment'] 
                    and c['id_type_energie'] == config_type['id']
                ]
                
                if compteurs_batiment:
                    batiment_data = {
                        'id_region': region_id,
                        'id_batiment': batiment['id_batiment'],
                        'type_energie': type_energie,
                        'unite': config_type['unite'],
                        'date_generation': date.strftime('%Y-%m-%d'),
                        'mesures': []
                    }
                    
                    for compteur in compteurs_batiment:
                        mesures = self.generer_mesures_horaires(
                            compteur['id_compteur'],
                            type_energie,
                            date
                        )
                        batiment_data['mesures'].extend(mesures)
                    
                    data.append(batiment_data)
        
        # Écrire le fichier JSON
        mois_str = date.strftime('%m_%Y')
        jour_str = date.strftime('%d')
        filename = f"{type_energie.capitalize()}_consumption_{jour_str}_{mois_str}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def generer_tous_fichiers_json(self, date_debut, date_fin, output_dir='output/json'):
        """Génère tous les fichiers JSON pour une période"""
        print("\n" + "="*60)
        print("📄 GÉNÉRATION DES FICHIERS JSON DE CONSOMMATION")
        print("="*60 + "\n")
        
        os.makedirs(output_dir, exist_ok=True)
        
        types_energie = ['electricite', 'eau', 'gaz']
        fichiers_generes = []
        
        date_courante = date_debut
        total_jours = (date_fin - date_debut).days + 1
        
        for i, _ in enumerate(range(total_jours)):
            for type_energie in types_energie:
                filepath = self.generer_fichier_json_journalier(
                    type_energie, 
                    date_courante, 
                    output_dir
                )
                fichiers_generes.append(filepath)
            
            if (i + 1) % 30 == 0 or i == total_jours - 1:
                print(f"  ✓ Jour {i+1}/{total_jours} traité - {date_courante.strftime('%Y-%m-%d')}")
            
            date_courante += timedelta(days=1)
        
        print(f"\n✅ {len(fichiers_generes)} fichiers JSON générés dans {output_dir}")
        return fichiers_generes


def generer_exemple_json():
    """Génère quelques fichiers JSON d'exemple"""
    from generate_mysql_data import GreenCityDataGenerator
    
    # Générer d'abord les données de base
    generator = GreenCityDataGenerator()
    generator.generer_regions()
    generator.generer_types_energie()
    generator.generer_batiments()
    generator.generer_compteurs()
    
    # Générer les fichiers JSON pour janvier 2025
    json_gen = JSONConsommationGenerator(
        generator.batiments,
        generator.compteurs,
        generator.regions
    )
    
    # Générer pour une semaine d'exemple
    json_gen.generer_tous_fichiers_json(
        datetime(2025, 1, 1),
        datetime(2025, 1, 7),  # 1 semaine
        'output/json'
    )


if __name__ == "__main__":
    generer_exemple_json()
