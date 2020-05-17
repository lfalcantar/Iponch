import pulp as plp
import numpy as np

## Input:
troncos = np.array([13]) # \in \R^m
piezas = np.array([5,7]) # \in \R^n
lim_inf = np.array([2,0]) # limite inferior

## Limite superior
#   Basado en total produccion de una pieza sobre todos los troncos
lim_sup = np.empty(len(piezas)) # Alocacion
for i in range(len(piezas)):
    lim_sup[i]=np.sum(troncos//piezas[i]) # Suma de cocientes

## Definicion de problema
iponch = plp.LpProblem("iponch_p",plp.LpMinimize)

## Variables
#   Suponemos que la solucion es un vector \in \R^{m x n}
#   donde 'm' es el numero de troncos y 'n' el numero de piezas
sol = {}
# rutina
for i in range(len(troncos)):
    for j in range(len(piezas)):
        sol['{},{}'.format(i,j)]= plp.LpVariable( \
        'Tronco:{},pieza:{}'.format(troncos[i],piezas[j]),\
        lowBound=0 , upBound=lim_sup[j], \
        cat='Integer')

## Definicion de problema
p = 0
for i in range(len(troncos)):
    s = 0
    for j in range(len(piezas)):
        s +=  sol['{},{}'.format(i,j)]*piezas[j]
    p += troncos[i] - s
iponch += p

## Constraints:
# Conservacion de Masa
for i in range(len(troncos)):
    c = 0
    for j in range(len(piezas)):
        c +=  sol['{},{}'.format(i,j)]*piezas[j]
    iponch += c <= troncos[i]
# Requerimiento de piezas
for i in range(len(lim_inf)):
    nn=0
    for j in range(len(troncos)):
        nn +=  sol['{},{}'.format(j,i)]
    iponch += nn >= lim_inf[i]

## OUTPUT
#print(iponch)
iponch.solve()
print('Desperdicio = ',plp.value(iponch.objective))
print('Caracterizacion: ',plp.LpStatus[iponch.status])
for variable in iponch.variables():
   print("{} = {}".format(variable.name, variable.varValue))


# cutStock.py stock=[13, 10] requiredSizes=[5,2]
#
# {
#   waste: "",
#   stockPatters:
#   [{
#     "size": "13" ,
#     "cuts": ["2","2","2","2","2","2"]
#     "waste": "1"
#     },
#   {
#     "size": "10" ,
#       "cuts": ["2","2","2","2","2"]
#     "waste": "0"
#   },
#   {
#     "size": "13" ,
#       "cuts": ["5","5", "1"]
#     "waste": "1"
#   }]
#   ...
#
# }
