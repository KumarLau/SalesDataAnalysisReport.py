import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'sales_uk.csv'  # Adjust if necessary
df = pd.read_csv(file_path)

# Streamlit app title
st.title("Interactive Sales Data Visualization Dashboard")

# Sidebar for chart selection
st.sidebar.header("Select Visualization Options")
chart_type = st.sidebar.selectbox("Select Chart Type:", ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Distribution Plot'])

# Sidebar for columns selection
columns = df.columns.tolist()
x_axis = st.sidebar.selectbox("X-Axis:", columns)
y_axis = st.sidebar.selectbox("Y-Axis (optional):", [None] + columns)

# Sidebar for sorting options
st.sidebar.header("Sorting Options")
sort_order = st.sidebar.radio("Sort by X-Axis Order:", ['Ascending', 'Descending'])
is_ascending = True if sort_order == 'Ascending' else False

# Sidebar for filtering by categorical columns (e.g., Branch, Product line, Customer type)
st.sidebar.header("Filter Data")
branch_filter = st.sidebar.multiselect('Branch:', options=df['Branch'].unique(), default=df['Branch'].unique())
df_filtered = df[df['Branch'].isin(branch_filter)]

# Sort the dataframe based on the x-axis selection
df_filtered = df_filtered.sort_values(by=x_axis, ascending=is_ascending)

# Debugging: Check if data is being filtered and sorted correctly
st.write("Filtered and Sorted Data Sample:")
st.write(df_filtered.head())

# Chart rendering logic
st.subheader(f"{chart_type} of {x_axis}" + (f" and {y_axis}" if y_axis else ""))

# Initialize the plot using context management to avoid stale state
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the selected chart
if chart_type == 'Bar Chart':
    if y_axis:
        sns.barplot(data=df_filtered, x=x_axis, y=y_axis, ax=ax)
    else:
        st.error("Bar Chart requires both X and Y axes to be selected.")
elif chart_type == 'Line Chart':
    if y_axis:
        sns.lineplot(data=df_filtered, x=x_axis, y=y_axis, ax=ax)
    else:
        st.error("Line Chart requires both X and Y axes to be selected.")
elif chart_type == 'Scatter Plot':
    if y_axis:
        sns.scatterplot(data=df_filtered, x=x_axis, y=y_axis, ax=ax)
    else:
        st.error("Scatter Plot requires both X and Y axes to be selected.")
elif chart_type == 'Distribution Plot':
    sns.histplot(df_filtered[x_axis], kde=True, ax=ax)

# Display the chart in Streamlit
st.pyplot(fig)

# Show data table
st.subheader("Filtered and Sorted Data")
st.dataframe(df_filtered)
