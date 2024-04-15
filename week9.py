import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2
from utils.modeling import *



REMOTE_DATA = 'Vegetables_Pulses2023.csv'


load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KeyID'],
        secret_key=os.environ['B2_applicationkey'])


@st.cache_data
def get_data():
    # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df = b2.get_df(REMOTE_DATA)
    return df



# Read data from CSV file
df = get_data()

# Filter the data for Per capita availability of artichokes in the United States
subset_data = df[(df['EndUse'] == 'Per capita availability') & (df['Location'] == 'United States')]

# Plotting
fig=plt.figure(figsize=(10, 6))
plt.plot(subset_data['Decade'], subset_data['PublishValue'], marker='o', linestyle='-')
plt.title('Per Capita Availability of Artichokes in the United States by Decade')
plt.xlabel('Decade')
plt.ylabel('Per Capita Availability (Pounds)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

st.pyplot(fig)
st.dataframe(df.head(20))


