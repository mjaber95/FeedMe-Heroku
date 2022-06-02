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
from PIL import Image


# Model for object detection
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
inspection_status = False
#col1, col2, col3 = st.columns([3, 1])
image = Image.open('images/LogoFeedMe.png')
st.sidebar.image(image)

st.sidebar.header("Fridge Inspection")

image_file = st.sidebar.file_uploader(label = 'Please upload a picture of your fridge', type=["png","jpg","jpeg"])
imageLocation = st.sidebar.empty()
 # check supported data for test


if 'key' not in st.session_state:
    st.session_state['key'] = 'value'
    st.session_state['click'] = 'value'


if image_file is not None:
	# To See details
	#file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size};
    # To View Uploaded Image
    imageLocation.image(load_image(image_file),width=300)


if st.sidebar.button('Inspect my fridge!'):
    if image_file is  None:
        st.sidebar.write("I know you are hungry but I can't help you without a picture :smile:  :smiling_imp:")
    else:
        # print is visible in the server output, not in the page
        print('button clicked!')
        # Object detection
        results = model(load_image(image_file))
        results.save()
        image2 = load_image(f"runs/detect/exp/image0.jpg")
        imageLocation.image(load_image(f"runs/detect/exp/image0.jpg"), width=300)
        shutil. rmtree("runs/detect/exp/")
        # Output ingredients
        output_list = results.pandas().xyxy[0]["name"].unique()
        output_vector = vector_output(output_list)
        st.session_state.vector = output_vector
        st.session_state.image = image2



m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 204, 204);color:grey;font-size:20px;height:4em;width:15em;border-radius:7px 7px 7px 7px;;
}
</style>""", unsafe_allow_html=True)


try:
    if image_file is not None:
        imageLocation.image(st.session_state.image, width=300)
        st.sidebar.header("Filters")
        st.sidebar.subheader("Complexity")
        complexity = st.sidebar.select_slider(
            'Are you a beginner or ready to please Gordon Ramsay ? Select a maximum complexity level !',
            options=['Easy', 'Medium', 'Difficult', 'Gordon Ramsay Tier'],value='Gordon Ramsay Tier')

        complexity_dict = {'Easy' : 0, 'Medium' : 1, 'Difficult' : 2, 'Gordon Ramsay Tier' : 3}
        complexity_value = complexity_dict[complexity]
        st.sidebar.subheader("Preparation Time")
        prep_time = st.sidebar.slider('When do you want to eat ? (in minutes)', 0, 600, 600, 15)

        # Diet filter
        st.sidebar.subheader("Diet")
        diet= st.sidebar.radio(
            "If you have any preferences in your diet, please select the appropriate item.",
            ('Omnivore', 'Vegetarian', 'Vegan'))
        vegetarian = False
        vegan = False

        if diet == 'Vegetarian':
            vegetarian = True
        if diet == 'Vegan':
            vegan = True
        st.sidebar.subheader("Allergens")
        # Allergens filter
        allergens_list = ['egg','milk','cheese','mustard', 'peanut', 'soy', 'walnut', 'almond', 'hazelnut', 'pecan',
            'cashew', 'pistachio', 'wheat']

        allergies = st.sidebar.multiselect(
            'If you have any allergies, let us know and we will take away those recipes.',
            ['egg','milk','cheese','mustard', 'peanut', 'soy', 'walnut', 'almond', 'hazelnut', 'pecan',
            'cashew', 'pistachio', 'wheat'])

        allergens_dict = {}
        for allergen in allergens_list:
            if allergen in allergies:
                allergens_dict[allergen] = True
            else:
                allergens_dict[allergen] = False
except:
    pass


try:
    if image_file is not None:
        imageLocation.image(st.session_state.image, width=300)
        if st.sidebar.button('FeedMe'):
            st.header("Chef's Choice:")
            data = load_data(3500)
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
            st.subheader(row['Title'].iloc[0])

            st.image(load_image(f"raw_data/Recipes/Food Images/{one_image}.jpg"),width=600)
            expander = st.expander("Details")
            i=1
            prep_time=row["Prep Time Range"].iloc[0]
            complexe=row["complexity_label"].iloc[0]
            if row["vegetarian"].iloc[0] == 1:
                veggie = 'Yes'
            else:
                veggie = 'No'
            if row["vegan"].iloc[0] == 1:
                vegan2 = 'Yes'
            else:
                vegan2 = 'No'

            expander.write(f"Preparation Time:  {prep_time} "  )
            expander.write(f"Complexity :   {complexe.capitalize()} ")
            expander.write(f"Vegetarian :   {veggie}")
            expander.write(f"Vegan :   {vegan2}")

            st.subheader('Ingredients:')
            for index, line in enumerate( ingredient):

                st.write( '\-' ,line   )
            st.subheader('Instructions:')
            #st.write(recipe)
            recipe1=recipe.split('.')

            for index, line in enumerate( recipe1):
                line = re.sub("[(['!@#$)]", '', line)
                if index+1<len(recipe1):
                    st.write((index+1 ) ,"-" ,line )

except:
    pass




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
