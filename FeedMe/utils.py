from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
import pandas as pd

ing_list = ["apple",
        "banana",
        "beef",
        "blueberry",
        "bread",
        "butter",
        "carrot",
        "cheese",
        "chicken",
        "chocolate",
        "corn",
        "egg",
        "flour",
        "bean",
        "ham",
        "cream",
        "lime",
        "milk",
        "mushroom",
        "onion",
        "potato",
        "shrimp",
        "spinach",
        "strawberry",
        "sugar",
        "tomato"]


def vector_output(list_1):
    ing_list = ["apple",
                "banana",
                "beef",
                "blueberry",
                "bread",
                "butter",
                "carrot",
                "cheese",
                "chicken",
                "chocolate",
                "corn",
                "egg",
                "flour",
                "bean",
                "ham",
                "cream",
                "lime",
                "milk",
                "mushroom",
                "onion",
                "potato",
                "shrimp",
                "spinach",
                "strawberry",
                "sugar",
                "tomato"]
    V = ing_list.copy()
    for i, ing in enumerate(V):
        if ing in list_1:
            V[i] = 1
        else:
            V[i] = 0
    return V

def score(row, vector):
    #computes dot product
    A = row.to_numpy()
    row["score"] = np.matmul(A, vector)
    return row

def load_data(nrows):
    data = pd.read_csv("raw_data/3105_receipe_final.csv", nrows=nrows)
    return data


def vegfilter(df, vegetarian=False, vegan=False):
    if vegan == True:
        df_filtered = df[df['vegan']==1]
    elif vegetarian == True:
        df_filtered = df[df['vegetarian']==1]
    else:
        df_filtered = df
    return df_filtered


def difficulty(df, max_prep_time=10000, max_complexity=0):
    df_filtered = df[df['Prep Time']<=max_prep_time]
    df_filtered = df_filtered[df_filtered['complexity']<=max_complexity]
    return df_filtered

def allergencheck(df, allergens):
    df_f = df
    for key in allergens:
        print(key)
        print(df_f.shape)
        if allergens[key] == True:
            df_f = df_f[df_f[key]==0]
    return df_f


def load_image(image_file):
	img = Image.open(image_file)
	return img
