from unittest import result
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import requests
import numpy as np
from urllib.error import URLError
from PIL import Image
import re
import time
import streamlit_modal as modal
import streamlit.components.v1 as components
import torch
from FeedMe.utils import vector_output, score, load_data, load_image, ing_list, vegfilter, difficulty, allergencheck
from ast import literal_eval



# Model for object detection
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

#col1, col2, col3 = st.columns([3, 1])


st.sidebar.header("FeedMe")
image_file = st.sidebar.file_uploader("Open your fridge!", type=["png","jpg","jpeg"])
imageLocation = st.sidebar.empty()
st.subheader("Fridge Image")
 # check supported data for test

if image_file is not None:
	# To See details
	file_details = {"filename":image_file.name, "filetype":image_file.type,
                            "filesize":image_file.size};
    # To View Uploaded Image
	imageLocation.image(load_image(image_file),width=300);

if st.sidebar.button('Inspect my fridge!'):
    if image_file is  None:
        st.write('Can you shome me your fridge please :smile:  :smiling_imp:')
    else:
        # print is visible in the server output, not in the page
        print('button clicked!')
        # Object detection
        results = model(load_image(image_file))
        results.save()
        imageLocation.image(load_image(f"runs/detect/exp/image0.jpg"), width=300)
        shutil. rmtree("runs/detect/exp/")
        # Output ingredients
        output_list = results.pandas().xyxy[0]["name"].unique()
        output_vector = vector_output(output_list)
        st.session_state.vector = output_vector


# Complexity filter
complexity = st.sidebar.select_slider(
     'Select maximum difficulty of the recipe',
     options=['easy', 'medium', 'difficult', 'very difficult'])

complexity_dict = {'easy' : 0, 'medium' : 1, 'difficult' : 2, 'very difficult' : 3}
complexity_value = complexity_dict[complexity]

prep_time = st.sidebar.slider('What maximum prep time do you want ?', 0, 1000, 120)

# Diet filter
diet= st.sidebar.radio(
     "What's your diet",
     ('Omnivore', 'Vegetarian', 'Vegan'))
vegetarian = False
vegan = False

if diet == 'Vegetarian':
    vegetarian = True
if diet == 'Vegan':
    vegan = True

# Allergens filter
allergens_list = ['egg','milk','cheese','mustard', 'peanut', 'soy', 'walnut', 'almond', 'hazelnut', 'pecan',
       'cashew', 'pistachio', 'wheat']

allergies = st.sidebar.multiselect(
     'Select your allergies',
     ['egg','milk','cheese','mustard', 'peanut', 'soy', 'walnut', 'almond', 'hazelnut', 'pecan',
       'cashew', 'pistachio', 'wheat'])

allergens_dict = {}
for allergen in allergens_list:
    if allergen in allergies:
        allergens_dict[allergen] = True
    else:
        allergens_dict[allergen] = False



if st.sidebar.button('FeedMe'):
    st.header("Chef's Choice:")
    data = load_data(3000)
    data = vegfilter(data,vegetarian,vegan)
    data = difficulty(data,prep_time, complexity_value)
    data = allergencheck(data, allergens_dict)
    df = data[ing_list].apply(lambda x: score(x, st.session_state.vector), axis=1)
    data["score"] = df["score"]
    data = data.sort_values(by="score", ascending=False)
    # Dataframe for troubleshooting
    # st.dataframe(data)

if 'data' in locals():
    row = data.head(1)
    one_image = row.Image_Name.iloc[0]
    recipe = row.Instructions.iloc[0]
    ingredient = row['Ingredients'].apply(literal_eval).iloc[0]
    st.session_state.recipe = recipe
    st.session_state.ingredient = ingredient
    st.image(load_image(f"raw_data/Recipes/Food Images/{one_image}.jpg"),width=500)
    st.subheader('Ingredients:')
    for i in ingredient:
        st.write(i)
    st.subheader('Instructions:')
    st.write(recipe)







# if st.sidebar.button('FeedMe'):
#     data["score"] = data[ing_list].apply(lambda x: score(x, output_vector), axis=1)
#     data = data.sort_values(by="score")
#     for row in range(3):
#             one_image=data.Image_Name[row]
#             recipe=data.Instructions[row]

#             ingredient=data.Cleaned_Ingredients[row]
#             st.image(load_image(f"raw_data/Recipes/Food Images/{one_image}.jpg"),width=500);
#             #st.write(data.Title[row])


#             open_modal = st.button("Recipe of " + data.Title[row])

#             if open_modal:
#                 modal.open()

#             if modal.is_open():
#                 with modal.container():
#                     html_string_0 = '''
#                     <h2> Ingredients : </h2>

#                     <script language="javascript">
#                     document.querySelector("h1").style.color = "red";
#                     </script>
#                     '''
#                     components.html(html_string_0)
#                     ingredient= ingredient.split(',')

#                     for index, line in enumerate( ingredient):
#                         line = re.sub("[['!@#$]", '', line)
#                         st.write((index +1) ,"-" ,line )

#                     html_string = '''
#                     <h2> Steps : </h2>

#                     <script language="javascript">
#                     document.querySelector("h1").style.color = "red";
#                     </script>
#                     '''
#                     components.html(html_string)

#                     recipe1=recipe.split('\n')
#                     for index, line in enumerate( recipe1):
#                         st.write((index +1) ,"-" ,line )

#                     st.write("Bon appetit")
