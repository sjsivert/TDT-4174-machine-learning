

from joblib import dump, load
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn import tree
from sklearn.metrics import explained_variance_score

scaler = load('../models/datascaler.joblib')
X_training = pd.read_csv('../data/x_training').iloc[:, 1:]
Y_training = pd.read_csv('../data/y_training')

#df = pd.read_csv('../data/processed_removed_outliers_normalized.csv')
#df = df.iloc[:,1:]
x_varLog = []
y_varLog = []
min = Y_training.min(axis=0)['price']
max = Y_training.max(axis=0)['price']
#scaler = StandardScaler()
#Y_training = pd.DataFrame(scaler.fit_transform(Y_training), columns=Y_training.columns)
for i in range(len(X_training)):
    tempList = []
    y_varLog.append((Y_training['price'][i] - min) / (max - min))
    for e in X_training.keys():
        tempList.append(X_training[e][i])
    tempList.append(1)
    x_varLog.append(tempList)


f = open("../models/logistic.txt", 'r')
thetaLog = []
for i in f.readline().split(','):
    thetaLog.append(float(i))
f.close()


def logisticProduct(x_i, theta):
    sum = 0
    for j in range(len(x_i)):
        sum += x_i[j] * theta[j]
    return (1 / (1 + (2.7183**-sum)))


def vectorLength(v):
    sum = 0
    for i in v:
        sum += i ** 2
    return sum ** 0.5


def grafdientDecentLog(thet, y, x, alpha, error, it):

    gradient = [0] * len(x[0])
    for j in range(len(x[0])):
        for i in range(len(x)):
            gradient[j] += (y[i] - logisticProduct(x[i], thet)) * x[i][j]
    for j in range(len(x[0])):
        thet[j] += (alpha * gradient[j])
    if vectorLength(gradient) > error:
        it = it+1
        print('Gradient length:', vectorLength(gradient), '\n   ' + 'Iterations:',it)
        return grafdientDecentLog(thet, y, x, alpha, error, it)
    else:
        print('\n' + 'Total iterations:',it, '\n')
        return thet


thetaLog = grafdientDecentLog(thetaLog, y_varLog, x_varLog, 0.00004, 1, 0)


thetaString = str(thetaLog[0])
for i in range(1, len(thetaLog)):
    thetaString += ","+str(thetaLog[i])

f = open("../models/logistic.txt", 'w')

f.write(thetaString)
f.close()

thetaLog.sort()

i = 0
print('Name                          Normalized Theta     Scaled up theta')
for key in X_training.keys():
    name = key
    theta  = round(thetaLog[i], 6)
    thetaScaled  = round((thetaLog[i] * (max - min) + min), 6)

    decimalPointAligner1 = ''
    if len(str(round(theta, 5))) != len(str(theta)):
        decimalPointAligner1 = ' '
    decimalPointAligner2 = (1 - len(decimalPointAligner1)) * ' '
    if len(str(round(thetaScaled, 5))) != len(str(thetaScaled)):
        decimalPointAligner2 += ' '

    nameSpace = (15 - len(name)) * ' '
    thetaSpace = (20 - len(str(theta))) * ' '
    thetaScaledSpace = (20 - len(str(thetaScaled))) * ' '

    print(name +  nameSpace, decimalPointAligner1, thetaSpace, theta, decimalPointAligner2 ,  thetaScaledSpace, thetaScaled)
    i+=1