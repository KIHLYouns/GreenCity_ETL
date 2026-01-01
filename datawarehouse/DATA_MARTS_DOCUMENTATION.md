# 📊 GreenCity Data Warehouse - Documentation des Data Marts

## Vue d'ensemble
Architecture en **Star Schema** avec 3 Data Marts spécialisés, partageant des dimensions communes et alimentés par les données transactionnelles opérationnelles.

---

## 🎯 Data Mart 1: CONSOMMATION ÉNERGÉTIQUE (dm_consommation)

### Objectif
Analyser et suivre la consommation énergétique par bâtiment, région, type d'énergie et période de temps.

### Table de Faits
- **`fait_consommation`** - Grain: 1 ligne par compteur/jour
  - Mesures: `quantite_consommee`, `cout_energie`, `temperature_moyenne`
  - Clés étrangères: `id_temps_fk`, `id_region_fk`, `id_batiment_fk`, `id_compteur_fk`, `id_type_energie_fk`

### Dimensions
| Dimension | Description | Grain |
|-----------|-------------|-------|
| `dim_temps` | Temps calendaire (jour, mois, année, trimestre) | 1 ligne/jour |
| `dim_region` | Régions géographiques (Tanger, Tétouan) | 1 ligne/région |
| `dim_batiment` | Bâtiments (surface, type, région) | 1 ligne/bâtiment |
| `dim_compteur` | Compteurs physiques (statut, type d'énergie) | 1 ligne/compteur |
| `dim_type_energie` | Types d'énergie (Électricité, Eau, Gaz) | 3 lignes |

### Sources de Données
- **Fichiers JSON IoT** → Mesures horaires de consommation
- **Base `greencity_facturation`** → Tables `compteurs`, `batiments`, `regions`, `types_energie`, `temperatures`

### KPI à Analyser
- **Consommation totale (kWh)** : par client, par bâtiment, par région et par période
- **Évolution de la consommation dans le temps** : graphique courbe pour tendances mensuelles/annuelles
- **Consommation vs Température** : corrélation entre consommation énergétique et température pour analyse saisonnière
- **Comparaison inter-bâtiments** : benchmarking de consommation par type de bâtiment
- **Consommation par type d'énergie** : répartition électricité/eau/gaz

---

## 💰 Data Mart 2: RENTABILITÉ ÉCONOMIQUE (dm_rentabilite)

### Objectif
Analyser la rentabilité, les revenus facturés, les taux de recouvrement et les paiements.

### Tables de Faits

#### 2a. `fait_rentabilite` - Grain: 1 ligne par facture
- Mesures: `montant_ht`, `tva`, `montant_ttc`, `cout_energie_total`, `consommation_total`
- Clés étrangères: `id_temps_fk`, `id_client_fk`, `id_contrat_fk`, `id_statut_paiement_fk`

#### 2b. `fait_paiement` - Grain: 1 ligne par paiement
- Mesures: `montant_paye`
- Clés étrangères: `id_temps_fk`, `id_client_fk`, `id_statut_paiement_fk`

### Dimensions
| Dimension | Description | Grain |
|-----------|-------------|-------|
| `dim_temps` | Temps calendaire | 1 ligne/jour |
| `dim_client` | Clients (particuliers, entreprises) | 1 ligne/client |
| `dim_contrat` | Contrats d'abonnement (statut, durée) | 1 ligne/contrat |
| `dim_statut_paiement` | Statuts: Payée, En attente, En retard, Partiel | 4 lignes (conformed) |

### Sources de Données
- **Base `greencity_facturation`** → Tables `factures`, `paiements`, `clients`, `contrats`, `tarifs`
- **Data Mart Consommation** → Montants énergétiques (join sur contrat/période)

### KPI à Analyser
- **Chiffre d'affaires (CA)** : somme des montants TTC par client, par bâtiment, par région et par période
- **Recouvrement des paiements (Taux de paiement)** : pourcentage de factures payées vs. impayées/partielles
- **Profitabilité / Marge** : marge = montant_TTC - coût_énergie (par client, bâtiment, région)
- **Rentabilité** : analyse par bâtiment, par région, par type d'énergie et par client
- **Classement des clients les plus rentables** : ranking clients par CA et marge générée
- **Analyse des délais de paiement** : délai moyen, clients en retard, taux de recouvrement

---

## 🌱 Data Mart 3: IMPACT ENVIRONNEMENTAL (dm_environnement)

### Objectif
Mesurer et analyser l'impact environnemental (émissions CO₂, taux de recyclage) par bâtiment et région.

### Table de Faits
- **`fait_environnement`** - Grain: 1 ligne par bâtiment/mois
  - Mesures: `emission_co2_kg`, `taux_recyclage`, `ratio_co2_consommation`
  - Clés étrangères: `id_temps_fk`, `id_region_fk`, `id_batiment_fk`

### Dimensions
| Dimension | Description | Grain |
|-----------|-------------|-------|
| `dim_temps` | Temps calendaire (mois) | 1 ligne/jour |
| `dim_region` | Régions géographiques | 1 ligne/région |
| `dim_batiment` | Bâtiments (type, surface, région) | 1 ligne/bâtiment |

### Sources de Données
- **Fichiers CSV mensuels** → Rapports environnementaux (`emission_CO2_kg`, `taux_recyclage`)
- **Data Mart Consommation** → Consommation énergétique (pour ratio CO₂/conso)
- **Base `greencity_facturation`** → Métadonnées bâtiments

### KPI à Analyser
- **Émissions totales de CO₂** : par bâtiment, par région et par période (kgCO₂)
- **Évolution des émissions dans le temps** : tendances pour identifier si pollution augmente ou diminue
- **Classement des bâtiments les plus polluants** : ranking bâtiments par émissions CO₂
- **Analyse du taux de recyclage** : taux par bâtiment/région, objectif de durabilité
- **Ratio CO₂/consommation énergétique** : indicateur d'efficacité écologique (kg CO₂ par kWh)
  - Identifie si la pollution est proportionnelle ou excessive par rapport à la consommation
- **Comparaison inter-régions** : benchmarking d'impact environnemental régional

---

## 📋 Dimensions Communes

### `dim_temps`
- **Grain**: 1 ligne par jour (2022-2026)
- **Contenu**: jour, mois, année, trimestre, jour_semaine, semaine, jour_ouvrable, jour_ferie
- **Source**: Procédure stockée `sp_generer_dim_temps()` (données de référence statiques)

### `dim_region`
- **Grain**: 1 ligne par région
- **Contenu**: 8 régions (Tanger: 4 + Tétouan: 4), code_postal, pays
- **Source**: `greencity_facturation.regions`

### `dim_batiment`
- **Grain**: 1 ligne par bâtiment
- **Contenu**: nom, surface (m²), type (Résidentiel/Commercial/Industriel/Mixte), année construction
- **Source**: `greencity_facturation.batiments`

### `dim_statut_paiement` (Conformed Dimension)
- **Grain**: 4 statuts figés
- **Contenu**: Payée | En attente | En retard | Partiel
- **Source**: Données de référence (INSERT statique)

---
