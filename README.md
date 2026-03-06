# Mini-Projet IA : Planification Robuste avec A* et Chaînes de Markov

Projet réalisé dans le cadre du cours d'Intelligence Artificielle - SDIA

## 📋 Description

Ce projet implémente et compare différents algorithmes de planification de chemins (A*, UCS, Greedy) et analyse leur robustesse face à l'incertitude en utilisant les chaînes de Markov. Le projet explore comment un agent peut naviguer dans un environnement avec des obstacles tout en gérant l'incertitude dans l'exécution de ses actions.

## 🎯 Objectifs

1. **Planification de chemins** : Implémentation et comparaison de plusieurs algorithmes de recherche
2. **Modélisation stochastique** : Utilisation des chaînes de Markov pour modéliser l'incertitude
3. **Analyse de robustesse** : Évaluation de la probabilité d'atteinte du but selon différents niveaux d'incertitude
4. **Visualisation** : Génération de graphiques et heatmaps pour analyser les résultats

## 🚀 Algorithmes Implémentés

### Algorithmes de Planification
- **UCS (Uniform Cost Search)** : Recherche à coût uniforme
- **Greedy Best-First Search** : Recherche gloutonne guidée par heuristique
- **A\*** : Recherche optimale combinant coût et heuristique
- **Weighted A\*** : Variante de A* avec pondération de l'heuristique

### Heuristiques
- **Manhattan** : Distance de Manhattan (admissible)
- **Euclidienne** : Distance euclidienne (admissible)
- **h=0** : Équivalent à UCS
- **Weighted** : Heuristique pondérée (non-admissible)

### Analyse Stochastique
- **Chaînes de Markov** : Modélisation de l'incertitude dans l'exécution
- **Analyse d'absorption** : Calcul des probabilités d'atteinte du but
- **Simulation Monte-Carlo** : Validation empirique des résultats théoriques

## 📁 Structure du Projet

```
.
├── astar.py                    # Implémentation des algorithmes de recherche
├── markov.py                   # Chaînes de Markov et analyse stochastique
├── experiments.py              # Expériences et visualisations principales
├── generate_figures.py         # Génération de figures haute résolution individuelles
├── .gitignore                  # Fichiers à ignorer par Git
└── README.md                   # Ce fichier
```

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip

### Dépendances

```bash
pip install numpy matplotlib
```

## 💻 Utilisation

### Exécuter toutes les expériences

```bash
python experiments.py
```

Cette commande génère :
- `exp1_grilles.png` : Comparaison visuelle des algorithmes sur 3 grilles
- `exp1_metriques.png` : Métriques de performance (nœuds, coût, temps)
- `exp2_epsilon.png` : Impact du paramètre d'incertitude ε
- `exp3_heuristics.png` : Comparaison des différentes heuristiques
- `exp4_absorption.png` : Heatmaps d'analyse d'absorption

### Générer des figures haute résolution

```bash
python generate_figures.py
```

Génère des figures individuelles en haute résolution (200 DPI) dans le dossier `figures/`.

### Utiliser les modules individuellement

```python
from astar import astar, make_grid
from markov import build_policy, monte_carlo

# Créer une grille
obstacles = [(2,2), (2,3), (3,2)]
grid = make_grid(5, 5, obstacles)

# Trouver un chemin avec A*
result = astar(grid, start=(0,0), goal=(4,4))
print(f"Chemin trouvé : {result['path']}")
print(f"Coût : {result['cost']}")

# Analyser avec Markov
policy = build_policy(result['path'])
mc_result = monte_carlo(grid, free_cells, state_index, policy, goal, epsilon=0.1)
print(f"P(atteindre le but) : {mc_result['p_goal']}")
```

## 📊 Expériences

### Expérience 1 : Comparaison des Algorithmes
Compare UCS, Greedy et A* sur 3 grilles de difficulté croissante :
- **Facile** : Zigzag 8×8
- **Moyen** : Labyrinthe 12×12
- **Difficile** : Serpentin 15×15

**Métriques** : Nombre de nœuds développés, coût du chemin, temps d'exécution

### Expérience 2 : Impact de l'Incertitude (ε)
Analyse l'effet du paramètre d'incertitude ε sur :
- La probabilité d'atteindre le but
- Le temps moyen d'atteinte
- La probabilité d'échec

**Valeurs testées** : ε ∈ {0.0, 0.1, 0.2, 0.3}

### Expérience 3 : Comparaison des Heuristiques
Évalue les performances de différentes heuristiques :
- Nombre de nœuds développés
- Optimalité du chemin trouvé
- Temps d'exécution

### Expérience 4 : Analyse d'Absorption
Visualise pour chaque état :
- La probabilité d'atteindre le but
- Le temps moyen avant absorption
- Les zones critiques de l'environnement

## 🎨 Visualisations

Le projet génère des visualisations stylisées avec :
- Grilles colorées avec obstacles et chemins
- Graphiques de métriques comparatives
- Trajectoires Monte-Carlo
- Heatmaps de probabilités

**Palette de couleurs** :
- 🟢 Départ (vert)
- 🔴 But (rose)
- ⚫ Obstacles (gris foncé)
- 🔵 Chemin planifié (dégradé bleu-violet-rose)

## 📈 Résultats Clés

- **A\* est optimal** : Trouve toujours le chemin de coût minimal
- **Greedy est rapide** : Développe moins de nœuds mais peut être sous-optimal
- **L'incertitude dégrade les performances** : P(but) diminue avec ε
- **Manhattan est efficace** : Bon compromis entre optimalité et vitesse

## 🔬 Méthodologie

1. **Planification** : Calcul du chemin optimal avec A*
2. **Modélisation** : Construction de la matrice de transition avec incertitude
3. **Analyse théorique** : Calcul matriciel des probabilités d'absorption
4. **Validation empirique** : Simulation Monte-Carlo (N=3000)
5. **Visualisation** : Génération de graphiques et heatmaps

## 📝 Notes Techniques

- Les grilles utilisent une représentation matricielle (0=libre, 1=obstacle)
- Les positions sont en format (ligne, colonne)
- Les actions sont : haut, bas, gauche, droite
- L'incertitude ε représente la probabilité de dévier perpendiculairement

## ⚙️ Configuration Git

Le projet inclut un `.gitignore` qui exclut automatiquement :
- `__pycache__/` et fichiers bytecode Python
- Environnements virtuels
- Fichiers IDE
- Figures générées (outputs)
- Fichiers système

## � Dépannage

### Erreur de chemin sous Windows
Si vous rencontrez des erreurs de type `FileNotFoundError`, assurez-vous que les chemins dans les scripts utilisent des chemins relatifs (déjà corrigé dans la version actuelle).

### Problèmes d'affichage des graphiques
Si les graphiques ne s'affichent pas correctement :
```bash
pip install --upgrade matplotlib
```

### Performance lente
Pour les simulations Monte-Carlo, réduire `n_sim` dans `experiments.py` :
```python
exp2_epsilon('medium', n_sim=1000)  # Au lieu de 3000
```

## 🤝 Auteur

**Farahi Abderahim** - SDIA

## 📄 Licence

Ce projet est réalisé dans un cadre académique.
