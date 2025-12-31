# Guide de Demarrage Rapide - GreenCity

## Installation en 3 etapes (avec venv)

### Etape 1 : Creer et activer l'environnement virtuel

```bash
cd greencity_data_generation

# Creer le venv
python3 -m venv .venv

# Activer le venv
source .venv/bin/activate
```

Vous devez voir `(.venv)` au debut de votre terminal.

### Etape 2 : Installer les dependances

Une fois le venv active :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Etape 3 : Lancer la generation

```bash
cd scripts
python main.py
```

## Resultats attendus

```
======================================================================
GREENCITY - SYSTEME DE GENERATION DE DONNEES
======================================================================
Periode: 2024-01-01 -> 2025-01-31
======================================================================

ETAPE 1: Generation des donnees MySQL...
... Generation en cours ...

ETAPE 2: Generation des fichiers JSON (consommation IoT)...
... Generation en cours ...

ETAPE 3: Generation des fichiers CSV (rapports environnementaux)...
... Generation en cours ...

GENERATION TERMINEE AVEC SUCCES!
```

Les fichiers sont generes dans le dossier `output/` :

```bash
ls -la output/sql/     # Script SQL
ls -la output/json/    # Fichiers JSON IoT
ls -la output/csv/     # Rapports CSV
```

## Alternative : Utiliser le script d'installation

```bash
cd greencity_data_generation
chmod +x install.sh
./install.sh
```

Le script creera automatiquement le venv et installera les dependances.

## Desactiver le venv

Quand vous avez termine :

```bash
deactivate
```

## Importer dans MySQL

```bash
# Creer la base de donnees
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS greencity_facturation;"

# Importer les donnees generees
mysql -u root -p greencity_facturation < output/sql/insert_data.sql
```

## Personnalisation

Modifiez `scripts/config.py` pour ajuster :

- Le nombre de regions, batiments, clients, etc.
- Les dates de generation
- Les taux d'erreurs pour les defauts de qualite

## Exemples d'usage

### Python

```python
# Lire les fichiers JSON
import json
with open('output/json/Electricite_consumption_01_01_2025.json', 'r') as f:
    data = json.load(f)

# Lire les fichiers CSV
import pandas as pd
df = pd.read_csv('output/csv/env_reports_01_2024.csv')
```

### SQL

```sql
-- Verifier les donnees importees
SELECT COUNT(*) FROM regions;
SELECT COUNT(*) FROM batiments;
SELECT COUNT(*) FROM clients;
SELECT COUNT(*) FROM factures;
```

## Caracteristiques

- Respect des cles etrangeres
- Donnees realistes (faker FR)
- Defauts de qualite controles (2-3%)
- Generation reproductible (seed=42)
- Multi-formats (SQL, JSON, CSV)

## Depannage

### Erreur "No module named 'faker'"

Verifiez que le venv est active :

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Erreur MySQL

- Verifiez que MySQL est demarr
- Verifiez les identifiants dans `scripts/config.py`
- Verifiez que la base de donnees existe

### Fichiers non generes

- Verifiez les permissions d'ecriture dans le dossier
- Verifiez l'espace disque disponible

## Documentation complete

Consultez `README.md` pour la documentation complete du projet.
