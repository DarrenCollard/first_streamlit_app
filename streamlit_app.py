import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


# New Section to display Fruityide Advice
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwifruit')
    #fruit_choice = streamlit.selectbox("What Fruit would you like information about?", list(my_fruit_list.index), index=1)
    if not fruit_choice:
        streamlit.error('please select a fruit to get information')
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        # convert .json info to data frame
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        # write your own comment - what does this do?
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
streamlit.write('The user entered ', fruit_choice)


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT FRUIT_NAME from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.text('Thanks for adding ' + add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
