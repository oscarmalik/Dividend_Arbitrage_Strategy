import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta
from scipy.stats import norm
import math

def get_sp500_tickers():
    sp500_df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return sp500_df['Symbol'].tolist()

def convert_to_date(timestamp_str):
    if timestamp_str == 'N/A':
        return None  # Return None if date is 'N/A'
        
    # Convert a timestamp string to a date (YYYY-MM-DD)
    return pd.to_datetime(timestamp_str, unit='s')  # Assuming the timestamp is in seconds

def is_within_next_n_days(date, n):
    if date is None or date == 'N/A':
        return False  # Not applicable if date is None or 'N/A'
    
    today = pd.Timestamp.now().date()
    future_date = today + pd.Timedelta(days=n)
    
    return today <= date.date() <= future_date

def get_dividend_data(stock_ticker):
    try:
        alpha_vantage_api_key = '23O4FTGRCJIRLAXR'  # My Alpha Vantage API key
        alpha_vantage_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={stock_ticker}&apikey={alpha_vantage_api_key}'
        response = requests.get(alpha_vantage_url)
        data = response.json()
        
        if 'Monthly Adjusted Time Series' in data:
            dividend_data = data['Monthly Adjusted Time Series']
            return dividend_data
    except Exception as e:
        print(f"Error fetching data for {stock_ticker} from Alpha Vantage: {e}")
    
    return {}

