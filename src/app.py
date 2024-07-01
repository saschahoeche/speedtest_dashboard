import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("Speedtest Dashboard")

# Generating random data
np.random.seed(42)  # For reproducibility
dates = pd.date_range(start="2023-01-01", end="2023-01-31", freq="D")
download_speeds = np.random.uniform(low=20.0, high=100.0, size=len(dates))
upload_speeds = np.random.uniform(low=5.0, high=50.0, size=len(dates))

# Creating a DataFrame
data = pd.DataFrame(
    {
        "Date": dates,
        "Download Speed (Mbps)": download_speeds,
        "Upload Speed (Mbps)": upload_speeds,
    }
)

# Plotting
fig, ax = plt.subplots()
ax.plot(data["Date"], data["Download Speed (Mbps)"], label="Download Speed")
ax.plot(data["Date"], data["Upload Speed (Mbps)"], label="Upload Speed")
ax.set_xlabel("Date")
ax.set_ylabel("Speed (Mbps)")
ax.legend()
ax.set_title("Internet Speed Over Time")

# Displaying the plot
st.pyplot(fig)
