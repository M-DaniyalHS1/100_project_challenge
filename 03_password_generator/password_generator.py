import random
import string
import streamlit as st
# imported  modules
 
def generate_password(length,use_digit,use_special): #definig function
    characters = string.ascii_letters     # defining character variable

    if use_digit:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    return ''.join(random.choice(characters) for _ in range(length))


st.title("Password Generator")
length = st.slider("select length for password",min_value=8,max_value = 25,value = 12)
use_digit = st.checkbox("Include digits")
use_special = st.checkbox("Include punctuation")
if st.button("Genrate Password"):
    password = generate_password(length,use_digit,use_special)
    st.write(f"Generated Password: {password}")

st.write("-------------------------------------")