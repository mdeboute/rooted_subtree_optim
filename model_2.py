#!/usr/bin/python
# coding: utf-8

import sys, time
from mip import *
from model_1 import parser

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

x_sorted = [i for i in range(n)]
dist_sorted = dist.copy()

for i in range(n):
    min = i
    for j in range(i, n):
        if(dist_sorted[j] < dist_sorted[min]):
            min = j
    if(min != i):
        temp = dist_sorted[i]
        dist_sorted[i] = dist_sorted[min]
        dist_sorted[min] = temp
        temp = x_sorted[i]
        x_sorted[i] = x_sorted[min]
        x_sorted[min] = temp

def sigma(i):
    for k in range(n):
        if(x_sorted[k] == i):
            return k

def sigma_inv(k):
    return x_sorted[k]

def delta(i):
    if i == center:
        return 0
    return dist[i] - dist[sigma_inv(sigma(i)-1)]

model_2 = Model(name='AEPMCC_cf', solver_name="CBC")

x = [model_2.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n+1)]
y = [model_2.add_var(name="y_%s" % i, var_type=BINARY) for i in range(n)]

model_2.objective = maximize(xsum(profit[i] * x[i] - y[i] * delta(i) for i in range(n)))

model_2.add_constr(xsum(w1[i] * x[i] for i in range(n)) <= c1, name="c1")
model_2.add_constr(xsum(w2[i] * x[i] for i in range(n)) <= c2, name="c2")

for i in range(n):
    if i != center:
        model_2.add_constr(x[i] <= x[pred[i]], name="c3_%s" % i)

model_2.add_constr(x[center] == 1, name="c4")

for i in range(n):
    model_2.add_constr(xsum(x[sigma_inv(k)] for k in range(i, n)) <= y[sigma_inv(i)]*(n-i), name="c5_%s" % i)

model_2.add_constr(x[-1] == 0, name="c6")

start = time.perf_counter()
status = model_2.optimize(max_seconds=120)
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
    if model_2.num_solutions>0:
        file.write("Bilan; " + instanceName + "; " + str(round(runtime,3)) + "; " + str(status) + "; " + str(model_2.objective_value) +"\n")
    else:
        file.write("Bilan; " + instanceName + "; " + str(round(runtime,3)) + "; " + str(status) + "; Aucune solution retournée\n")
