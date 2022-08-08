import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text('🥣 Omega 3 and Blueberry Oat Meal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-boiled Free Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_dice(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice) 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list():
  with my_cnx_cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input("What fruit do you like info about?")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    backfromfunction = get_fruityvice_dice(fruit_choice)
    streamlit.dataframe(backfromfunction)
except URLError as e:
    streamlit.error()


if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

streamlit.header("Fruit Load List Contains:")


fruit_choice = streamlit.text_input("What fruit would you like to add?")
streamlit.write('Thanks for adding ',fruit_choice)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
