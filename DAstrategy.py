{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "b201a069",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Enter the number of days for the ex-dividend date criteria: 5\n",
      "Risk Tolerance Questionnaire:\n",
      "Please select the option that best represents your risk tolerance for investments.\n",
      "1. Very Conservative (Prefer low-risk)\n",
      "2. Conservative (Prefer low to moderate risk)\n",
      "3. Moderate (Willing to accept moderate risk)\n",
      "4. Aggressive (Comfortable with higher risk)\n",
      "5. Very Aggressive (Willing to accept significant risk)\n",
      "Enter the number corresponding to your risk tolerance: 3\n",
      "[*********************100%%**********************]  1 of 1 completed\n",
      "[*********************100%%**********************]  1 of 1 completed\n",
      "Stock: ABT\n",
      "Safety Assessment: Safe\n"
     ]
    },
    {
     "ename": "NameError",
     "evalue": "name 'current_stock_price' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m/var/folders/kt/61h89lsn4tdg5p23pzccqsrh0000gn/T/ipykernel_27083/2144191742.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m    231\u001b[0m                 \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mf\"Stock: {stock_ticker}\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    232\u001b[0m                 \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mf\"Safety Assessment: {safety_result}\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 233\u001b[0;31m                 \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mf\"Current Stock Price: {current_stock_price:.2f}\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    234\u001b[0m                 \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Option Metrics:\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    235\u001b[0m                 \u001b[0moption_metrics\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msort\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mkey\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mlambda\u001b[0m \u001b[0mx\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mx\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"percent_difference\"\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mreverse\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mNameError\u001b[0m: name 'current_stock_price' is not defined"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import requests\n",
    "import yfinance as yf\n",
    "from datetime import datetime, timedelta\n",
    "from scipy.stats import norm\n",
    "import math\n",
    "\n",
    "def get_sp500_tickers():\n",
    "    sp500_df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]\n",
    "    return sp500_df['Symbol'].tolist()\n",
    "\n",
    "def convert_to_date(timestamp_str):\n",
    "    if timestamp_str == 'N/A':\n",
    "        return None  # Return None if date is 'N/A'\n",
    "        \n",
    "    # Convert a timestamp string to a date (YYYY-MM-DD)\n",
    "    return pd.to_datetime(timestamp_str, unit='s')  # Assuming the timestamp is in seconds\n",
    "\n",
    "def is_within_next_n_days(date, n):\n",
    "    if date is None or date == 'N/A':\n",
    "        return False  # Not applicable if date is None or 'N/A'\n",
    "    \n",
    "    today = pd.Timestamp.now().date()\n",
    "    future_date = today + pd.Timedelta(days=n)\n",
    "    \n",
    "    return today <= date.date() <= future_date\n",
    "\n",
    "def get_dividend_data(stock_ticker):\n",
    "    try:\n",
    "        alpha_vantage_api_key = '23O4FTGRCJIRLAXR'  # My Alpha Vantage API key\n",
    "        alpha_vantage_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={stock_ticker}&apikey={alpha_vantage_api_key}'\n",
    "        response = requests.get(alpha_vantage_url)\n",
    "        data = response.json()\n",
    "        \n",
    "        if 'Monthly Adjusted Time Series' in data:\n",
    "            dividend_data = data['Monthly Adjusted Time Series']\n",
    "            return dividend_data\n",
    "    except Exception as e:\n",
    "        print(f\"Error fetching data for {stock_ticker} from Alpha Vantage: {e}\")\n",
    "    \n",
    "    return {}\n",
    "\n",
    "def assess_risk_tolerance():\n",
    "    print(\"Risk Tolerance Questionnaire:\")\n",
    "    print(\"Please select the option that best represents your risk tolerance for investments.\")\n",
    "    print(\"1. Very Conservative (Prefer low-risk)\")\n",
    "    print(\"2. Conservative (Prefer low to moderate risk)\")\n",
    "    print(\"3. Moderate (Willing to accept moderate risk)\")\n",
    "    print(\"4. Aggressive (Comfortable with higher risk)\")\n",
    "    print(\"5. Very Aggressive (Willing to accept significant risk)\")\n",
    "    \n",
    "    while True:\n",
    "        try:\n",
    "            user_choice = int(input(\"Enter the number corresponding to your risk tolerance: \"))\n",
    "            if 1 <= user_choice <= 5:\n",
    "                # Map user's choice to risk_tolerance_threshold\n",
    "                risk_tolerance_threshold_mapping = {1: 3.25, 2: 2.625, 3: 2.0, 4: 1.375, 5: 0.75}\n",
    "                risk_tolerance_threshold = risk_tolerance_threshold_mapping[user_choice]\n",
    "                return risk_tolerance_threshold\n",
    "            else:\n",
    "                print(\"Invalid choice. Please select a number between 1 and 5.\")\n",
    "        except ValueError:\n",
    "            print(\"Invalid input. Please enter a number between 1 and 5.\")\n",
    "\n",
    "def calculate_option_metrics(stock_symbol, desired_stock_price_increase):\n",
    "    try:\n",
    "        # Find the nearest expiration date that is at least 3 weeks away\n",
    "        current_date = datetime.now()\n",
    "        expiration_dates = yf.Ticker(stock_symbol).options\n",
    "        selected_expiration_date = None\n",
    "\n",
    "        for expiration_date in expiration_dates:\n",
    "            expiration_date = datetime.strptime(expiration_date, \"%Y-%m-%d\")\n",
    "            if (expiration_date - current_date).days >= 21:\n",
    "                selected_expiration_date = expiration_date\n",
    "                break\n",
    "\n",
    "        # Check if a suitable expiration date was found\n",
    "        if selected_expiration_date:\n",
    "            # Fetch stock data\n",
    "            stock = yf.Ticker(stock_symbol)\n",
    "            current_stock_price = stock.history(period=\"1d\")[\"Close\"][0]\n",
    "\n",
    "            # Fetch option chain data for the selected expiration date\n",
    "            option_chain = stock.option_chain(selected_expiration_date.strftime(\"%Y-%m-%d\"))\n",
    "\n",
    "            # Define the minimum desired stock price increase (5% higher)\n",
    "            desired_strike_price = current_stock_price * (1 + desired_stock_price_increase)\n",
    "            option_data = []\n",
    "\n",
    "            # Obtain the 10-year government bond rate and inflation rate\n",
    "            ten_year_bond_rate = 0.0478\n",
    "            inflation_rate = 0.0367\n",
    "            \n",
    "            # Calculate the risk-free interest rate\n",
    "            risk_free_rate = (1 + ten_year_bond_rate) / (1 + inflation_rate)\n",
    "\n",
    "            for index, row in option_chain.puts.iterrows():\n",
    "                strike_price = row[\"strike\"]\n",
    "                option_price = row[\"lastPrice\"]\n",
    "                days_to_expiration = (selected_expiration_date - current_date).days\n",
    "\n",
    "                # Check if the option is in-the-money and strike price is greater than or equal to the desired strike price\n",
    "                is_option_itm = strike_price >= desired_strike_price\n",
    "\n",
    "                if is_option_itm:\n",
    "                    # Calculate historical volatility from stock data (adjust the period as needed)\n",
    "                    historical_volatility = stock.history(period=\"60d\")[\"Close\"].pct_change().std() * math.sqrt(252)\n",
    "\n",
    "                    # Calculate d1 and d2 using the calculated risk-free rate\n",
    "                    T = days_to_expiration / 365\n",
    "                    r = math.log(risk_free_rate)\n",
    "                    d1 = (math.log(current_stock_price / strike_price) + (r + (historical_volatility ** 2) / 2) * T) / (\n",
    "                        historical_volatility * math.sqrt(T))\n",
    "                    d2 = d1 - historical_volatility * math.sqrt(T)\n",
    "\n",
    "                    # Calculate the theoretical option price\n",
    "                    theoretical_option_price = strike_price * math.exp(-r * T) * norm.cdf(-d2) - current_stock_price * norm.cdf(-d1)\n",
    "\n",
    "                    # Calculate percent difference\n",
    "                    percent_difference = (theoretical_option_price - option_price) / option_price * 100\n",
    "\n",
    "                    # Add option data to the list\n",
    "                    option_data.append({\n",
    "                        \"strike_price\": strike_price,\n",
    "                        \"option_price\": option_price,\n",
    "                        \"historical_volatility\": historical_volatility,\n",
    "                        \"theoretical_option_price\": theoretical_option_price,\n",
    "                        \"percent_difference\": percent_difference,\n",
    "                        \"days_to_expiration\": days_to_expiration\n",
    "                    })\n",
    "\n",
    "            # Sort option_data based on percent difference\n",
    "            option_data.sort(key=lambda x: x[\"percent_difference\"], reverse=True)\n",
    "\n",
    "            return option_data\n",
    "\n",
    "        else:\n",
    "            print(f\"No suitable expiration date found for {stock_symbol}.\")\n",
    "            return []\n",
    "\n",
    "    except Exception as e:\n",
    "        print(f\"Error calculating option metrics for {stock_symbol}: {e}\")\n",
    "        return []\n",
    "\n",
    "def calculate_dividend_arbitrage_safety(stock_ticker, risk_tolerance_threshold, num_days, market_return):\n",
    "    try:\n",
    "        # Fetch stock information\n",
    "        stock = yf.Ticker(stock_ticker)\n",
    "        ex_dividend_date_timestamp = stock.info.get('exDividendDate', 'N/A')\n",
    "        \n",
    "        # Convert the timestamp to a date, handling 'N/A'\n",
    "        ex_dividend_date = convert_to_date(ex_dividend_date_timestamp)\n",
    "        \n",
    "        # Check if the ex-dividend date is within the specified number of days\n",
    "        if is_within_next_n_days(ex_dividend_date, num_days):\n",
    "            # Convert ex_dividend_date to a consistent time zone (e.g., UTC)\n",
    "            ex_dividend_date = ex_dividend_date.tz_localize('America/New_York').tz_convert('UTC')\n",
    "            \n",
    "            # Fetch historical stock data from yfinance\n",
    "            start_date = ex_dividend_date - timedelta(days=10)  # Adjust the date range as needed\n",
    "            end_date = ex_dividend_date\n",
    "            stock_data = yf.download(stock_ticker, start=start_date, end=end_date)\n",
    "            \n",
    "            # Calculate safety score based on criteria\n",
    "            safety_score = 0\n",
    "            \n",
    "            # Criteria 1: Expected Return\n",
    "            dividend_data = yf.Ticker(stock_ticker).dividends\n",
    "            dividends_sorted = dividend_data.sort_index(ascending=False)  # Sort dividends in descending order by date\n",
    "            recent_dividend = dividends_sorted.iloc[0]  # Most recent dividend\n",
    "            dividend_before = dividends_sorted.iloc[1]  # Dividend before the most recent one\n",
    "            dividend_amount = recent_dividend + (recent_dividend - dividend_before)\n",
    "            # Check if dividend_amount is more or less than 15% of the most recent dividend amount\n",
    "            if abs(dividend_amount - recent_dividend) > 0.15 * recent_dividend:\n",
    "                dividend_amount = recent_dividend\n",
    "            current_stock_price = stock_data['Adj Close'].iloc[-1]\n",
    "            expected_return = (dividend_amount / current_stock_price) * 100\n",
    "            safety_score += expected_return\n",
    "            \n",
    "            # Criteria 2: Volatility\n",
    "            average_volume = stock_data['Volume'].mean()\n",
    "            market_ticker = 'SPY'  # S&P index ETF\n",
    "            market_data = yf.download(market_ticker, start=start_date, end=end_date)\n",
    "            market_volatility = market_data['Adj Close'].std()\n",
    "            # Calculate the average return for SPY over the past 3 months\n",
    "            average_spy_return = (market_data['Adj Close'] / market_data['Adj Close'].shift(1) - 1).mean()\n",
    "            expected_volatility = stock.info.get('beta', None) * (market_volatility / average_spy_return)\n",
    "            volatility_score = market_volatility / expected_volatility\n",
    "            safety_score += volatility_score\n",
    "            \n",
    "            # Criteria 3: Volume Check\n",
    "            volume_score = stock_data['Volume'].iloc[-1] / average_volume\n",
    "            safety_score += volume_score\n",
    "            \n",
    "            # Adjust the risk tolerance threshold as needed\n",
    "            days_risk = 1.1 ** num_days / 10\n",
    "            safety_score -= days_risk\n",
    "\n",
    "            # Check the overall safety\n",
    "            if safety_score >= risk_tolerance_threshold:\n",
    "                return \"Safe\"\n",
    "            else:\n",
    "                return \"Unsafe\"\n",
    "        else:\n",
    "            return \"Ex-dividend date is not within the specified number of days\"\n",
    "        \n",
    "    except Exception as e:\n",
    "        return f\"Error: {e}\"\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    # Get the list of S&P 500 stock tickers using the provided function.\n",
    "    sp500_stocks = get_sp500_tickers()\n",
    "\n",
    "    # Ask the user for the number of days for the ex-dividend date criteria.\n",
    "    try:\n",
    "        num_days = int(input(\"Enter the number of days for the ex-dividend date criteria: \"))\n",
    "    except ValueError:\n",
    "        print(\"Invalid input. Using default value of 5 days.\")\n",
    "        num_days = 5\n",
    "\n",
    "    # Calculate the average return for SPY over the past 3 months\n",
    "    market_ticker = 'SPY'  # S&P 500 ETF\n",
    "    three_months_ago = datetime.now() - timedelta(days=90)\n",
    "    market_data = yf.download(market_ticker, start=three_months_ago)\n",
    "    average_spy_return = (market_data['Adj Close'] / market_data['Adj Close'].shift(1) - 1).mean()\n",
    "\n",
    "    # Ask the user for the risk tolerance questionnaire\n",
    "    user_risk_tolerance = assess_risk_tolerance()\n",
    "\n",
    "    # Loop through the S&P 500 stocks and calculate safety for each\n",
    "    for stock_ticker in sp500_stocks:\n",
    "        safety_result = calculate_dividend_arbitrage_safety(stock_ticker, user_risk_tolerance, num_days, average_spy_return)\n",
    "        \n",
    "        if safety_result != \"Ex-dividend date is not within the specified number of days\":\n",
    "            option_metrics = calculate_option_metrics(stock_ticker, desired_stock_price_increase=0.05)\n",
    "            \n",
    "            if option_metrics:\n",
    "                print(f\"Stock: {stock_ticker}\")\n",
    "                print(f\"Safety Assessment: {safety_result}\")\n",
    "                print(\"Option Metrics:\")\n",
    "                option_metrics.sort(key=lambda x: x[\"percent_difference\"], reverse=True)\n",
    "                for i, data in enumerate(option_metrics[:3], start=1):\n",
    "                    print(f\"  Option {i}:\")\n",
    "                    print(f\"  Strike Price: {data['strike_price']}\")\n",
    "                    print(f\"  Option Price (Market): {data['option_price']}\")\n",
    "                    print(f\"  Historical Volatility: {data['historical_volatility']:.4f}\")\n",
    "                    print(f\"  Theoretical Option Price: {data['theoretical_option_price']:.2f}\")\n",
    "                    print(f\"  Percent Difference: {data['percent_difference']:.2f}%\")\n",
    "                    print(f\"  Days to Expiration: {data['days_to_expiration']} days\\n\")\n",
    "                print(\"=\" * 50)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d1f7824f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}