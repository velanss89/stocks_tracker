import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('stock_snapshot.csv')
# Add percent difference column
if 'Market Price (₹)' in df.columns and 'Fair Value' in df.columns:
    df['% Diff Market vs Fair'] = ((df['Market Price (₹)'] - df['Fair Value']) / df['Fair Value'] * 100).round(2)

st.title("📈 Stock Metrics Dashboard")

all_companies = df['Company'].tolist()
select_all = st.checkbox("Select All Companies")

# Category filter checkboxes
show_undervalued = st.checkbox("Show Undervalued")
show_overvalued = st.checkbox("Show Overvalued")
show_fairvalued = st.checkbox("Show Fairly Priced")

selected_categories = []
if show_undervalued:
    selected_categories.append('Undervalued')
if show_overvalued:
    selected_categories.append('Overvalued')
if show_fairvalued:
    selected_categories.append('Fairly Priced')

if select_all:
    selected = all_companies
else:
    selected = st.multiselect("Choose Companies", all_companies)

filtered = df[df['Company'].isin(selected)]
if selected_categories:
    filtered = filtered[filtered['Category'].isin(selected_categories)]

# Show data
st.dataframe(filtered[['Company', 'Market Price (₹)', 'Fair Value', 'Category', '% Diff Market vs Fair', 'PE Ratio', 'Market Cap', 'ROE', 'Dividend Yield']])

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