import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('stock_snapshot.csv')
st.title("📈 Stock Metrics Dashboard")

all_companies = df['Company'].tolist()
select_all = st.checkbox("Select All Companies")
if select_all:
    selected = all_companies
else:
    selected = st.multiselect("Choose Companies", all_companies)
filtered = df[df['Company'].isin(selected)]

# Show data
st.dataframe(filtered)

# PE Ratio Bar Chart
st.subheader("📊 PE Ratio Comparison")
st.bar_chart(filtered.set_index('Company')['PE Ratio'])

# ROE Heatmap (requires seaborn)
import seaborn as sns
import matplotlib.pyplot as plt

st.subheader("🧠 ROE Heatmap")
fig, ax = plt.subplots()
sns.heatmap(filtered[['ROE']].set_index(filtered['Company']), annot=True, cmap='Greens', ax=ax)
st.pyplot(fig)