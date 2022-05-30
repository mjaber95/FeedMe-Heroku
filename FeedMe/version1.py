import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
from urllib.error import URLError
from PIL import Image
import re
import time
import streamlit_modal as modal
import streamlit.components.v1 as components
import torch
from FeedMe.utils import vector_output, score, load_data
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

model = torch.hub.load('ultralytics/yolov5', 'custom', path='/Users/mamdouhjaber/code/mjaber95/FeedMe/YOLOv5_model/best.pt')

#col1, col2, col3 = st.columns([3, 1])

def load_image(image_file):
	img = Image.open(image_file)
	return img
st.sidebar.header("FeedMe")
st.subheader("Fridge Image")
image_file = st.sidebar.file_uploader("Open your fridge!", type=["png","jpg","jpeg"]) # check supported data for test

if image_file is not None:
	# To See details
	file_details = {"filename":image_file.name, "filetype":image_file.type,
                            "filesize":image_file.size};
    # To View Uploaded Image
	st.sidebar.image(load_image(image_file),width=275);

if st.sidebar.button('Get my recipe'):
    if image_file is  None:
        st.write('Can you shome me your fridge please :smile:  :smiling_imp:')
    else:
        # print is visible in the server output, not in the page
        print('button clicked!')
        results = model(load_image(image_file))
        #st.image(results.imgs[0],width=500)
        output_list = results.pandas().xyxy[0]["name"].unique()
        output_vector = vector_output(output_list)
        # results.show()
        data = load_data(1000)
        df = data[ing_list].apply(lambda x: score(x, output_vector), axis=1)
        data["score"] = df["score"]
        data = data.sort_values(by="score", ascending=False)
        st.dataframe(data)
        for row in data.head(3).iterrows():
                one_image=row[1].Image_Name
                recipe=row[1].Instructions

                ingredient=row[1].Cleaned_Ingredients
                st.image(load_image(f"raw_data/Recipes/Food Images/{one_image}.jpg"),width=500);
                #st.write(data.Title[row])


                open_modal = st.button("Recipe of " + row[1].Title)

                if open_modal:
                    modal.open()

                if modal.is_open():
                    with modal.container():
                        html_string_0 = '''
                        <h2> Ingredients : </h2>

                        <script language="javascript">
                        document.querySelector("h1").style.color = "red";
                        </script>
                        '''
                        components.html(html_string_0)
                        ingredient= ingredient.split(',')

                        for index, line in enumerate( ingredient):
                            line = re.sub("[['!@#$]", '', line)
                            st.write((index +1) ,"-" ,line )

                        html_string = '''
                        <h2> Steps : </h2>

                        <script language="javascript">
                        document.querySelector("h1").style.color = "red";
                        </script>
                        '''
                        components.html(html_string)

                        recipe1=recipe.split('\n')
                        for index, line in enumerate( recipe1):
                            st.write((index +1) ,"-" ,line )

                        st.write("Bon appetit")
        st.write('Your Fridg contains :')
        st.write('Wow! You can prepare one of those recipes: ')

        'We are looking for the perfect recepies for you...'

        # Add a placeholder
        # latest_iteration = st.empty()
        # bar = st.progress(0)

        # for i in range(10):
        #     # Update the progress bar with each iteration.
        #     latest_iteration.text(f'Iteration {i+1}')
        #     bar.progress(i + 1)
        #     time.sleep(0.1)

        '...and now we\'re done! Choose your recipe'







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
