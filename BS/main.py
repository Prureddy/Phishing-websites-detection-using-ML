import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

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
sns.countplot(x='having_At_Symbol',data=df)
sns.countplot(x='having_IPhaving_IP_Address',data=df)
sns.countplot(x='web_traffic', data=df)
sns.countplot(x='Result', data=df)
sns.countplot(x='Links_pointing_to_page', data=df)
sns.countplot(x='Result', hue='having_At_Symbol', data=df)
sns.distplot(df['Result'], color='darkred')
sns.distplot(df['Links_pointing_to_page'])
sns.displot(df['web_traffic'])
a=len(df[df.Result==0])
b=len(df[df.Result==-1])
c=len(df[df.Result==1])
print("Count of Legitimate Websites = ", b)
print("Count of Suspicious Websites = ", a)
print("Count of Phishy Websites = ", c)
df.drop(['index'],axis=1,inplace=True)
print(len(df.columns))

df.plot.hist(subplots=True,layout=(5,5),figsize=(15, 15), bins=20)
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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
logreg=LogisticRegression()
model_1=logreg.fit(train_X,train_Y)
logreg_predict= model_1.predict(test_X)
print('The accurcy of Logistic Regression Model is : ', 100.0 * accuracy_score(logreg_predict,test_Y))
print(classification_report(logreg_predict,test_Y))
def plot_confusion_matrix(test_Y, predict_y):
 C = confusion_matrix(test_Y, predict_y)
 A =(((C.T)/(C.sum(axis=1))).T)
 B =(C/C.sum(axis=0))
 plt.figure(figsize=(20,4))
 labels = [1,2]
 cmap=sns.light_palette("blue")
 plt.subplot(1, 3, 1)
 sns.heatmap(C, annot=True, cmap=cmap, fmt=".3f", xticklabels=labels, yticklabels=labels)
 plt.xlabel('Predicted Class')
 plt.ylabel('Original Class')
 plt.title("Confusion matrix")
 plt.subplot(1, 3, 2)
 sns.heatmap(B, annot=True, cmap=cmap, fmt=".3f", xticklabels=labels, yticklabels=labels)
 plt.xlabel('Predicted Class')
 plt.ylabel('Original Class')
 plt.title("Precision matrix")
 plt.subplot(1, 3, 3)
 sns.heatmap(A, annot=True, cmap=cmap, fmt=".3f", xticklabels=labels, yticklabels=labels)
 plt.xlabel('Predicted Class')
 plt.ylabel('Original Class')
 plt.title("Recall matrix")
 plt.show()



