import pulp as plp
import numpy as np

## Input:
troncos = np.array([100,13,17,22]) # \in \R^m
piezas = np.array([7,5,3,2]) # \in \R^n
lim_inf = np.array([7,4,1,2]) # limite inferior

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
        'Tronco:{}, pieza:{}'.format(troncos[i],piezas[j]),\
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

## Constraint: Conservacion de Masa
for i in range(len(troncos)):
    c = 0
    for j in range(len(piezas)):
        c +=  sol['{},{}'.format(i,j)]*piezas[j]
    iponch += c <= troncos[i]


for i in range(len(lim_inf)):
    nn=0
    for j in range(len(troncos)):
        nn +=  sol['{},{}'.format(j,i)]
    print(nn,lim_inf[i])
    iponch += nn >= lim_inf[i]

#print(iponch)
#Reporte
status=iponch.solve()
print(plp.value(iponch.objective))
print('Criteria',plp.LpStatus[iponch.status])
for variable in iponch.variables():
   print("{} = {}".format(variable.name, variable.varValue))

# x = plp.LpVariable('x', lowBound=0 , cat='Integer')
# y = plp.LpVariable('y', lowBound=0 , cat='Integer')

# # Waste Function
# iponch += 4*x + 3*y , "W"
#
# # Constraints
# iponch += 2*y <= 25 - x
# iponch += 4*y >= 2*x - 8
# iponch += y <= 2*x - 5

#status=iponch.solve()
#print(plp.value(iponch.objective))
#print('Criteria',plp.LpStatus[iponch.status])

#for variable in iponch.variables():
#    print("{} = {}".format(variable.name, variable.varValue))


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
