import streamlit as st
import pandas as pd
import time
from stock_analysis import run_analysis, load_companies, filter_stocks_by_category, filter_stocks_by_criteria

st.set_page_config(layout="wide")

st.title("Stock Analysis Dashboard")

# Load companies
companies = load_companies()

if not companies:
    st.error("Could not load companies. Please check the `companies.csv` file.")
else:
    st.sidebar.header("Controls")
    if st.sidebar.button("Run Stock Analysis"):
        with st.spinner("Running analysis..."):
            start_time = time.time()
            df = run_analysis(companies)
            end_time = time.time()
            elapsed_time = end_time - start_time
            st.session_state['stock_df'] = df
            st.session_state['elapsed_time'] = elapsed_time
            st.success(f"Analysis complete in {elapsed_time:.2f} seconds!")

    if 'stock_df' in st.session_state:
        df = st.session_state['stock_df']
        st.sidebar.header("Filters")

        # Category Filter
        categories = ['All'] + sorted(df['Category'].unique().tolist())
        selected_category = st.sidebar.selectbox("Filter by Category", categories)

        if selected_category != 'All':
            display_df = filter_stocks_by_category(df, selected_category)
        else:
            display_df = df

        # Criteria Filter
        if st.sidebar.checkbox("Show only stocks matching specific criteria"):
            display_df = filter_stocks_by_criteria(display_df)

        st.header("Stock Data")
        st.dataframe(display_df)

        st.header("Analysis Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Companies Analyzed", len(df))
        if 'elapsed_time' in st.session_state:
            col2.metric("Analysis Time", f"{st.session_state['elapsed_time']:.2f}s")

        if selected_category != 'All':
            st.metric(f"Companies in {selected_category}", len(display_df))

        # Download Button
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='filtered_stock_data.csv',
            mime='text/csv',
        )
