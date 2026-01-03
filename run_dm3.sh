#!/bin/bash
# Script pour lancer le pipeline ETL DM3 Environnement

PENTAHO_HOME="/Users/kihlyouns/Desktop/GreenCity_ETL/Pentaho"
DM3_DIR="/Users/kihlyouns/Desktop/GreenCity_ETL/pentaho_etl/dm3_environnement"
LAST_RUN_FILE="${DM3_DIR}/.last_run"

# Récupérer la date de dernière exécution
if [ -f "$LAST_RUN_FILE" ]; then
  LAST_RUN_DATE=$(cat "$LAST_RUN_FILE")
else
  LAST_RUN_DATE="1900-01-01"
fi

echo "=========================================="
echo "DM3 ETL - START"
echo "=========================================="
echo "Date dernière exécution: $LAST_RUN_DATE"
echo ""

# Étape 1: Extraction
echo "[1/3] Extraction CSV..."
"$PENTAHO_HOME/pan.sh" -file "$DM3_DIR/1_extract_csv.ktr" 2>&1 | grep -E "ERROR|Finished|lines"
if [ $? -ne 0 ]; then
  echo "ERREUR: Extraction échouée"
  exit 1
fi

# Étape 2: Transformation
echo "[2/3] Transformation..."
"$PENTAHO_HOME/pan.sh" -file "$DM3_DIR/2_transform_env.ktr" 2>&1 | grep -E "ERROR|Finished|lines"
if [ $? -ne 0 ]; then
  echo "ERREUR: Transformation échouée"
  exit 1
fi

# Étape 3: Chargement
echo "[3/3] Chargement Data Mart..."
"$PENTAHO_HOME/pan.sh" -file "$DM3_DIR/3_load_dm3.ktr" -param:LAST_RUN_DATE="$LAST_RUN_DATE" 2>&1 | grep -E "ERROR|Finished|lines"
if [ $? -ne 0 ]; then
  echo "ERREUR: Chargement échoué"
  exit 1
fi

# Mettre à jour la date de dernière exécution
echo "$(date +'%Y-%m-%d')" > "$LAST_RUN_FILE"

echo ""
echo "=========================================="
echo "DM3 ETL - SUCCESS!"
echo "=========================================="
