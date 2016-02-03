import numpy as np
import parse_data as par
import load_data as ld
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import cross_validation
from sklearn.svm import SVR
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor


def get_data(data, data_name):
    dfDict = par.parse_data(data)
    X = dfDict[data_name][:,0:-1]
    Y = dfDict[data_name][:,-1]
    return X, Y


def lasso_reg(X,Y):
    model = linear_model.Lasso(alpha = 0.1).fit(X,Y)
    scores = cross_validation.cross_val_score(
        model, X, Y, cv=10, scoring = 'mean_absolute_error')
    mean_abs_err = np.abs(np.mean(scores))
    print('Done Lasso. Mean absolute error: ', mean_abs_err)
    return model, mean_abs_err


def svr_rbf(X,Y):
    model = SVR(C=1.0,kernel='rbf').fit(X,Y)
    scores = cross_validation.cross_val_score(
        model, X, Y, cv=10, scoring = 'mean_absolute_error')
    mean_abs_err = np.abs(np.mean(scores))
    print('Done SVR-RBF. Mean absolute error: ', mean_abs_err)
    return model, mean_abs_err


def svr_lin(X,Y):
    model = SVR(C=1.0,kernel='linear').fit(X,Y)
    scores = cross_validation.cross_val_score(
        model, X, Y, cv=10, scoring = 'mean_absolute_error')
    mean_abs_err = np.abs(np.mean(scores))
    print('Done SVR-LIN. Mean absolute error: ', mean_abs_err)
    return model, mean_abs_err


def reg_tree(X,Y):
    model  = tree.DecisionTreeRegressor().fit(X,Y)
    scores = cross_validation.cross_val_score(
        model, X, Y, cv=10, scoring = 'mean_absolute_error')
    mean_abs_err = np.abs(np.mean(scores))
    print('Done Regression Tree. Mean absolute error: ', mean_abs_err)
    return model, mean_abs_err


def reg_rand_forest(X,Y):
    model  = RandomForestRegressor(n_estimators=100).fit(X,Y)
    scores = cross_validation.cross_val_score(
        model, X, Y, cv=10, scoring = 'mean_absolute_error')
    mean_abs_err = np.abs(np.mean(scores))
    print('Done Random Forest. Mean absolute error: ', mean_abs_err)
    return model, mean_abs_err


def reg_boost(X,Y):
    model  = GradientBoostingRegressor(n_estimators=100).fit(X,Y)
    scores = cross_validation.cross_val_score(
        model, X, Y, cv=10, scoring = 'mean_absolute_error')
    mean_abs_err = np.abs(np.mean(scores))
    print('Done Boosting. Mean absolute error: ', mean_abs_err)
    return model, mean_abs_err


if __name__ == "__main__":
    sqlfilename = input("Type sql script filename: ")
    data = ld.load_data(sqlfilename)
    data_name = input("Which data set do you want? (CT, MD, DOSE, PRES, PHYS): ")
    X,Y = get_data(data, data_name)
    lasso_reg(X,Y)
    svr_rbf(X,Y)
    svr_lin(X,Y)
    reg_tree(X,Y)
    reg_rand_forest(X,Y)
    reg_boost(X,Y)

