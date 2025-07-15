import yfinance as yf
import pandas as pd
import logging

companies_df = pd.read_csv('companies.csv')
companies = dict(zip(companies_df['Company'], companies_df['Ticker']))

data = []

for name, ticker in companies.items():
    info = yf.Ticker(ticker).info
    logging.basicConfig(
        filename='stock_analysis.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info(f'Fetching info for {name} ({ticker})')
    # Clear the log file before first write
    if name == list(companies.keys())[0]:
        open('stock_analysis.log', 'w').close()
    logging.info(f"Info: {info}")
    market_price = info.get('currentPrice')
    fair_value = info.get('fairValue')
    # Realistic fair value calculation if not available
    if not fair_value:
        eps = info.get('trailingEps')
        # You can set sector_avg_pe based on sector or use a default
        sector_avg_pe = 20
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
    data.append({
        'Company': name,
        'Market Price (₹)': market_price,
        'Fair Value': fair_value,
        'Category': category,
        'PE Ratio': info.get('trailingPE'),
        'Market Cap': info.get('marketCap'),
        'ROE': info.get('returnOnEquity'),
        'Dividend Yield': info.get('dividendYield')
    })

df = pd.DataFrame(data)
df.to_csv('stock_snapshot.csv', index=False)

# Option to filter by category
def filter_by_category(df, category):
    return df[df['Category'] == category]

# Example usage:
category_to_filter = 'Undervalued'  # Change to 'Overvalued', 'Fairly Priced', or 'Unknown' as needed
category_df = filter_by_category(df, category_to_filter)

print(f'Stocks in category: {category_to_filter}')
print(category_df[['Company', 'Market Price (₹)', 'Fair Value', 'PE Ratio', 'Category']])

# Filter stocks: Market Price within +/-20% of Fair Value and PE Ratio <= 20
filtered_df = df[(df['Fair Value'].notnull()) & (df['Market Price (₹)'].notnull())]
filtered_df = filtered_df[
    (abs(filtered_df['Market Price (₹)'] - filtered_df['Fair Value']) / filtered_df['Fair Value'] <= 0.2) &
    (filtered_df['PE Ratio'].notnull()) & (filtered_df['PE Ratio'] <= 20)
]

print('Stocks with Market Price within +/-20% of Fair Value and PE Ratio <= 20:')
print(filtered_df[['Company', 'Market Price (₹)', 'Fair Value', 'PE Ratio', 'Category']])