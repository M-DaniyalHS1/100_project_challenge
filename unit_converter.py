import streamlit as st

def unit_converter(value,unit_from,unit_to):

    conversions = {
        "meters_kilometers" : 0.001,   # 1 meter - o.oo1 kilometer
        "kilometers_meters": 1000,  #1 kilometer = 1000 meter
        "grams_kilograms":0.001,     # 1 gram = 0.001 kilogram
        "kilograms_grams"  :1000  # 1 kilogram = 1000 gram
            }
  
    key = f"{unit_from}_{unit_to}"

    if key in conversions:
        conversion = conversions[key]
        return value *  conversion

    else:
        return "conversion not supported"
    

st.title("Unit Converter")
value = st.number_input("Enter the value")
unit_from = st.selectbox("convert from:",["meters","kilometers","grams","kilograms"])
unit_to = st.selectbox("convert to: ",["meters","kilometers","grams","kilograms"])

if st.button("Convert"):
    result = unit_converter(value,unit_from,unit_to)
    st.write("converted unit: ",result)