def assess_risk_tolerance():
    print("Risk Tolerance Questionnaire:")
    print("Please select the option that best represents your risk tolerance for investments.")
    print("1. Very Conservative (Prefer low-risk)")
    print("2. Conservative (Prefer low to moderate risk)")
    print("3. Moderate (Willing to accept moderate risk)")
    print("4. Aggressive (Comfortable with higher risk)")
    print("5. Very Aggressive (Willing to accept significant risk)")
    
    while True:
        try:
            user_choice = int(input("Enter the number corresponding to your risk tolerance: "))
            if 1 <= user_choice <= 5:
                # Map user's choice to risk_tolerance_threshold
                risk_tolerance_threshold_mapping = {1: 3.25, 2: 2.625, 3: 2.0, 4: 1.375, 5: 0.75}
                risk_tolerance_threshold = risk_tolerance_threshold_mapping[user_choice]
                return risk_tolerance_threshold
            else:
                print("Invalid choice. Please select a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

def calculate_option_metrics(stock_symbol, desired_stock_price_increase):
    try:
        # Find the nearest expiration date that is at least 3 weeks away
        current_date = datetime.now()
        expiration_dates = yf.Ticker(stock_symbol).options
        selected_expiration_date = None

        for expiration_date in expiration_dates:
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            if (expiration_date - current_date).days >= 21:
                selected_expiration_date = expiration_date
                break

        # Check if a suitable expiration date was found
        if selected_expiration_date:
            # Fetch stock data
            stock = yf.Ticker(stock_symbol)
            current_stock_price = stock.history(period="1d")["Close"][0]

            # Fetch option chain data for the selected expiration date
            option_chain = stock.option_chain(selected_expiration_date.strftime("%Y-%m-%d"))

            # Define the minimum desired stock price increase (5% higher)
            desired_strike_price = current_stock_price * (1 + desired_stock_price_increase)
            option_data = []

            # Obtain the 10-year government bond rate and inflation rate
            ten_year_bond_rate = 0.0478
            inflation_rate = 0.0367
            
            # Calculate the risk-free interest rate
            risk_free_rate = (1 + ten_year_bond_rate) / (1 + inflation_rate)

            for index, row in option_chain.puts.iterrows():
                strike_price = row["strike"]
                option_price = row["lastPrice"]
                days_to_expiration = (selected_expiration_date - current_date).days

                # Check if the option is in-the-money and strike price is greater than or equal to the desired strike price
                is_option_itm = strike_price >= desired_strike_price

                if is_option_itm:
                    # Calculate historical volatility from stock data (adjust the period as needed)
                    historical_volatility = stock.history(period="60d")["Close"].pct_change().std() * math.sqrt(252)

                    # Calculate d1 and d2 using the calculated risk-free rate
                    T = days_to_expiration / 365
                    r = math.log(risk_free_rate)
                    d1 = (math.log(current_stock_price / strike_price) + (r + (historical_volatility ** 2) / 2) * T) / (
                        historical_volatility * math.sqrt(T))
                    d2 = d1 - historical_volatility * math.sqrt(T)

                    # Calculate the theoretical option price
                    theoretical_option_price = strike_price * math.exp(-r * T) * norm.cdf(-d2) - current_stock_price * norm.cdf(-d1)

                    # Calculate percent difference
                    percent_difference = (theoretical_option_price - option_price) / option_price * 100

                    # Add option data to the list
                    option_data.append({
                        "strike_price": strike_price,
                        "option_price": option_price,
                        "historical_volatility": historical_volatility,
                        "theoretical_option_price": theoretical_option_price,
                        "percent_difference": percent_difference,
                        "days_to_expiration": days_to_expiration
                    })

            # Sort option_data based on percent difference
            option_data.sort(key=lambda x: x["percent_difference"], reverse=True)

            return option_data

        else:
            print(f"No suitable expiration date found for {stock_symbol}.")
            return []

    except Exception as e:
        print(f"Error calculating option metrics for {stock_symbol}: {e}")
        return []

def calculate_dividend_arbitrage_safety(stock_ticker, risk_tolerance_threshold, num_days, market_return):
    try:
        # Fetch stock information
        stock = yf.Ticker(stock_ticker)
        ex_dividend_date_timestamp = stock.info.get('exDividendDate', 'N/A')
        
        # Convert the timestamp to a date, handling 'N/A'
        ex_dividend_date = convert_to_date(ex_dividend_date_timestamp)
        
        # Check if the ex-dividend date is within the specified number of days
        if is_within_next_n_days(ex_dividend_date, num_days):
            # Convert ex_dividend_date to a consistent time zone (e.g., UTC)
            ex_dividend_date = ex_dividend_date.tz_localize('America/New_York').tz_convert('UTC')
            
            # Fetch historical stock data from yfinance
            start_date = ex_dividend_date - timedelta(days=10)  # Adjust the date range as needed
            end_date = ex_dividend_date
            stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
            
            # Calculate safety score based on criteria
            safety_score = 0
            
            # Criteria 1: Expected Return
            dividend_data = yf.Ticker(stock_ticker).dividends
            dividends_sorted = dividend_data.sort_index(ascending=False)  # Sort dividends in descending order by date
            recent_dividend = dividends_sorted.iloc[0]  # Most recent dividend
            dividend_before = dividends_sorted.iloc[1]  # Dividend before the most recent one
            dividend_amount = recent_dividend + (recent_dividend - dividend_before)
            # Check if dividend_amount is more or less than 15% of the most recent dividend amount
            if abs(dividend_amount - recent_dividend) > 0.15 * recent_dividend:
                dividend_amount = recent_dividend
            current_stock_price = stock_data['Adj Close'].iloc[-1]
            expected_return = (dividend_amount / current_stock_price) * 100
            safety_score += expected_return
            
            # Criteria 2: Volatility
            average_volume = stock_data['Volume'].mean()
            market_ticker = 'SPY'  # S&P index ETF
            market_data = yf.download(market_ticker, start=start_date, end=end_date)
            market_volatility = market_data['Adj Close'].std()
            # Calculate the average return for SPY over the past 3 months
            average_spy_return = (market_data['Adj Close'] / market_data['Adj Close'].shift(1) - 1).mean()
            expected_volatility = stock.info.get('beta', None) * (market_volatility / average_spy_return)
            volatility_score = market_volatility / expected_volatility
            safety_score += volatility_score
            
            # Criteria 3: Volume Check
            volume_score = stock_data['Volume'].iloc[-1] / average_volume
            safety_score += volume_score
            
            # Adjust the risk tolerance threshold as needed
            days_risk = 1.1 ** num_days / 10
            safety_score -= days_risk

            # Check the overall safety
            if safety_score >= risk_tolerance_threshold:
                return "Safe"
            else:
                return "Unsafe"
        else:
            return "Ex-dividend date is not within the specified number of days"
        
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Get the list of S&P 500 stock tickers using the provided function.
    sp500_stocks = get_sp500_tickers()

    # Ask the user for the number of days for the ex-dividend date criteria.
    try:
        num_days = int(input("Enter the number of days for the ex-dividend date criteria: "))
    except ValueError:
        print("Invalid input. Using default value of 5 days.")
        num_days = 5

    # Calculate the average return for SPY over the past 3 months
    market_ticker = 'SPY'  # S&P 500 ETF
    three_months_ago = datetime.now() - timedelta(days=90)
    market_data = yf.download(market_ticker, start=three_months_ago)
    average_spy_return = (market_data['Adj Close'] / market_data['Adj Close'].shift(1) - 1).mean()

    # Ask the user for the risk tolerance questionnaire
    user_risk_tolerance = assess_risk_tolerance()

    # Loop through the S&P 500 stocks and calculate safety for each
    for stock_ticker in sp500_stocks:
        safety_result = calculate_dividend_arbitrage_safety(stock_ticker, user_risk_tolerance, num_days, average_spy_return)
        
        if safety_result != "Ex-dividend date is not within the specified number of days":
            option_metrics = calculate_option_metrics(stock_ticker, desired_stock_price_increase=0.05)
            
            if option_metrics:
                print(f"Stock: {stock_ticker}")
                print(f"Safety Assessment: {safety_result}")
                print("Option Metrics:")
                option_metrics.sort(key=lambda x: x["percent_difference"], reverse=True)
                for i, data in enumerate(option_metrics[:3], start=1):
                    print(f"  Option {i}:")
                    print(f"  Strike Price: {data['strike_price']}")
                    print(f"  Option Price (Market): {data['option_price']}")
                    print(f"  Historical Volatility: {data['historical_volatility']:.4f}")
                    print(f"  Theoretical Option Price: {data['theoretical_option_price']:.2f}")
                    print(f"  Percent Difference: {data['percent_difference']:.2f}%")
                    print(f"  Days to Expiration: {data['days_to_expiration']} days\n")
                print("=" * 50)