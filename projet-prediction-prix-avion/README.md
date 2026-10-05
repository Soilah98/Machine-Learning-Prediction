# Prédiction du Prix des Billets d'Avion — Pipeline ML Complet

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Status](https://img.shields.io/badge/Status-Terminé-green)


> **Un modèle Random Forest déployé en application Streamlit pour estimer le prix d'un billet d'avion à partir de ses caractéristiques : compagnie, trajet, classe, escales, délai de réservation.**

---

##  Problème business

Le prix d'un billet d'avion varie fortement selon la compagnie, le trajet, la classe, le nombre d'escales et le délai entre la réservation et le vol. Ce projet construit un modèle prédictif capable d'estimer le prix d'un billet à partir de ces caractéristiques, et le déploie sous forme d'application interactive.

---

##  Dataset

- **Source** : [Flight Price Prediction — Kaggle](https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction)
- **Collecte** : Scraping du site EaseMyTrip sur 50 jours (février–mars 2022)
- **Volume** : 300 261 réservations de vols entre les grandes villes indiennes
- **Classes** : Économique et Affaires
- **Variables clés** : compagnie aérienne, ville de départ/arrivée, heure de départ/arrivée, nombre d'escales, durée du vol, jours avant le vol, prix (cible)

---

##  Méthodologie

### 1. Analyse exploratoire (EDA)
- Classification des variables (discrètes / continues)
- Analyse univariée : distributions, asymétries, valeurs extrêmes
- Analyse multivariée : relations entre le prix et chaque variable

### 2. Tests statistiques
| Hypothèse testée | Test utilisé | Résultat |
|---|---|---|
| Durée du vol influence le prix | Test de Pearson |  Corrélation significative |
| La compagnie influence le prix | ANOVA / Kruskal-Wallis |  Différences significatives |
| Le nombre d'escales influence le prix | Test d'Anava |  Impact confirmé |
|Le délai de réservation influence le prix | Test de Pearson|  Correlation significative |

### 3. Preprocessing
- Encodage des variables catégorielles (OneHotEncoder)
- Standardisation des variables numériques (StandardScaler)
- Pipeline Scikit-learn pour éviter tout data leakage

### 4. Modélisation — comparaison de modèles

| Modèle | MAE (CV) | Notes |
|---|---|---|
| DummyRegressor (baseline) | Élevée | Référence |
| Régression Linéaire | Moyenne | Limite non-linéarité |
| Ridge (α=0.1, 1, 20) | Similaire à LinReg | Régularisation peu impactante |
| **Random Forest** ✅ | **Meilleure** | Capture les interactions non-linéaires |

### 5. Modèle final — Random Forest
- `n_estimators = 100`, `random_state = 42`
- Entraîné sur l'ensemble du train set
- Intervalle de confiance à 95% calculé sur la MAE test

### 6. Export & Déploiement
- Modèle exporté en `.joblib` avec métadonnées JSON
- Application interactive déployée avec **Streamlit**

---

##  Structure du projet

```
├── README.md
├── Dockerfile
├── docker-compose.yml
├── artifacts/
│   ├── flight_price_model.joblib       # Modèle entraîné
│   └── flight_price_model.meta.json    # Métadonnées du modèle
├── data/
│   └── Clean_Dataset.csv               # Dataset source
├── deploiement/
│   └── dashboard_streamlit.py          # Application Streamlit
├── notebooks/
│   └── flight.ipynb                    # Notebook d'analyse complet
├── src/
│   └── visualisation.py                # Fonctions de visualisation
├── tests/
│   └── __init__.py
├── requirements.txt
└── pyproject.toml
```

---

##  Stack technique

- **Python** · Pandas · NumPy · Scipy
- **Scikit-learn** : Pipeline, RandomForestRegressor, Ridge, OneHotEncoder, StandardScaler
- **Streamlit** : déploiement de l'application interactive
- **Joblib** : sérialisation du modèle
- **Matplotlib / Seaborn** : visualisation
- **Docker**
- HTML + CSS

---

##  Installation & Utilisation

```bash
# Cloner le repository
git clone https://github.com/Soilah98/Machine-learning.git
cd prediction-prix-avion

# Installer les dépendances
pip install -r requirements.txt

# Lancer le notebook d'analyse
jupyter notebook notebooks/flight.ipynb

# Lancer l'application Streamlit
streamlit run deploiement/dashboard_streamlit.py
```

---

##  Insights clés

- ✅ **La classe (Économique vs Affaires)** est le facteur le plus discriminant sur le prix
- ✅ **Réserver tôt** est associé à des prix plus bas — la relation est non-linéaire
- ✅ **Vistara et Air India** affichent des prix systématiquement plus élevés que les autres compagnies
- ✅ **Le Random Forest** surpasse largement la régression linéaire grâce à la capture des interactions entre variables
- ✅ **Pipeline Scikit-learn** garantit l'absence de data leakage entre train et test

---

##  Ce qui différencie ce projet

Ce projet couvre **l'intégralité du cycle ML** :
- De l'exploration statistique rigoureuse (tests d'hypothèses)
- À la comparaison de modèles avec validation croisée
- Jusqu'au déploiement en application interactive Streamlit

Le modèle est exporté, versionné et utilisable directement via `.predict()`.

---

## Auteur

**Ibrahim Soilah** · [GitHub](https://github.com/Soilah98) · [LinkedIn](https://www.linkedin.com/in/soilah-5a166225b/) · [Malt](https://www.malt.fr/profile/ibrahimsoilahoudine)
