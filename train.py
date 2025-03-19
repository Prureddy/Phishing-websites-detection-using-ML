# Purpose - This file is used to create a classifier and store it in a .pkl file. You can modify the contents of this
# file to create your own version of the classifier.

import numpy as np

from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, classification_report
# from sklearn import metrics

import joblib



def training():
    # labels = []
    # data_file = open('dataset/Training Dataset.arff').read()
    # data_list = data_file.split('\r\n')
    # data = np.array(data_list)
    # data1 = [i.split(',') for i in data_list]
    # data1 = data1[0:-1]
    # print(data1)
    # data1 = np.array(data1)
    # print(data1)
    # for i in data1:
    #     labels.append(i[30])
    # labels = np.array(labels).astype(np.float)
    # # data1 = np.array(data1)
    # features = data1[:, :-1]
    # features = np.array(features).astype(np.float)
    # # Choose only the relevant features from the data set.
    # features = features[:, [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 22, 23, 24, 25, 27, 29]]

    labels = []
    data = np.genfromtxt('dataset/Training Dataset.arff', delimiter=',', dtype=str)

    # Extract labels (assuming the label is the last column, change index if different)
    for i in data:
        labels.append(i[30])
    labels = data[:, -1].astype(np.float)

    # Convert the rest of the data into float (excluding the last column)
    data1 = data[:, :-1].astype(np.float)

    # Choose only the relevant features from the data set.
    features = data1[:, [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 22, 23, 24, 25, 27, 29]]

    features_train = features
    labels_train = labels
    # features_test=features[10000:]
    # labels_test=labels[10000:]


    print("\n\n ""Random Forest Algorithm Results"" ")
    clf4 = RandomForestClassifier(min_samples_split=7, verbose=True)
    clf4.fit(features_train, labels_train)
    importances = clf4.feature_importances_
    std = np.std([tree.feature_importances_ for tree in clf4.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(features_train.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # pred4=clf4.predict(features_test)
    # print(classification_report(labels_test, pred4))
    # print 'The accuracy is:', accuracy_score(labels_test, pred4)
    # print metrics.confusion_matrix(labels_test, pred4)

    # sys.setrecursionlimit(9999999)
    joblib.dump(clf4, 'classifier/random_forest.pkl', compress=9)


    # import joblib
    # import pandas as pd
    # import seaborn as sns
    # import matplotlib.pyplot as plt
    # import random
    # import pickle
    # from sklearn.ensemble import RandomForestClassifier
    # from sklearn.model_selection import train_test_split

    # df = pd.read_csv('https://raw.githubusercontent.com/Govind155/Web-Phishing-Detection-/main/dataset.csv')
        


    # # Your data preprocessing and feature extraction code here
    # df.drop(['index','port','Redirect','on_mouseover','popUpWidnow','RightClick','Page_Rank','Links_pointing_to_page'], axis=1, inplace=True)
    # l = [1, -1]
    # length = len(df)
    # for i in range(length):
    #     if df['having_At_Symbol'].isnull().sum():
    #         rand = random.randint(0, 1)
    #         df['having_At_Symbol'][i] = l[rand]

    # # Drop NaN values if any
    # df.dropna(inplace=True)

    # X = df.drop(columns='Result')
    # Y = df['Result']


    # # Split the data into training and testing sets
    # train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.40, random_state=10)

    # # Train the RandomForestClassifier
    # """ rfc = RandomForestClassifier()
    # model = rfc.fit(train_X, train_Y) """
    # from sklearn.svm import SVC
    # svc=SVC()
    # model=svc.fit(train_X,train_Y)
    # svm_predict=model.predict(test_X)
    # """ print('The accuracy of SVM Classifier is: ', 100.0 * accuracy_score(svm_predict,test_Y))
    # print(classification_report(svm_predict,test_Y)) """


    # # Save the trained model as model.pkl
    # # with open('static/model.pkl', 'wb') as file:
    # #     pickle.dump(model, file)
    # joblib.dump(model, 'classifier/random_forest.pkl', compress=9)

    # print( "Model trained successfully!")