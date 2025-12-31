# -*- coding: utf-8 -*-
# generate_mysql_data.py - Génération des données MySQL avec relations

import random
import string
from datetime import datetime, timedelta
from faker import Faker
import mysql.connector
from config import *

fake = Faker('fr_FR')
Faker.seed(42)
random.seed(42)

class GreenCityDataGenerator:
    def __init__(self):
        self.regions = []
        self.types_energie = []
        self.batiments = []
        self.compteurs = []
        self.clients = []
        self.contrats = []
        self.factures = []
        self.paiements = []
        self.tarifs = []
        self.temperatures = []
        
    # ============================================
    # FONCTIONS UTILITAIRES POUR DÉFAUTS DE QUALITÉ
    # ============================================
    
    def ajouter_espaces(self, valeur):
        """Ajoute des espaces inutiles avant/après"""
        if random.random() < DEFAUTS_QUALITE['taux_espaces_inutiles']:
            espaces_avant = ' ' * random.randint(1, 3)
            espaces_apres = ' ' * random.randint(1, 3)
            return f"{espaces_avant}{valeur}{espaces_apres}"
        return valeur
    
    def valeur_manquante(self, valeur):
        """Retourne NULL aléatoirement"""
        if random.random() < DEFAUTS_QUALITE['taux_valeurs_manquantes']:
            return None
        return valeur
    
    def format_date_incorrect(self, date_obj):
        """Retourne parfois un format de date incorrect"""
        if random.random() < DEFAUTS_QUALITE['taux_format_date_incorrect']:
            formats_incorrects = [
                date_obj.strftime('%d/%m/%Y'),
                date_obj.strftime('%m-%d-%Y'),
                date_obj.strftime('%Y/%m/%d'),
                str(date_obj.timestamp()),
            ]
            return random.choice(formats_incorrects)
        return date_obj.strftime('%Y-%m-%d')
    
    def valeur_incoherente(self, valeur, type_valeur='numeric'):
        """Introduit des valeurs incohérentes"""
        if random.random() < DEFAUTS_QUALITE['taux_valeurs_incoherentes']:
            if type_valeur == 'numeric':
                return -abs(valeur) if random.random() < 0.5 else valeur * 100
            elif type_valeur == 'email':
                return valeur.replace('@', '@@') if '@' in str(valeur) else valeur
        return valeur

    # ============================================
    # GÉNÉRATION DES TABLES
    # ============================================
    
    def generer_regions(self):
        """Génère les régions"""
        print("📍 Génération des régions...")
        for region in REGIONS_DATA[:CONFIG['nb_regions']]:
            self.regions.append({
                'id_region': region['id'],
                'nom_region': self.ajouter_espaces(region['nom']),
                'pays': region['pays'],
                'ville': region['ville'],
                'code_postal': region['code_postal']
            })
        print(f"   ✓ {len(self.regions)} régions générées")
        return self.regions
    
    def generer_types_energie(self):
        """Génère les types d'énergie"""
        print("⚡ Génération des types d'énergie...")
        for te in TYPES_ENERGIE:
            self.types_energie.append({
                'id_type_energie': te['id'],
                'libelle': te['libelle'],
                'unite': te['unite']
            })
        print(f"   ✓ {len(self.types_energie)} types d'énergie générés")
        return self.types_energie
    
    def generer_batiments(self):
        """Génère les bâtiments (FK: id_region)"""
        print("🏢 Génération des bâtiments...")
        types_batiment = ['Résidentiel', 'Commercial', 'Industriel', 'Mixte']
        noms_batiments = ['Tour', 'Résidence', 'Immeuble', 'Centre', 'Complexe', 'Pavillon']
        
        for i in range(CONFIG['nb_batiments']):
            id_region = random.choice(self.regions)['id_region']
            nom = f"{random.choice(noms_batiments)} {fake.last_name()}"
            
            batiment = {
                'id_batiment': f"BAT{str(i+1).zfill(3)}",
                'id_region': id_region,
                'nom_batiment': self.ajouter_espaces(nom),
                'adresse': self.valeur_manquante(fake.street_address()),
                'surface_m2': round(random.uniform(500, 15000), 2),
                'type_batiment': random.choice(types_batiment),
                'nb_etages': random.randint(1, 5),
                'annee_construction': random.randint(1980, 2023)
            }
            
            # Introduire quelques incohérences (surface négative)
            if random.random() < DEFAUTS_QUALITE['taux_valeurs_incoherentes']:
                batiment['surface_m2'] = -batiment['surface_m2']
            
            self.batiments.append(batiment)
        
        # Ajouter quelques doublons
        nb_doublons = int(len(self.batiments) * DEFAUTS_QUALITE['taux_doublons'])
        for _ in range(nb_doublons):
            doublon = random.choice(self.batiments).copy()
            doublon['id_batiment'] = f"BAT{str(CONFIG['nb_batiments'] + _ + 1).zfill(3)}"
            self.batiments.append(doublon)
        
        print(f"   ✓ {len(self.batiments)} bâtiments générés")
        return self.batiments
    
    def generer_compteurs(self):
        """Génère les compteurs (FK: id_batiment, id_type_energie)"""
        print("📊 Génération des compteurs...")
        statuts = ['Actif', 'Actif', 'Actif', 'Inactif', 'Maintenance']  # Majorité actifs
        
        compteur_id = 1
        for batiment in self.batiments:
            for type_energie in self.types_energie:
                prefixe = {'Électricité': 'ELEC', 'Eau': 'EAU', 'Gaz': 'GAZ'}
                
                compteur = {
                    'id_compteur': f"{prefixe[type_energie['libelle']]}_{str(compteur_id).zfill(4)}",
                    'id_batiment': batiment['id_batiment'],
                    'id_type_energie': type_energie['id_type_energie'],
                    'date_installation': fake.date_between(
                        start_date=datetime(2015, 1, 1),
                        end_date=datetime(2023, 12, 31)
                    ).strftime('%Y-%m-%d'),
                    'statut': random.choice(statuts)
                }
                self.compteurs.append(compteur)
                compteur_id += 1
        
        print(f"   ✓ {len(self.compteurs)} compteurs générés")
        return self.compteurs
    
    def generer_clients(self):
        """Génère les clients (FK: id_region)"""
        print("👥 Génération des clients...")
        
        for i in range(CONFIG['nb_clients']):
            type_client = random.choice(['Particulier', 'Entreprise'])
            id_region = random.choice(self.regions)['id_region']
            
            if type_client == 'Particulier':
                nom = fake.last_name()
                prenom = fake.first_name()
            else:
                nom = fake.company()
                prenom = None
            
            email = fake.email()
            # Parfois email invalide
            if random.random() < DEFAUTS_QUALITE['taux_valeurs_incoherentes']:
                email = email.replace('@', '@@')
            
            client = {
                'id_client': f"CLI{str(i+1).zfill(5)}",
                'nom': self.ajouter_espaces(nom),
                'prenom': self.valeur_manquante(prenom),
                'email': self.valeur_manquante(email),
                'telephone': self.valeur_manquante(fake.phone_number()),
                'type_client': type_client,
                'adresse': fake.address().replace('\n', ', '),
                'id_region': id_region,
                'date_inscription': fake.date_between(
                    start_date=datetime(2020, 1, 1),
                    end_date=datetime(2024, 12, 31)
                ).strftime('%Y-%m-%d'),
                'statut': random.choices(['Actif', 'Inactif'], weights=[0.9, 0.1])[0]
            }
            self.clients.append(client)
        
        print(f"   ✓ {len(self.clients)} clients générés")
        return self.clients
    
    def generer_contrats(self):
        """Génère les contrats (FK: id_client, id_compteur)"""
        print("📝 Génération des contrats...")
        statuts_contrat = ['Actif', 'Terminé', 'Suspendu', 'Résilié']
        
        # Assurer que chaque compteur peut avoir plusieurs contrats
        compteurs_disponibles = self.compteurs.copy()
        
        for i in range(CONFIG['nb_contrats']):
            client = random.choice(self.clients)
            compteur = random.choice(compteurs_disponibles)
            
            date_debut = fake.date_between(
                start_date=datetime(2022, 1, 1),
                end_date=datetime(2024, 6, 30)
            )
            
            # 70% des contrats sont actifs (pas de date_fin)
            if random.random() < 0.7:
                date_fin = None
                statut = 'Actif'
            else:
                date_fin = date_debut + timedelta(days=random.randint(180, 730))
                statut = random.choice(['Terminé', 'Résilié'])
            
            contrat = {
                'id_contrat': f"CTR{str(i+1).zfill(6)}",
                'id_client': client['id_client'],
                'id_compteur': compteur['id_compteur'],
                'date_debut': date_debut.strftime('%Y-%m-%d'),
                'date_fin': date_fin.strftime('%Y-%m-%d') if date_fin else None,
                'statut': statut
            }
            self.contrats.append(contrat)
        
        print(f"   ✓ {len(self.contrats)} contrats générés")
        return self.contrats
    
    def generer_tarifs(self):
        """Génère l'historique des tarifs (FK: id_type_energie)"""
        print("💰 Génération des tarifs...")
        
        # Tarifs par type d'énergie
        tarifs_base = {
            1: {'achat': 0.08, 'vente': 0.15},   # Électricité
            2: {'achat': 2.50, 'vente': 4.20},   # Eau
            3: {'achat': 0.05, 'vente': 0.09},   # Gaz
        }
        
        for type_id, prix in tarifs_base.items():
            # Plusieurs périodes tarifaires
            date_courante = datetime(2022, 1, 1)
            
            while date_courante < datetime(2025, 1, 1):
                variation = random.uniform(0.95, 1.15)  # ±15%
                
                tarif = {
                    'id_type_energie': type_id,
                    'cout_achat_unitaire': round(prix['achat'] * variation, 4),
                    'prix_vente_unitaire': round(prix['vente'] * variation, 4),
                    'date_debut': date_courante.strftime('%Y-%m-%d'),
                    'date_fin': (date_courante + timedelta(days=180)).strftime('%Y-%m-%d')
                }
                self.tarifs.append(tarif)
                date_courante += timedelta(days=180)
        
        print(f"   ✓ {len(self.tarifs)} tarifs générés")
        return self.tarifs
    
    def generer_factures(self):
        """Génère les factures (FK: id_contrat)"""
        print("🧾 Génération des factures...")
        
        facture_id = 1
        for contrat in self.contrats:
            # Trouver le compteur et son type d'énergie
            compteur = next(c for c in self.compteurs if c['id_compteur'] == contrat['id_compteur'])
            type_energie_id = compteur['id_type_energie']
            
            date_debut_contrat = datetime.strptime(contrat['date_debut'], '%Y-%m-%d')
            date_fin_contrat = datetime.strptime(contrat['date_fin'], '%Y-%m-%d') if contrat['date_fin'] else datetime(2025, 1, 31)
            
            # Générer une facture par mois
            date_courante = date_debut_contrat
            mois_count = 0
            
            while date_courante < date_fin_contrat and mois_count < CONFIG['nb_factures_par_contrat']:
                periode_debut = date_courante
                periode_fin = date_courante + timedelta(days=30)
                
                # Calcul consommation et montants
                if type_energie_id == 1:  # Électricité
                    consommation = round(random.uniform(200, 2000), 2)
                    cout_unitaire = 0.15
                elif type_energie_id == 2:  # Eau
                    consommation = round(random.uniform(10, 100), 2)
                    cout_unitaire = 4.20
                else:  # Gaz
                    consommation = round(random.uniform(50, 500), 2)
                    cout_unitaire = 0.09
                
                cout_energie = round(consommation * cout_unitaire * 0.6, 2)  # Coût d'achat
                montant_ht = round(consommation * cout_unitaire, 2)
                tva = 20.00
                montant_ttc = round(montant_ht * 1.20, 2)
                
                # Statut de paiement
                statut = random.choices(
                    ['Payée', 'En attente', 'En retard'],
                    weights=[0.75, 0.15, 0.10]
                )[0]
                
                facture = {
                    'id_facture': f"FAC{str(facture_id).zfill(8)}",
                    'id_contrat': contrat['id_contrat'],
                    'date_emission': periode_fin.strftime('%Y-%m-%d'),
                    'date_echeance': (periode_fin + timedelta(days=30)).strftime('%Y-%m-%d'),
                    'periode_debut': periode_debut.strftime('%Y-%m-%d'),
                    'periode_fin': periode_fin.strftime('%Y-%m-%d'),
                    'montant_ht': montant_ht,
                    'tva': tva,
                    'montant_ttc': montant_ttc,
                    'cout_energie': cout_energie,
                    'consommation': consommation,
                    'statut_paiement': statut
                }
                
                # Introduire quelques incohérences
                if random.random() < DEFAUTS_QUALITE['taux_valeurs_incoherentes']:
                    facture['montant_ht'] = -facture['montant_ht']
                
                self.factures.append(facture)
                facture_id += 1
                date_courante += timedelta(days=30)
                mois_count += 1
        
        print(f"   ✓ {len(self.factures)} factures générées")
        return self.factures
    
    def generer_paiements(self):
        """Génère les paiements (FK: id_facture)"""
        print("💳 Génération des paiements...")
        
        modes_paiement = ['Virement', 'Carte bancaire', 'Prélèvement', 'Chèque', 'Espèces']
        paiement_id = 1
        
        for facture in self.factures:
            if facture['statut_paiement'] == 'Payée':
                date_echeance = datetime.strptime(facture['date_echeance'], '%Y-%m-%d')
                
                # Date de paiement (avant ou après échéance)
                jours_decalage = random.randint(-15, 10)
                date_paiement = date_echeance + timedelta(days=jours_decalage)
                
                paiement = {
                    'id_paiement': f"PAY{str(paiement_id).zfill(8)}",
                    'id_facture': facture['id_facture'],
                    'date_paiement': date_paiement.strftime('%Y-%m-%d'),
                    'montant': facture['montant_ttc'],
                    'mode_paiement': random.choice(modes_paiement),
                    'reference_transaction': ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
                }
                self.paiements.append(paiement)
                paiement_id += 1
        
        print(f"   ✓ {len(self.paiements)} paiements générés")
        return self.paiements
    
    def generer_temperatures(self):
        """Génère les températures (FK: id_region)"""
        print("🌡️ Génération des températures...")
        
        # Températures moyennes par saison
        temp_base = {
            'hiver': {'min': -5, 'max': 10, 'moy': 3},
            'printemps': {'min': 5, 'max': 20, 'moy': 12},
            'ete': {'min': 15, 'max': 35, 'moy': 25},
            'automne': {'min': 5, 'max': 18, 'moy': 11}
        }
        
        for region in self.regions:
            date_courante = DATE_DEBUT
            
            while date_courante <= DATE_FIN:
                mois = date_courante.month
                
                # Déterminer la saison
                if mois in [12, 1, 2]:
                    saison = 'hiver'
                elif mois in [3, 4, 5]:
                    saison = 'printemps'
                elif mois in [6, 7, 8]:
                    saison = 'ete'
                else:
                    saison = 'automne'
                
                base = temp_base[saison]
                variation = random.uniform(-3, 3)
                
                temp = {
                    'id_region': region['id_region'],
                    'date_mesure': date_courante.strftime('%Y-%m-%d'),
                    'temperature_min': round(base['min'] + variation, 2),
                    'temperature_max': round(base['max'] + variation, 2),
                    'temperature_moyenne': round(base['moy'] + variation, 2)
                }
                
                # Parfois format de date incorrect
                if random.random() < DEFAUTS_QUALITE['taux_format_date_incorrect']:
                    temp['date_mesure'] = date_courante.strftime('%d/%m/%Y')
                
                self.temperatures.append(temp)
                date_courante += timedelta(days=1)
        
        print(f"   ✓ {len(self.temperatures)} enregistrements de température générés")
        return self.temperatures

    # ============================================
    # EXPORT SQL
    # ============================================
    
    def escape_sql(self, value):
        """Échappe les valeurs pour SQL"""
        if value is None:
            return 'NULL'
        if isinstance(value, str):
            return f"'{value.replace(chr(39), chr(39)+chr(39))}'"
        return str(value)
    
    def generer_sql_inserts(self, filename='output/sql/insert_data.sql'):
        """Génère le fichier SQL avec tous les INSERT"""
        print("\n📄 Génération du fichier SQL...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("-- ============================================\n")
            f.write("-- DONNÉES GÉNÉRÉES AUTOMATIQUEMENT - GREENCITY\n")
            f.write(f"-- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- ============================================\n\n")
            f.write("USE greencity_facturation;\n\n")
            
            # Désactiver les contraintes FK temporairement
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            # REGIONS
            f.write("-- REGIONS\n")
            for r in self.regions:
                f.write(f"INSERT INTO regions (id_region, nom_region, pays, ville, code_postal) VALUES "
                       f"({self.escape_sql(r['id_region'])}, {self.escape_sql(r['nom_region'])}, "
                       f"{self.escape_sql(r['pays'])}, {self.escape_sql(r['ville'])}, "
                       f"{self.escape_sql(r['code_postal'])});\n")
            
            # TYPES_ENERGIE
            f.write("\n-- TYPES_ENERGIE\n")
            for te in self.types_energie:
                f.write(f"INSERT INTO types_energie (id_type_energie, libelle, unite) VALUES "
                       f"({te['id_type_energie']}, {self.escape_sql(te['libelle'])}, "
                       f"{self.escape_sql(te['unite'])});\n")
            
            # BATIMENTS
            f.write("\n-- BATIMENTS\n")
            for b in self.batiments:
                f.write(f"INSERT INTO batiments (id_batiment, id_region, nom_batiment, adresse, "
                       f"surface_m2, type_batiment, nb_etages, annee_construction) VALUES "
                       f"({self.escape_sql(b['id_batiment'])}, {self.escape_sql(b['id_region'])}, "
                       f"{self.escape_sql(b['nom_batiment'])}, {self.escape_sql(b['adresse'])}, "
                       f"{b['surface_m2']}, {self.escape_sql(b['type_batiment'])}, "
                       f"{b['nb_etages']}, {b['annee_construction']});\n")
            
            # COMPTEURS
            f.write("\n-- COMPTEURS\n")
            for c in self.compteurs:
                f.write(f"INSERT INTO compteurs (id_compteur, id_batiment, id_type_energie, "
                       f"date_installation, statut) VALUES "
                       f"({self.escape_sql(c['id_compteur'])}, {self.escape_sql(c['id_batiment'])}, "
                       f"{c['id_type_energie']}, {self.escape_sql(c['date_installation'])}, "
                       f"{self.escape_sql(c['statut'])});\n")
            
            # CLIENTS
            f.write("\n-- CLIENTS\n")
            for cl in self.clients:
                f.write(f"INSERT INTO clients (id_client, nom, prenom, email, telephone, "
                       f"type_client, adresse, id_region, date_inscription, statut) VALUES "
                       f"({self.escape_sql(cl['id_client'])}, {self.escape_sql(cl['nom'])}, "
                       f"{self.escape_sql(cl['prenom'])}, {self.escape_sql(cl['email'])}, "
                       f"{self.escape_sql(cl['telephone'])}, {self.escape_sql(cl['type_client'])}, "
                       f"{self.escape_sql(cl['adresse'])}, {self.escape_sql(cl['id_region'])}, "
                       f"{self.escape_sql(cl['date_inscription'])}, {self.escape_sql(cl['statut'])});\n")
            
            # CONTRATS
            f.write("\n-- CONTRATS\n")
            for ct in self.contrats:
                f.write(f"INSERT INTO contrats (id_contrat, id_client, id_compteur, "
                       f"date_debut, date_fin, statut) VALUES "
                       f"({self.escape_sql(ct['id_contrat'])}, {self.escape_sql(ct['id_client'])}, "
                       f"{self.escape_sql(ct['id_compteur'])}, {self.escape_sql(ct['date_debut'])}, "
                       f"{self.escape_sql(ct['date_fin'])}, {self.escape_sql(ct['statut'])});\n")
            
            # TARIFS
            f.write("\n-- TARIFS\n")
            for t in self.tarifs:
                f.write(f"INSERT INTO tarifs (id_type_energie, cout_achat_unitaire, "
                       f"prix_vente_unitaire, date_debut, date_fin) VALUES "
                       f"({t['id_type_energie']}, {t['cout_achat_unitaire']}, "
                       f"{t['prix_vente_unitaire']}, {self.escape_sql(t['date_debut'])}, "
                       f"{self.escape_sql(t['date_fin'])});\n")
            
            # FACTURES
            f.write("\n-- FACTURES\n")
            for fa in self.factures:
                f.write(f"INSERT INTO factures (id_facture, id_contrat, date_emission, "
                       f"date_echeance, periode_debut, periode_fin, montant_ht, tva, "
                       f"montant_ttc, cout_energie, consommation, statut_paiement) VALUES "
                       f"({self.escape_sql(fa['id_facture'])}, {self.escape_sql(fa['id_contrat'])}, "
                       f"{self.escape_sql(fa['date_emission'])}, {self.escape_sql(fa['date_echeance'])}, "
                       f"{self.escape_sql(fa['periode_debut'])}, {self.escape_sql(fa['periode_fin'])}, "
                       f"{fa['montant_ht']}, {fa['tva']}, {fa['montant_ttc']}, "
                       f"{fa['cout_energie']}, {fa['consommation']}, "
                       f"{self.escape_sql(fa['statut_paiement'])});\n")
            
            # PAIEMENTS
            f.write("\n-- PAIEMENTS\n")
            for p in self.paiements:
                f.write(f"INSERT INTO paiements (id_paiement, id_facture, date_paiement, "
                       f"montant, mode_paiement, reference_transaction) VALUES "
                       f"({self.escape_sql(p['id_paiement'])}, {self.escape_sql(p['id_facture'])}, "
                       f"{self.escape_sql(p['date_paiement'])}, {p['montant']}, "
                       f"{self.escape_sql(p['mode_paiement'])}, "
                       f"{self.escape_sql(p['reference_transaction'])});\n")
            
            # TEMPERATURES
            f.write("\n-- TEMPERATURES\n")
            for t in self.temperatures:
                f.write(f"INSERT INTO temperatures (id_region, date_mesure, temperature_min, "
                       f"temperature_max, temperature_moyenne) VALUES "
                       f"({self.escape_sql(t['id_region'])}, {self.escape_sql(t['date_mesure'])}, "
                       f"{t['temperature_min']}, {t['temperature_max']}, "
                       f"{t['temperature_moyenne']});\n")
            
            # Réactiver les contraintes FK
            f.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
        
        print(f"   ✓ Fichier SQL généré: {filename}")

    def generer_toutes_donnees(self):
        """Génère toutes les données dans l'ordre correct"""
        print("\n" + "="*60)
        print("🚀 GÉNÉRATION DES DONNÉES GREENCITY")
        print("="*60 + "\n")
        
        # Ordre important pour respecter les FK
        self.generer_regions()
        self.generer_types_energie()
        self.generer_batiments()
        self.generer_compteurs()
        self.generer_clients()
        self.generer_contrats()
        self.generer_tarifs()
        self.generer_factures()
        self.generer_paiements()
        self.generer_temperatures()
        
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DE LA GÉNÉRATION")
        print("="*60)
        print(f"  • Régions:        {len(self.regions)}")
        print(f"  • Types énergie:  {len(self.types_energie)}")
        print(f"  • Bâtiments:      {len(self.batiments)}")
        print(f"  • Compteurs:      {len(self.compteurs)}")
        print(f"  • Clients:        {len(self.clients)}")
        print(f"  • Contrats:       {len(self.contrats)}")
        print(f"  • Tarifs:         {len(self.tarifs)}")
        print(f"  • Factures:       {len(self.factures)}")
        print(f"  • Paiements:      {len(self.paiements)}")
        print(f"  • Températures:   {len(self.temperatures)}")
        print("="*60 + "\n")


if __name__ == "__main__":
    import os
    
    # Créer les dossiers de sortie
    os.makedirs('output/sql', exist_ok=True)
    os.makedirs('output/json', exist_ok=True)
    os.makedirs('output/csv', exist_ok=True)
    
    # Générer les données
    generator = GreenCityDataGenerator()
    generator.generer_toutes_donnees()
    generator.generer_sql_inserts()
    
    print("✅ Génération terminée avec succès!")
