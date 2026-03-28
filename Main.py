import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_selection import SelectKBest, chi2
#=================flask code starts here
from flask import Flask, render_template, request, redirect, url_for, session,send_from_directory
import pymysql

app = Flask(__name__)
app.secret_key = 'welcome'

dataset = pd.read_csv("Dataset/RT_IOT2022.csv")
labels = np.unique(dataset['Attack_type'])
label_encoder = []
columns = dataset.columns
types = dataset.dtypes.values
for j in range(len(types)):
    name = types[j]
    if name == 'object': #finding column with object type
        le = LabelEncoder()
        dataset[columns[j]] = pd.Series(le.fit_transform(dataset[columns[j]].astype(str)))#encode all str columns to numeric
        label_encoder.append([columns[j], le])
dataset.fillna(dataset.mean(), inplace = True)
Y = dataset['Attack_type'].ravel()
Y = Y.astype('int')
dataset.drop(['no', 'Attack_type'], axis = 1,inplace=True)
X = dataset.values
scaler = MinMaxScaler(feature_range = (0, 1))
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
data = np.load("model/data.npy", allow_pickle=True)
X_train, X_test, y_train, y_test = data
selector = SelectKBest(score_func=chi2, k=45) 
X_train = selector.fit_transform(X_train, y_train)
X_test = selector.transform(X_test)
ada = AdaBoostClassifier()
er = ExtraTreesClassifier(n_estimators=100, criterion='gini', max_depth=50, random_state=42)
estimators = [('ert', er), ('ada', ada)]
hybrid_model = VotingClassifier(estimators = estimators, voting='soft')
hybrid_model.fit(X_train, y_train)

@app.route('/Predict', methods=['GET', 'POST'])
def predictView():
    return render_template('Predict.html', msg='')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')

@app.route('/UserLogin', methods=['GET', 'POST'])
def UserLogin():
    return render_template('UserLogin.html', msg='')

@app.route('/UserLoginAction', methods=['GET', 'POST'])
def UserLoginAction():
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        if user == "admin" and password == "admin":
            return render_template('UserScreen.html', msg="<font size=3 color=blue>Welcome "+user+"</font>")
        else:
            return render_template('UserLogin.html', msg="<font size=3 color=red>Invalid login details</font>")

@app.route('/Logout')
def Logout():
    return render_template('index.html', msg='')

@app.route('/PredictAction', methods=['GET', 'POST'])
def PredictAction():
    if request.method == 'POST':
        global scaler, selector, dataset, labels, hybrid_model, label_encoder
        testData = pd.read_csv("Dataset/testData.csv")#load test data
        data = testData.values
        for i in range(len(label_encoder)-1):#label encoding from non-numeric to numeric
            le = label_encoder[i]
            testData[le[0]] = pd.Series(le[1].transform(testData[le[0]].astype(str)))#encode all str columns to numeric
        testData.fillna(dataset.mean(), inplace = True)#replace misisng values with mean    
        testData = testData.values    
        testData = scaler.transform(testData)#normalize test data
        testData = selector.transform(testData)#select relevant features
        predict = hybrid_model.predict(testData)#apply extension hybrid model to predict attack type
        output = '<table border=1 align=center width=100%><tr>'
        output += '<th><font size="3" color="black">Test Data</font></th>'
        output += '<th><font size="3" color="blue">Predicted Attack Type</font></th></tr>'
        for i in range(len(predict)):
            output += "<tr>"
            output += '<td><font size="3" color="black">'+str(data[i])+'</font></td>'                
            output += '<td><font size="4" color="red">'+labels[predict[i]]+'</font></td>'            
        output += "</table><br/><br/><br/><br/>"             
        return render_template('UserScreen.html', msg=output)

if __name__ == '__main__':
    app.run()    
