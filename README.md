# Dividend Arbitrage Program

## Overview

This repository contains a Python function for assessing the safety of dividend stocks and a detailed report on dividend arbitrage. The program helps investors identify safe dividend stocks and understand the concept of dividend arbitrage.

## What is Dividend Arbitrage?

Dividend arbitrage is a strategy where investors aim to profit from the difference in stock prices just before and after a company pays out dividends to its shareholders. By purchasing dividend stocks before the ex-dividend date (the last day to qualify for a dividend payment), investors can benefit from a dividend income. Subsequently, they can either hold or sell the stock to capitalize on the stock price adjustment that typically occurs after the ex-dividend date.

## Why Use This Program?

The Dividend Arbitrage Program simplifies the process of identifying dividend arbitrage opportunities and assessing the safety of potential investments. It helps investors:

- Identify stocks with upcoming ex-dividend dates.
- Assess the safety of dividend stocks using a customizable risk tolerance questionnaire.
- Calculate safety scores based on financial criteria.
- Obtain option metrics for safer stocks, including strike prices, option prices, historical volatility, and theoretical option prices.
- Make informed investment decisions.

## How to Use This Program?

### Prerequisites

Before you begin, make sure you have the following:

- Python 3.7 or higher installed on your system.
- Required Python libraries installed. You can install them using pip with the following command:

    ```bash
    pip install pandas requests yfinance scipy
    ```

### Step 1: Obtain the Code

1. Clone the GitHub repository containing the code:

    ```bash
    git clone https://github.com/oscarmalik/Dividend_Arbitrage_Strategy
    ```

2. Change your current directory to the repository:

    ```bash
    cd Dividend_Arbitrage_Strategy
    ```

### Step 2: Run the Program

1. Execute the Python script in your terminal or command prompt:

    ```bash
    python strategy.py
    ```

### Step 3: Follow the Program's Prompts

1. The program will prompt you for the number of days to consider for the ex-dividend date criteria. Enter a number and press Enter. If you provide an invalid input, the default value of 5 days will be used.

2. The program will present you with a risk tolerance questionnaire. Select the option that best represents your risk tolerance by entering the corresponding number (1 to 5). The program will use this information to tailor the safety assessment.

3. The program will then proceed to loop through S&P 500 stocks and calculate safety assessments and option metrics for each stock.

### Step 4: View the Printed Results

1. The program will print the results to the terminal. You'll see information about each stock, including its safety assessment and option metrics.

    Here's an example of what the printed results might look like:

    ```plaintext
    Stock: AAPL
    Safety Assessment: Safe
    Option Metrics:
      Option 1:
      Strike Price: 100
      Option Price (Market): 2.50
      Historical Volatility: 0.2002
      Theoretical Option Price: 2.45
      Percent Difference: -2.00%
      Days to Expiration: 21 days

      Option 2:
      Strike Price: 105
      Option Price (Market): 3.00
      Historical Volatility: 0.2002
      Theoretical Option Price: 2.95
      Percent Difference: -1.67%
      Days to Expiration: 21 days

    ... (results for other stocks) ...
    ```

2. The program will continue to provide results for each stock in the S&P 500. You can review the safety assessments and option metrics to make informed investment decisions based on your risk tolerance.

## Report

The repository includes a comprehensive report titled ["Dividend Arbitrage: Understanding Its Application and Calculating Its Risk"](https://github.com/oscarmalik/Dividend_Arbitrage_Strategy/blob/main/Dividend_Arbitrage_Project_Report.pdf). This report covers the importance of dividend arbitrage, its practical application, and a detailed explanation of the provided function. It also provides insights into the complexity of the method, risk assessment, and key statistics.

## Conclusion

Dividend arbitrage is a valuable strategy for investors seeking to maximize returns from dividend stocks while minimizing risks. By using this toolkit and the accompanying report, you can gain a deeper understanding of dividend arbitrage, make informed investment decisions, and enhance your financial goals.
