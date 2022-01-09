#!/usr/bin/python
# coding: utf-8

import sys, time
from mip import *

def parser(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        n, c1, c2, center = lines[0].split()
        pred = []
        dist = []
        profit = []
        w1 = []
        w2 = []
        for line in lines[1:-3]:
            pred.append(int(line.split()[0]))
            dist.append(float(line.split()[1]))
            profit.append(float(line.split()[2]))
            w1.append(float(line.split()[3]))
            w2.append(float(line.split()[4]))
        return int(n), float(c1), float(c2), int(center), pred, dist, profit, w1, w2


# Vérificaion du nombre d'arguments du programme.
# Le premier argument (d'indice 0) est toujours le nom du programme
# Ici, il faut trois arguments :
# - le nom du programme (d'extension .py)
# - le nom du fichier de données
# - le nom du répertoire d esauvegarde des solutions.
if len(sys.argv) < 3:
    print("Nombre d'arguments insuffisants")
    print("usage : python model_1.py nom_fichier_data nom_rep_solution")
    sys.exit()

# Récupération du nom du fichier de donnée corespondant au deuxième argument
datafileName = sys.argv[1]

n, c1, c2, center, pred, dist, profit, w1, w2 = parser(datafileName)

model_1 = Model(name='AEPMCC_cf', solver_name="CBC")

x = [model_1.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n+1)]
r = model_1.add_var(name="r", var_type=CONTINUOUS)

model_1.objective = maximize(xsum(profit[i] * x[i] for i in range(n)) - r)

model_1.add_constr(xsum(w1[i] * x[i] for i in range(n)) <= c1, name="c1")
model_1.add_constr(xsum(w2[i] * x[i] for i in range(n)) <= c2, name="c2")

for i in range(n):
    if i != center:
        model_1.add_constr(x[i] <= x[pred[i]], name="c3_%s" % i)

for i in range(n):
    model_1.add_constr(x[i]*dist[i] <= r, name="c4_%s" % i)

model_1.add_constr(x[center] == 1, name="c5")

model_1.add_constr(x[-1] == 0, name="c6")


start = time.perf_counter()
status = model_1.optimize(max_seconds=120)
runtime = time.perf_counter() - start


#datafileName = 'Instances/btk_1-Reichstett_0_0.dat'
datafileNameSplit = datafileName.split('/')
instanceName = datafileNameSplit[len(datafileNameSplit)-1]
solutionfileName = sys.argv[2]+"/"+instanceName+".sol"

with open(solutionfileName, 'w') as file:  #ouvre le fichier, le ferme automatiquement à la fin et gère les exceptions
    if status == OptimizationStatus.OPTIMAL:
        file.write("Status de la résolution: OPTIMAL")
    elif status == OptimizationStatus.FEASIBLE:
        file.write("Status de la résolution: TEMPS LIMITE et SOLUTION REALISABLE CALCULEE")
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        file.write("Status de la résolution: TEMPS LIMITE et AUCUNE SOLUTION CALCULEE")
    elif status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE:
        file.write("Status de la résolution: IRREALISABLE")
    elif status == OptimizationStatus.UNBOUNDED:
        file.write("Status de la résolution: NON BORNE")

    file.write("\nTemps de résolution (s) : " + str(round(runtime,3))+"\n")
    file.write("----------------------------------\n")

    # Si le modèle a été résolu à l'optimalité ou si une solution a été trouvée dans le temps limite accordé
    if model_1.num_solutions>0:
        file.write("Bilan; " + instanceName + "; " + str(round(runtime,3)) + "; " + str(status) + "; " + str(model_1.objective_value) +"\n")
    else:
        file.write("Bilan; " + instanceName + "; " + str(round(runtime,3)) + "; " + str(status) + "; Aucune solution retournée\n")
