from distutils import command
from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from scipy.stats import norm
import math
import matplotlib.pyplot as plt




root = Tk()
root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Excel Files","*.xlsx"),("all files","*.*")))


file = root.filename
df = pd.read_excel(file, index_col=0)
my_array = []
#Copy to array
for index, row in df.iterrows():
    my_array.append([row[0], row[1]])

my_array = my_array[2:]
#Ascending Sort
for x in range(len(my_array)):
    for y in range(len(my_array)):
        if my_array[x][1] < my_array[y][1]:
            pom = my_array[x]
            my_array[x] = my_array[y]
            my_array[y] = pom

#Reverse Rank
for x in range(len(my_array)):
    my_array[x].insert(2, 196 - x)

#Numbers
for x in range(len(my_array)):
    my_array[x].insert(3, x + 1)


#Copy to new array
new_array = []
i = 0
for x in range(len(my_array)):
    if my_array[x][0] =='F':
        new_array.append(my_array[x])
        i = i + 1

#Estimate of CDF
new_array[0].insert(4, 1 *new_array[0][2]/(new_array[0][2]+1))

for x in range(1, len(new_array)):
    new_array[x].insert(4, (new_array[x-1][4] * new_array[x][2])/(new_array[x][2]+1))

#Estimate of CDF(1 - S)
for x in range(len(new_array)):
    new_array[x].insert(5, 1 - new_array[x][4])
#Probit
for x in range(len(new_array)):
    new_array[x].insert(6, norm.ppf(new_array[x][5]))
#LN
for x in range(len(new_array)):
    new_array[x].insert(7, math.log(new_array[x][1]))


#XY
for x in range(len(new_array)):
    new_array[x].insert(8, new_array[x][6] * new_array[x][7])
#X^2
for x in range(len(new_array)):
    new_array[x].insert(9, new_array[x][7] * new_array[x][7])
#Sum X
sum_X = 0
for x in range(len(new_array)):
    sum_X = sum_X + new_array[x][7]
#Sum Y
sum_Y = 0
for x in range(len(new_array)):
    sum_Y = sum_Y + new_array[x][6]
#Sum XY
sum_XY = 0
for x in range(len(new_array)):
    sum_XY = sum_XY + new_array[x][8]
#Sum X^2
sum_XX = 0
for x in range(len(new_array)):
    sum_XX = sum_XX + new_array[x][9]
#N
N = len(new_array)
#a
a = (N * sum_XY - sum_X * sum_Y) / (N * sum_XX - sum_X * sum_X)
#b
b = (sum_Y - a * sum_X) / N
#Lambda
lam = b/a
#Ksi
ksi = 1/a
#New y Values
for x in range(len(new_array)):
    new_array[x].insert(10, a * new_array[x][7] + b)
y_values_new = []
for y in range(len(new_array)):
    y_values_new.append(new_array[y][10])
#Chart of Lognorm
x_values = []
for x in range(len(new_array)):
    x_values.append(new_array[x][7])
y_values = []
for y in range(len(new_array)):
    y_values.append(new_array[y][6])
plt.scatter(x_values, y_values)
plt.plot(x_values, y_values_new)
plt.xlabel('Elapsed time log(days')
plt.ylabel('Probit(1-Surv)')
plt.title('Lognormal\n')

plt.text(8.2, -1.1, 'a = ')
plt.text(8.3, -1.1, a)

plt.text(8.2, -1.2, 'b = ')
plt.text(8.3, -1.2, b)

plt.text(8.2, -1.3, 'Lambda = ')
plt.text(8.45, -1.3, lam)

plt.text(8.2, -1.4, 'Ksi = ')
plt.text(8.35, -1.4, ksi)
plt.show()



#Life table
sec_array = []
int_endpoint = []
for index, row in df.iterrows():
    sec_array.append([row[0], row[1]])

sec_array = sec_array[2:]
#Ascending Sort
for x in range(len(sec_array)):
    for y in range(len(sec_array)):
        if sec_array[x][1] < sec_array[y][1]:
            pom = sec_array[x]
            sec_array[x] = sec_array[y]
            sec_array[y] = pom
#Make second table
i = 0
for x in range(9):
    int_endpoint.append(i)
    i = i + 2000
#n
n = 0
counter = 0
n_array = []
n_array.append(0)
for x in range(1,len(int_endpoint)):
    for y in range(len(sec_array)):
        if sec_array[y][1] > n:
            counter = counter + 1
    n_array.append(counter)
    counter = 0
    n = n + 2000
#d
d = 0
n = 0
counter = 0
d_array = []
d_array.append(0)
for x in range(1,len(int_endpoint)):
    for y in range(len(sec_array)):
        if sec_array[y][1] > n and sec_array[y][1] < n + 2000 and sec_array[y][0] == 'F':
            counter = counter + 1
            
    d_array.append(counter)
    n = n + 2000
    counter = 0

#w
w = 0
n = 0
counter = 0
w_array = []
w_array.append(0)
for x in range(1,len(int_endpoint)):
    for y in range(len(sec_array)):
        if sec_array[y][1] > n and sec_array[y][1] < n + 2000 and sec_array[y][0] == 'S':
            counter = counter + 1
            
    w_array.append(counter)
    n = n + 2000
    counter = 0

#Survival
survival = []
survival.append(1.0)
for x in range(1, len(int_endpoint)):
    survival.append(survival[x-1] * (1 - d_array[x] / (n_array[x] - w_array[x] / 2)))  

#Interval midpoint
int_midpoint = []
for x in range(len(int_endpoint) - 1):
    int_midpoint.append((int_endpoint[x] + int_endpoint[x + 1]) / 2)

#Hazard
hazard = []
hazard.append(0)
for x in range(1, len(int_endpoint) - 1):
    hazard.append(survival[x + 1] * d_array[x + 1] / ((n_array[x + 1] - 0.5 * w_array[x + 1]) * 2000))

#Chart of Lifetable

survival.pop() #usuniete aby byla mozliwosc zrobienia wykresu
plt.plot(int_midpoint, survival)
plt.xlabel('Days elapsed')
plt.ylabel('Survival Distribution Function')
plt.ylim(0,1.2)
plt.xlim(0, 20000)
plt.title('Life Table')
plt.show()

plt.plot(int_midpoint, hazard)
plt.xlabel('Days elapsed')
plt.ylabel('Hazard Function')
plt.title('Life Table')
plt.show()