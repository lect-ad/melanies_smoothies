# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Cutomize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

#fruit_list = session.sql('select distinct fruit_name from smoothies.public.fruit_options')

my_dataframe = session.table("smoothies.public.fruit_options")
#st.dataframe(data=my_dataframe, use_container_width=True)

fruit_list = my_dataframe.select(col('FRUIT_NAME')) 

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list, 
    max_selections = 5)

customer_name = st.text_input("Name on smoothie:", "", max_chars=100)
st.write(f"The name on your smoothie will be {customer_name}")

if ingredients_list:
    ingredients_string = (', ').join(ingredients_list)
    st.text(ingredients_string)
    for fruit_chosen in ingredients_list:
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
        st.subheader(f'{fruit_chosen} Nutrition Information:'
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    if customer_name:
        submit_button = st.button('Submit Order')

        if submit_button:
            insert_stmt = f"insert into smoothies.public.orders (name_on_order, ingredients) values ('{customer_name}', '{ingredients_string}')"
            # st.write(insert_stmt)
            # st.stop
            session.sql(insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {customer_name}!', icon="✅")

