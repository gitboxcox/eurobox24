import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Hard-coded data
data1 = np.random.randn(100)
data2 = np.random.rand(100)

# Title for your app
st.title('Simple Streamlit Demo with Graph')

# Dropdown menu for dataset selection
option = st.selectbox(
    'Which dataset would you like to visualize?',
    ('Dataset 1', 'Dataset 2'))

# Plot based on selection
if option == 'Dataset 1':
    fig, ax = plt.subplots()
    ax.hist(data1, bins=20, alpha=0.5, color='blue')
    ax.set_title('Histogram of Dataset 1')
    st.pyplot(fig)
else:
    fig, ax = plt.subplots()
    ax.hist(data2, bins=20, alpha=0.5, color='green')
    ax.set_title('Histogram of Dataset 2')
    st.pyplot(fig)
