# -*- coding: utf-8 -*-
# config.py - Configuration centrale

import random
from datetime import datetime, timedelta

# ============================================
# PARAMÈTRES DE GÉNÉRATION
# ============================================

# Volumes de données
CONFIG = {
    'nb_regions': 8,
    'nb_batiments': 50,
    'nb_clients': 200,
    'nb_compteurs_par_batiment': 3,  # 1 par type d'énergie
    'nb_contrats': 180,
    'nb_factures_par_contrat': 12,   # ~1 an de factures
    'nb_paiements_ratio': 0.85,       # 85% des factures payées
    'nb_temperatures_par_region': 365,  # 1 an de données
}

# Période de données
DATE_DEBUT = datetime(2024, 1, 1)
DATE_FIN = datetime(2025, 1, 31)

# Taux d'erreurs pour les défauts de qualité
DEFAUTS_QUALITE = {
    'taux_valeurs_manquantes': 0.02,    # 2%
    'taux_doublons': 0.01,               # 1%
    'taux_espaces_inutiles': 0.03,       # 3%
    'taux_format_date_incorrect': 0.02,  # 2%
    'taux_valeurs_incoherentes': 0.02,   # 2%
}

# Types d'énergie
TYPES_ENERGIE = [
    {'id': 1, 'libelle': 'Électricité', 'unite': 'kWh'},
    {'id': 2, 'libelle': 'Eau', 'unite': 'm³'},
    {'id': 3, 'libelle': 'Gaz', 'unite': 'm³'},
]

# Sites/Zones marocains (Tanger et Tétouan avec plusieurs régions chacune)
REGIONS_DATA = [
    {'id': 'REG01', 'nom': 'Centre-Ville Tanger', 'pays': 'Maroc', 'ville': 'Tanger', 'code_postal': '90000'},
    {'id': 'REG02', 'nom': 'Quartier Charf Tanger', 'pays': 'Maroc', 'ville': 'Tanger', 'code_postal': '90000'},
    {'id': 'REG03', 'nom': 'Quartier Mgharza Tanger', 'pays': 'Maroc', 'ville': 'Tanger', 'code_postal': '90000'},
    {'id': 'REG04', 'nom': 'Quartier Ben Diab Tanger', 'pays': 'Maroc', 'ville': 'Tanger', 'code_postal': '90000'},
    {'id': 'REG05', 'nom': 'Centre-Ville Tétouan', 'pays': 'Maroc', 'ville': 'Tétouan', 'code_postal': '93000'},
    {'id': 'REG06', 'nom': 'Quartier Moulay Mehdi Tétouan', 'pays': 'Maroc', 'ville': 'Tétouan', 'code_postal': '93000'},
    {'id': 'REG07', 'nom': 'Quartier Sidi Mandri Tétouan', 'pays': 'Maroc', 'ville': 'Tétouan', 'code_postal': '93000'},
    {'id': 'REG08', 'nom': 'Quartier Oued Laou Tétouan', 'pays': 'Maroc', 'ville': 'Tétouan', 'code_postal': '93000'},
]

# Connexion MySQL
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'greencity_facturation'
}
