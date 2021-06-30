#Load libraries
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import base64
from decimal import Decimal

#Data & Comparison libs
from pygrowup import Observation

#Modeling
import xgboost as xgb


#Set title and favicon
st.set_page_config(page_title='RoboDx', page_icon='https://www.squadhelp.com/story_images/visual_images/1591351763-robodx.jpg')

###################### CSS Styling ############################################################################################################
#Remove rainbow bar
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

#Hide hamburger menu & footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#Spinner style
st.markdown(
  """
  <style>
    .st-bv {
      background-color: #F9F9F9;
      border: #F9F9F9;
      }
  </style>""",
  unsafe_allow_html=True
)

st.markdown(
  """
  <style>
    .css-1v4eu6x {
    font-family: Avenir,Helvetica Neue,sans-serif;
    margin-bottom: -1rem;
    }
  </style>""",
  unsafe_allow_html=True
)
st.markdown(
  """
  <style>
    .st-bt {
    color: #262730;
    }
  </style>""",
  unsafe_allow_html=True
)

#General font (body)
st.markdown(
  """
  <style>
    body {
    font-family: Avenir,Helvetica Neue,sans-serif;
    }

    .fullScreenFrame > div {
    display: flex;
    justify-content: center;
    }
  </style>""",
  unsafe_allow_html=True
)


###################### End CSS Styling ############################################################################################################


#Create initial titles/subtitles
st.markdown('<h1 style="font-family:Avenir,Helvetica Neue,sans-serif;"> RoboDx </h1>', unsafe_allow_html=True)
st.markdown("""<h2 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Using data to understand your child's health </h2>""", unsafe_allow_html=True)
st.text("")

#Display image/avatar
st.image('robo.png')

st.markdown("""<p style="font-family:Avenir,Helvetica Neue,sans-serif;"> The following tool will help you understand and indentify whether or not your child's (up to 5 years) anthropometric measurements are within the expected ranges depending on his sex, age, weight, and height.</p>""", unsafe_allow_html=True)


#Input child's data
st.markdown("""<h3 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Child's Data </h3>""", unsafe_allow_html=True)
dob = st.date_input('Date of Birth')
today = date.today()
#st.date_input('Date of Measurement')

#Input gender
sex = st.selectbox("Child's Sex", ["male", "female"], key='sex_box', index=1) #Add a dropdown element

if (sex == "male"):
  sex = Observation.MALE
else:
  sex = Observation.FEMALE

#Input weight & height
weight = st.number_input("Weight (kg)", min_value=1.00, max_value=125.00, step=0.1)
height = st.number_input("Height (inch)", min_value=18.00, max_value=43.00, step=0.1)
height = round(height * 2.54, 2)
st.text("")


#Parents Data
st.markdown("""<h3 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Mom and Dad's Data </h3>""", unsafe_allow_html=True)

#Input mother height
st.markdown("""<p style="font-family:Avenir,Helvetica Neue,sans-serif;"> Input the <b>Mother's</b> height. First ft. then inches.</p>""", unsafe_allow_html=True)
Mother_height_feet = st.number_input("Mother's Height (ft)", min_value=0.00, max_value=8.00, value=5.00, step=1.0)
Mother_height_inch = st.number_input("Mother's Height (inch)", min_value=0.00, max_value=11.00, value=2.00, step=1.0)
Mother_feet_to_cm = Mother_height_feet / 0.03281
Mother_inch_to_cm = Mother_height_inch * 2.54
Mother_height_final = Mother_feet_to_cm + Mother_inch_to_cm

#Input father height
st.markdown("""<p style="font-family:Avenir,Helvetica Neue,sans-serif;"> Input the <b>Father's</b> height. First ft. then inches.</p>""", unsafe_allow_html=True)
Father_height_feet = st.number_input("Father's Height (ft)", min_value=0.00, max_value=8.00, value=5.00, step=1.0)
Father_height_inch = st.number_input("Father's Height (inch)", min_value=0.00, max_value=11.00, value=10.00, step=1.0)
Fahter_feet_to_cm = Father_height_feet / 0.03281
Father_inch_to_cm = Father_height_inch * 2.54
Father_height_final = Fahter_feet_to_cm + Father_inch_to_cm


#Convert from cm to inches
Mother_height = round(Mother_height_final / 2.54, 2)
Father_height = round(Father_height_final / 2.54, 2)
st.text("")


#Siblings
st.markdown("""<h3 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Siblings </h3>""", unsafe_allow_html=True)
siblings = st.number_input("How many children do you have?", min_value=1, max_value=15, step=1)

