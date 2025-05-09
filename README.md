# Emploi du temps automatique avec OR-Tools

## Description
Ce projet permet de générer automatiquement un emploi du temps équilibré pour un ensemble de matières, de groupes d'élèves et de professeurs, en minimisant le nombre de cours simultanés par créneau (charge maximale). Le solveur est implémenté en Python avec la bibliothèque OR-Tools de Google, et les données d'entrée sont lues depuis deux fichiers Excel.

## Prérequis
- Python 3.8 ou supérieur
- Un environnement virtuel (recommandé) : `venv`, `conda` ou autre
- Les bibliothèques Python suivantes :
  - `ortools`
  - `pandas`
  - `openpyxl`

## Installation
1. Clonez ce dépôt :
   ```bash
   git clone https://votre-repo.git
   cd votre-repo

2. Créez et activez un environnement virtuel :

   ```bash
   python -m venv .venv       # ou conda create -n edt python=3.x
   source .venv/bin/activate  # sous Windows : .venv\\Scripts\\activate
   ```
3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Préparez vos fichiers Excel :

   * **Sample classes.xlsx** : colonnes `subjects`, `students`, `teacher`, `hourly_rate`
   * **créneaux.xlsx** : colonne `times` (ex. `Lun_M1`, `Mar_S`, etc.)
2. Adaptez le chemin vers les fichiers Excel dans le script `timetabling_solver.py` si nécessaire.
3. Lancez le script :

   ```bash
   python timetabling_solver.py
   ```
4. Le programme affichera la répartition des matières par créneau et la charge maximale atteinte.

## Structure du projet

```text
votre-repo/
├── timetabling_solver.py   # Script principal
├── Sample classes.xlsx     # Données matières et professeurs
├── créneaux.xlsx           # Liste des créneaux horaires
├── requirements.txt        # Dépendances Python
└── README.md               # Document d'information du projet
```

## Contribuer

Les contributions sont les bienvenues (pour la prise en compte de contraintes plus poussées par exemple ^_~):

1. Forkez le dépôt
2. Créez une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commitez vos modifications (`git commit -m 'Ajout d'une fonction X'`)
4. Poussez la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

```
```
