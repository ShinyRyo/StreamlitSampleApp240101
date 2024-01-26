import streamlit as st
st.write("Hello, Streamlit!")

number = st.slider('Select a number', 0, 100, 50)
st.write('Selected number is:', number)

import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
st.write(df)