if st.button('Calculate Results'):
  
  #Instantiate the observation comparison object
  obs = Observation(sex=sex, dob=dob,
                  date_of_observation=today)
  try:
  #Get z-scores
    z_weight_for_age = obs.weight_for_age(Decimal(weight))
    z_length_or_height_for_age = obs.length_or_height_for_age(Decimal(height))
    z_weight_for_length = obs.weight_for_length(Decimal(weight), Decimal(height))
  except Exception as error:
    st.write(error, ", the measurement provided is likely an error, please review your entry and try again.", unsafe_allow_html=True)
  
  #Weight-to-age ratio
  st.markdown('<h3 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Weight for Age </h3>', unsafe_allow_html=True)
  if (z_weight_for_age < 2):
    results ='<p style="font-family:Avenir,Helvetica Neue,sans-serif;">Your childs weight-to-age ratio is '  + '<b>'+str(z_weight_for_age)+'</b> standard deviations '+' from the mean, which is still consider within the normal range. </p>'
    st.write(results, unsafe_allow_html=True)
  elif (z_weight_for_age < 3):
    st.write('<p style="font-family:Avenir,Helvetica Neue,sans-serif;">Your childs weight-to-age ratio is', '<b>"'+str(z_weight_for_age)+'"', '</b> standard deviations from the mean, which is considered to be outside or the normal range, it is recommended to visit your childs pediatrician and provide this information to do further tests.</p>', unsafe_allow_html=True)
  else:
    st.write('<p style="font-family:Avenir,Helvetica Neue,sans-serif;">The measurement seems to extreme, please review your measurement and try again, if it is indeed correct, please visit a doctor and provide him with further information</p>', unsafe_allow_html=True)

  #Height-to-age ratio
  st.markdown('<h3 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Height for Age </h3>', unsafe_allow_html=True)
  if (z_length_or_height_for_age < 2):
    results ='<p style="font-family:Avenir,Helvetica Neue,sans-serif;">Your childs height-to-age ratio is '  + '<b>'+str(z_length_or_height_for_age)+'</b> standard deviations '+' from the mean, which is still consider within the normal range. </p>'
    st.write(results, unsafe_allow_html=True)
  elif (z_length_or_height_for_age < 3):
    st.write('<p style="font-family:Avenir,Helvetica Neue,sans-serif;">Your childs height-to-age ratio is', '<b>"'+str(z_length_or_height_for_age)+'"', '</b> standard deviations from the mean, which is considered to be outside or the normal range, it is recommended to visit your childs pediatrician and provide this information to do further tests.</p>', unsafe_allow_html=True)
  else:
    st.write('<p style="font-family:Avenir,Helvetica Neue,sans-serif;">The measurement seems to extreme, please review your measurement and try again, if it is indeed correct, please visit a doctor and provide him with further information</p>', unsafe_allow_html=True)

  #Weight-to-length/height ratio
  st.markdown('<h3 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Weight to Height Ratio </h3>', unsafe_allow_html=True)
  if (z_weight_for_length < 2):
    results ='<p style="font-family:Avenir,Helvetica Neue,sans-serif;">Your childs weight-to-height ratio is '  + '<b>'+str(z_weight_for_length)+'</b> standard deviations '+' from the mean, which is still consider within the normal range. </p>'
    st.write(results, unsafe_allow_html=True)
  elif (z_weight_for_length < 3):
    st.write('<p style="font-family:Avenir,Helvetica Neue,sans-serif;">Your childs weight-to-height ratio is', '<b>"'+str(z_weight_for_length)+'"', '</b> standard deviations from the mean, which is considered to be outside or the normal range, it is recommended to visit your childs pediatrician and provide this information to do further tests.</p>', unsafe_allow_html=True)
  else:
    st.write('<p style="font-family:Avenir,Helvetica Neue,sans-serif;">The measurement seems to extreme, please review your measurement and try again, if it is indeed correct, please visit a doctor and provide him with further information</p>', unsafe_allow_html=True)


  #Modeling
  st.markdown('<h3 style="font-family:Avenir,Helvetica Neue,sans-serif;"> Target Height </h3>', unsafe_allow_html=True)

  #Load dataset
  data = pd.read_csv("Galtons Height Data.csv")
  
  #Define target & features
  X = data.drop(['Height','Family'], axis=1)
  y = data['Height']
  
  #Sex indicator 
  if (sex == "male"):
    sex_indicator = 0.0
  else:
    sex_indicator = 1.0

  #Prepare data for prediction
  predict_child = pd.DataFrame({"Father": Father_height, "Mother": Mother_height, "Female": sex_indicator, "Kids": siblings}, index=[0])

  def target_height_prediction(predict_child):
    #Instantiate & fit data to the model 
    params = {'colsample_bytree':0.20759825721739386, 'max_depth':16, 'learning_rate':0.20681877827930437, 'n_estimators':50}
    model = xgb.XGBRegressor(**params).fit(X, y)
    # Predict target height
    th = round(model.predict(predict_child)[0],2)
    return th
  
  
  target_height = target_height_prediction(predict_child)
  feet = target_height / 12
  feet = round(feet,5)
  feet_round = int(feet)
  inch = str(feet-int(feet))[1:]
  inch = int(round(float(inch) * 12,2))

  results_target_height ='<p style="font-family:Avenir,Helvetica Neue,sans-serif;">Your childs target height is: '  + '<b>'+str(feet_round) + '</b> feet and <b>' + str(inch) + '</b> inches. +/- <b>1</b> inch.</p>'
  st.write(results_target_height, unsafe_allow_html=True)


              


