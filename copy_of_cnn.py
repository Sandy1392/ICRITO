# -*- coding: utf-8 -*-
"""Copy of CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qktR_ybLzIbcISkPdTU_FcAe8PEhcAb8
"""

# univariate CNN example
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten

import pandas
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

from google.colab import drive
drive.mount('/content/gdrive')

directory_root = '/content/gdrive/MyDrive/Colab Notebooks/Dataset/JTDS.csv'

import pandas as pd
df = pd.read_csv(directory_root)
print(df)

df.drop(df.columns[[0]], axis = 1, inplace = True)
X = df.iloc[:,:-1]                                                                               
print(X)
y = df.iloc[:,-1]
print(y)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y)
encoded_y = encoder.transform(y)

from sklearn.feature_selection import mutual_info_classif
importances = mutual_info_classif(X,encoded_y)
print("Values of Information Gain for each feature wrt the target variable is:\n", importances)

print(type(importances)) # numpy array of information gain values

print("\nIn ascending order:", np.sort(importances))


# Metrics and their Information Gains/Importances
print("\nFeature and its Importance:")
for i in range(len(df.columns)-1): # or range(11), 12 columns 0 to 11 with 11 feats.+ 1 target, 0 to 10 or 12-1=11
    print(df.columns[i], importances[i])
    
# Plotting the values
feat_importances = pd.Series(importances, df.columns[0:len(df.columns)-1])
feat_importances.plot(kind='barh', color='teal')
plt.show()

from sklearn.feature_selection import SelectKBest

print("\nBefore Feature Selection:\n", X)

# define feature selection
fs_IG = SelectKBest(score_func=mutual_info_classif, k=7)
            
# apply feature selection
X_IG_selected = fs_IG.fit_transform(X, encoded_y)

print("\nRows and Columns after fit_transofrm() using Information Gain:", X_IG_selected.shape)
print("\nAfter Feature Selection using Information Gain:\n", X_IG_selected)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_IG_selected, encoded_y, train_size=0.67,test_size=0.33, random_state=101)

y_train.shape

y_train1 = y_train
y_test1 = y_test
# convert integers to dummy variables (i.e. one hot encoded)
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense

(X_train,y_train) , (X_test,y_test)=mnist.load_data()
#reshaping data
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], X_train.shape[2], 1))
X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],X_test.shape[2],1)) 
#checking the shape after reshaping
print(X_train.shape)
print(X_test.shape)
#normalizing the pixel values
X_train=X_train/255
X_test=X_test/255

#defining model
model=Sequential()
#adding convolution layer
model.add(Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1)))
#adding pooling layer
model.add(MaxPool2D(2,2))
#adding fully connected layer
model.add(Flatten())
model.add(Dense(100,activation='relu'))
#adding output layer
model.add(Dense(10,activation='softmax'))
#compiling the model
model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
#fitting the model
model.fit(X_train,y_train,epochs=50)

#evaluting the model
model.evaluate(X_test,y_test)

yp = model.predict(X_test)
yp
y_predicted_labels = [np.argmax(i) for i in yp]
y_predicted_labels

import seaborn as sn
import tensorflow as tf
import matplotlib.pyplot as plt
y_predicted = model.predict(X_test)
y_predicted_labels = [np.argmax(i) for i in y_predicted]
cm = tf.math.confusion_matrix(labels=y_test,predictions=y_predicted_labels)

plt.figure(figsize = (5,5))
sn.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

from sklearn.metrics import confusion_matrix , classification_report
import numpy as np
y_pred = model.predict(X_test)
y_pred_classes = [np.argmax(element) for element in y_pred]
print("Classification Report: \n", classification_report(y_test, y_predicted_labels))