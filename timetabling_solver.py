import pandas as pd
from ortools.linear_solver import pywraplp

# --- Importer les données des fichiers excels ---
# "Sample classes" contient les colonnes: subjects, students (codes des groupes d'élèves séparés par des virgules), teacher, hourly_rate
# "créneaux" contient une seule colonne: times (e.x., 'Lun_M1', 'Mar_S', etc.)

df_classes = pd.read_excel('Sample classes.xlsx')
df_slots   = pd.read_excel('créneaux.xlsx')

# Extraction des listes
C = df_classes['subjects'].tolist()
N = df_classes['hourly_rate'].astype(int).tolist()
T = df_slots['times'].tolist()

num_classes = len(C)
num_slots   = len(T)

# construction de la liste de matière par groupes d'élèves et professeurs avec leurs indices
# élèves 
all_groups = set(
    g.strip() for grp_list in df_classes['students']
    for g in grp_list.split(',')
)
indices_group = {
    grp: [i for i, grp_list in enumerate(df_classes['students'])
          if grp in [g.strip() for g in grp_list.split(',')]]
    for grp in sorted(all_groups)
}

# professeurs
all_teachers = df_classes['teacher'].unique().tolist()
indices_teacher = {
    teacher: [i for i, t in enumerate(df_classes['teacher']) if t == teacher]
    for teacher in all_teachers
}

# --- Création du solveur ---
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    raise Exception("Solver not created.")

# Variables de décision: x[i,j]=1 si le cours i a lieu au créneau j
x = {}
for i in range(num_classes):
    for j in range(num_slots):
        x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

# nombre de salle de classe utilisé par créneau 
loads = [solver.Sum(x[i, j] for i in range(num_classes))
         for j in range(num_slots)]
max_load = solver.NumVar(0, num_classes, 'max_load')

# Constrainte 1: chaque matière doit être enseignée le nombre d'heures hebdomadaire spécifié
for i in range(num_classes):
    solver.Add(solver.Sum(x[i, j] for j in range(num_slots)) == N[i])

# Constrainte 2: par groupe d'élèves, chaque créneau horaire ne peut être occupé que par une seule matière
for j in range(num_slots):
    for grp, idxs in indices_group.items():
        solver.Add(solver.Sum(x[i, j] for i in idxs) <= 1)

# Constrainte 3: par professeur, chaque créneau horaire ne peut être occupé que par une seule matière
for j in range(num_slots):
    for teacher, idxs in indices_teacher.items():
        solver.Add(solver.Sum(x[i, j] for i in idxs) <= 1)

# Constrainte 4: nombre de classes utilisé par créneau ≤ max_load
for load in loads:
    solver.Add(load <= max_load)

# Objectif: minimiser le nombre maximum de classes par créneau
solver.Minimize(max_load)

# Résoudre
status = solver.Solve()

# Sortie
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print('Solution trouvé:')
    print(f'Nombre de salle de classe nécessaire = {solver.Objective().Value()}')
    for j in range(num_slots):
        for i in range(num_classes):
            if x[i, j].solution_value() > 0.5:
                print(f'Créneau {T[j]}: {C[i]} (Professeur: {df_classes.at[i, "teacher"]}, Elèves: {df_classes.at[i, "students"]})')
else:
    print('Aucune solution trouvée.')
    if status == pywraplp.Solver.INFEASIBLE:
        print('Le Problème est infaisable.')
    elif status == pywraplp.Solver.UNBOUNDED:
        print('Le Problème est non borné.')
    else:
        print('Solver status:', status)
