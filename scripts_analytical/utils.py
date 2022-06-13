import os
import itertools

import pandas as pd
import numpy as np
from sklearn.metrics import f1_score,roc_curve,confusion_matrix
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

def plot_candletick(df):
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Candlestick(
            x=df['event_time'],
            open=df['open_price'],
            high=df['high_price'],
            low=df['low_price'],
            close=df['close_price']
        ))
    
    fig.show()
      
def plot_candletick_anomaly(df, filepath_output, left_b, right_b):

    df = df[left_b:right_b]
        
    fig = px.scatter(
        x = df[df['target'] == 1]['t_start'],
        y = df[df['target'] == 1]['open_price']
    )

    fig.add_trace(
        go.Candlestick(
            x=df['t_start'],
            open=df['open_price'],
            high=df['high_price'],
            low=df['low_price'],
            close=df['close_price']
        ))
    
    fig.show()

    fig.write_image(os.path.join(filepath_output,'candlestick.png'))

def plot_roc_curve(y_true, y_score):
    
    fpr, tpr, thresholds = roc_curve(y_true, y_score)

    plt.plot([0,1], [0,1], linestyle='--', label = 'No Skill')
    plt.plot(fpr, tpr, marker='.', label = 'CatBoost')

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    plt.legend()

    plt.show()

def find_max_fscore(y_true, y_score):

    f_score = []
    cutoff_list = np.arange(0,1,0.01)
 
    for cutoff in cutoff_list:
        y_pred = (y_score > cutoff).astype(int)
        f_scr = f1_score(y_true, y_pred, pos_label=1, average='binary')
        f_score.append(f_scr)
       
    f_score = pd.Series(f_score, index=cutoff_list)

    return f_score.idxmax()

def plot_confusion_matrix(y_true, y_score, cutoff):
    
    cm = confusion_matrix(y_true, y_score > cutoff)
    classes = ['Non-event', 'event']
    
    fig, ax = plt.subplots()
    
    ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    
    ax.set_title('Confusion matrix')
    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')
    
    ax.set_xticks(np.arange(len(classes)), classes, rotation=45)
    ax.set_yticks(np.arange(len(classes)), classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    fig.set_size_inches(8, 5)
    fig.set_tight_layout(True)
    
    plt.show()

def plot_feature_importnaces(model,x_train):
    
    importances = model.get_feature_importance()
    forest_importances = pd.Series(importances, index=x_train.columns.to_list())
    forest_importances = forest_importances.sort_values(ascending = False)
    
    fig, ax = plt.subplots()
    forest_importances.plot.bar(ax=ax)
    ax.set_title("Feature importances")
    fig.tight_layout()
    plt.show()