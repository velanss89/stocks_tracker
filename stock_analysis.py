import yfinance as yf
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    filename='stock_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_companies(file_path='companies.csv'):
    """Loads company names and tickers from a CSV file."""
    try:
        companies_df = pd.read_csv(file_path)
        return dict(zip(companies_df['Company'], companies_df['Ticker']))
    except FileNotFoundError:
        logging.error(f"Error: {file_path} not found. Please ensure it exists.")
        return {}

def analyze_stock(name, ticker):
    """Fetches stock info and performs analysis for a single company."""
    try:
        info = yf.Ticker(ticker).info
        logging.info(f'Fetching info for {name} ({ticker})')
        logging.info(f"Info: {info}")

        market_price = info.get('currentPrice')
        fair_value = info.get('fairValue')

        # Realistic fair value calculation if not available
        if not fair_value:
            eps = info.get('trailingEps')
            sector_avg_pe = 20  # Default or configurable
            if eps:
                fair_value = eps * sector_avg_pe
            else:
                fair_value = None

        # Determine category
        if fair_value and market_price:
            if abs(market_price - fair_value) / fair_value < 0.05:
                category = 'Fairly Priced'
            elif market_price < fair_value:
                category = 'Undervalued'
            else:
                category = 'Overvalued'
        else:
            category = 'Unknown'

        return {
            'Company': name,
            'Market Price (₹)': market_price,
            'Fair Value': fair_value,
            'Category': category,
            'PE Ratio': info.get('trailingPE'),
            'Market Cap': info.get('marketCap'),
            'ROE': info.get('returnOnEquity'),
            'Dividend Yield': info.get('dividendYield')
        }
    except Exception as e:
        logging.error(f"Error analyzing {name} ({ticker}): {e}")
        return {
            'Company': name,
            'Market Price (₹)': None,
            'Fair Value': None,
            'Category': 'Error',
            'PE Ratio': None,
            'Market Cap': None,
            'ROE': None,
            'Dividend Yield': None
        }

def run_analysis(companies):
    """Runs the stock analysis for a given dictionary of companies."""
    data = []
    # Clear the log file before first write
    open('stock_analysis.log', 'w').close()
    for name, ticker in companies.items():
        stock_data = analyze_stock(name, ticker)
        data.append(stock_data)
    return pd.DataFrame(data)

def filter_stocks_by_category(df, category):
    """Filters the DataFrame by a specific stock category."""
    return df[df['Category'] == category]

def filter_stocks_by_criteria(df):
    """Filters stocks based on market price proximity to fair value and PE ratio."""
    filtered_df = df[(df['Fair Value'].notnull()) & (df['Market Price (₹)'].notnull())]
    filtered_df = filtered_df[
        (abs(filtered_df['Market Price (₹)'] - filtered_df['Fair Value']) / filtered_df['Fair Value'] <= 0.2) &
        (filtered_df['PE Ratio'].notnull()) & (filtered_df['PE Ratio'] <= 20)
    ]
    return filtered_df

if __name__ == '__main__':
    companies = load_companies()
    if companies:
        df = run_analysis(companies)
        df.to_csv('stock_snapshot.csv', index=False)

        print("\n--- All Stock Data ---")
        print(df[['Company', 'Market Price (₹)', 'Fair Value', 'PE Ratio', 'Category']])

        # Example usage of filters
        category_to_filter = 'Undervalued'
        category_df = filter_stocks_by_category(df, category_to_filter)
        print(f'\n--- Stocks in category: {category_to_filter} ---')
        print(category_df[['Company', 'Market Price (₹)', 'Fair Value', 'PE Ratio', 'Category']])

        filtered_by_criteria_df = filter_stocks_by_criteria(df)
        print('\n--- Stocks with Market Price within +/-20% of Fair Value and PE Ratio <= 20 ---')
        print(filtered_by_criteria_df[['Company', 'Market Price (₹)', 'Fair Value', 'PE Ratio', 'Category']])
    else:
        print("No companies loaded. Please check 'companies.csv'.")
