# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("Cutomize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

#fruit_list = session.sql('select distinct fruit_name from smoothies.public.fruit_options')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')) 
#fruit_list = my_dataframe.select(col('FRUIT_NAME'), col('SEARCH_ON')) 
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=pd_df, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df['FRUIT_NAME'], 
    max_selections = 5)

customer_name = st.text_input("Name on smoothie:", "", max_chars=100)
st.write(f"The name on your smoothie will be {customer_name}")

if ingredients_list:
    ingredients_string = (' ').join(ingredients_list) + ' '
    st.text(ingredients_string)
    for fruit_chosen in ingredients_list:
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        st.subheader(f'{fruit_chosen} Nutrition Information:')
        if fruityvice_response:
            fv_df = st.dataframe(data=fruityvice_response.json()["nutritions"], use_container_width=True)
        else:
            st.write(f"No nutrition information available for {fruit_chosen}")

    if customer_name:
        submit_button = st.button('Submit Order')

        if submit_button:
            insert_stmt = f"insert into smoothies.public.orders (name_on_order, ingredients) values ('{customer_name}', '{ingredients_string}')"
            # st.write(insert_stmt)
            # st.stop
            session.sql(insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {customer_name}!', icon="✅")

