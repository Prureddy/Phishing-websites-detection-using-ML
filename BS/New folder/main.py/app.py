from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
from train import training
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)
def preprocess_url(url):
    df = pd.read_csv('https://raw.githubusercontent.com/Govind155/Web-Phishing-Detection-/main/dataset.csv')
    df.head()
    sns.heatmap(df[0:120].isnull(), cmap= 'viridis')
    plt.savefig('heatmap.png')
    df.describe()
    print(df.corr()['Result'].sort_values())
    # Remove features having correlation coeff. between +/- 0.03
    df.drop(['Favicon','Iframe','Redirect',
                    'popUpWidnow','RightClick','Submitting_to_email'],axis=1,inplace=True)
    print(len(df.columns))
    sns.heatmap(df.corr())
    plt.savefig('corr.png')
    l = [1,-1]
    length = len(df)
    # df.head()
    for i in range(length):
        if(df['having_At_Symbol'].isnull().sum()):
            rand = random.randint(0,1)
            df['having_At_Symbol'][i] = l[rand]

    df.head()
    # print(df['having_At_Symbol'])
    sns.heatmap(df.isnull())
    plt.savefig('clean_heatmap.png')
    sns.set_style('whitegrid')
    """ sns.countplot(x='having_At_Symbol',data=df)
    sns.countplot(x='having_IPhaving_IP_Address',data=df)
    sns.countplot(x='web_traffic', data=df)
    sns.countplot(x='Result', data=df)
    sns.countplot(x='Links_pointing_to_page', data=df)
    sns.countplot(x='Result', hue='having_At_Symbol', data=df)
    sns.distplot(df['Result'], color='darkred')
    sns.distplot(df['Links_pointing_to_page'])
    sns.displot(df['web_traffic']) """
    a=len(df[df.Result==0])
    b=len(df[df.Result==-1])
    c=len(df[df.Result==1])
    print("Count of Legitimate Websites = ", b)
    print("Count of Suspicious Websites = ", a)
    print("Count of Phishy Websites = ", c)
    df.drop(['index'],axis=1,inplace=True)
    print(len(df.columns))
    #df.plot.hist(subplots=True,layout=(5,5),figsize=(15, 15), bins=20)
    df.corr()
    from sklearn.model_selection import train_test_split,cross_val_score
    X= df.drop(columns='Result')
    X.head()
    Y=df['Result']
    Y=pd.DataFrame(Y)
    Y.head()
    train_X,test_X,train_Y,test_Y=train_test_split(X,Y,test_size=0.40,random_state=10)
    print("Training set has {} samples.".format(train_X.shape[0]))
    print("Testing set has {} samples.".format(test_X.shape[0]))



# Function to preprocess the input URL and extract features
""" def preprocess_url(url):
    import numpy as np
 """
""" def preprocess_url(url):
    import numpy as np
    # Basic URL preprocessing (You can add more complex preprocessing based on your requirements)
    url_length = len(url)
    num_dots = url.count('.')
    num_hyphens = url.count('-')
    num_digits = sum(1 for char in url if char.isdigit())

    # Store the extracted features in a 1D array
    features = np.array([url_length, num_dots], dtype=float)

    # Check for NaN values (in case any feature extraction resulted in NaN)
    if np.isnan(features).any():
        # If there are NaN values, reshape features into a 2D column vector
        features = features.reshape(-1, 1)
    else:
        # If there are no NaN values, reshape features into a 2D row vector
        features = features.reshape(1, -1)

    return features

    #sns.heatmap(df[0:120].isnull(), cmap= 'viridis')
    plt.savefig('heatmap.png')
    # Your URL preprocessing code here
    # ...

    # Return the extracted features as a NumPy array
    
    #return features """

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['GET', 'POST'])
def train():
    training()
    df = pd.read_csv('https://raw.githubusercontent.com/Govind155/Web-Phishing-Detection-/main/dataset.csv')
    
    

    # Your data preprocessing and feature extraction code here
    df.drop(['Favicon','Iframe','Redirect','popUpWidnow','RightClick','Submitting_to_email'], axis=1, inplace=True)
    l = [1, -1]
    length = len(df)
    for i in range(length):
        if df['having_At_Symbol'].isnull().sum():
            rand = random.randint(0, 1)
            df['having_At_Symbol'][i] = l[rand]

    # Drop NaN values if any
    df.dropna(inplace=True)

    X = df.drop(columns='Result')
    Y = df['Result']
    

    # Split the data into training and testing sets
    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.40, random_state=10)

    # Train the RandomForestClassifier
    """ rfc = RandomForestClassifier()
    model = rfc.fit(train_X, train_Y) """
    from sklearn.svm import SVC
    svc=SVC()
    model=svc.fit(train_X,train_Y)
    svm_predict=model.predict(test_X)
    """ print('The accuracy of SVM Classifier is: ', 100.0 * accuracy_score(svm_predict,test_Y))
    print(classification_report(svm_predict,test_Y)) """


    # Save the trained model as model.pkl
    with open('static/model.pkl', 'wb') as file:
        pickle.dump(model, file)

    return "Model trained successfully!"

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    # Preprocess the input URL and extract features
    features = preprocess_url(url)

    # Load the pre-trained model
    with open('static/model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Perform prediction using the pre-trained model
    prediction = model.predict([features])[0]

    # Display the result on the prediction page
    return render_template('prediction.html', url=url, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)





#  df = pd.read_csv('https://raw.githubusercontent.com/Govind155/Web-Phishing-Detection-/main/dataset.csv')
    
    

#     # Your data preprocessing and feature extraction code here
#     df.drop(['Favicon','Iframe','Redirect','popUpWidnow','RightClick','Submitting_to_email'], axis=1, inplace=True)
#     l = [1, -1]
#     length = len(df)
#     for i in range(length):
#         if df['having_At_Symbol'].isnull().sum():
#             rand = random.randint(0, 1)
#             df['having_At_Symbol'][i] = l[rand]

#     # Drop NaN values if any
#     df.dropna(inplace=True)

#     X = df.drop(columns='Result')
#     Y = df['Result']
    

#     # Split the data into training and testing sets
#     train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.40, random_state=10)

#     # Train the RandomForestClassifier
#     """ rfc = RandomForestClassifier()
#     model = rfc.fit(train_X, train_Y) """
#     from sklearn.svm import SVC
#     svc=SVC()
#     model=svc.fit(train_X,train_Y)
#     svm_predict=model.predict(test_X)
#     """ print('The accuracy of SVM Classifier is: ', 100.0 * accuracy_score(svm_predict,test_Y))
#     print(classification_report(svm_predict,test_Y)) """


#     # Save the trained model as model.pkl
#     with open('static/model.pkl', 'wb') as file:
#         pickle.dump(model, file)

#     return "Model trained successfully!"

# @app.route('/predict', methods=['POST'])
# def predict():
#     url = request.form['url']

#     # Preprocess the input URL and extract features
#     features = preprocess_url(url)

#     # Load the pre-trained model
#     with open('static/model.pkl', 'rb') as file:
#         model = pickle.load(file)

#     # Perform prediction using the pre-trained model
#     prediction = model.predict([features])[0]

#     # Display the result on the prediction page
#     return render_template('prediction.html', url=url, prediction=prediction)

# if __name__ == '__main__':
#     app.run(debug=True)
