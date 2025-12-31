#!/bin/bash

# Script d'installation et de lancement rapide pour GreenCity

echo "========================================================================"
echo "GREENCITY - Installation du Systeme de Generation de Donnees"
echo "========================================================================"
echo ""

# Verifier que Python est installe
if ! command -v python3 &> /dev/null; then
    echo "Erreur: Python 3 n'est pas installe. Veuillez l'installer d'abord."
    exit 1
fi

echo "✓ Python 3 detecte: $(python3 --version)"
echo ""

# Creer l'environnement virtuel
echo "Creation de l'environnement virtuel..."
python3 -m venv .venv

if [ $? -ne 0 ]; then
    echo "Erreur lors de la creation du venv"
    exit 1
fi

echo "✓ Environnement virtuel cree avec succes"
echo ""

# Activer le venv
echo "Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installer les dependances
echo "Installation des dependances..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependances installees avec succes"
else
    echo "Erreur lors de l'installation des dependances"
    exit 1
fi

echo ""
echo "========================================================================"
echo "Installation terminee avec succes!"
echo "========================================================================"
echo ""
echo "L'environnement virtuel est ACTIVE dans ce terminal."
echo ""
echo "Pour lancer la generation de donnees, executez:"
echo "  cd scripts"
echo "  python main.py"
echo ""
echo "IMPORTANT: L'environnement virtuel est active uniquement dans ce terminal."
echo "Pour utiliser le venv dans un autre terminal, executez:"
echo "  source .venv/bin/activate"
echo ""

