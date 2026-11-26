# Retail Analytics Dashboard

A comprehensive data analysis dashboard for retail business insights, built with Dash and Plotly.

## Overview

This dashboard analyzes shopping trends data to provide actionable business insights through interactive visualizations. It helps retail businesses understand customer behavior, product performance, and sales patterns.

## Features

- **Interactive Filtering**: Filter data by product category, season, age group, and gender
- **Key Performance Metrics**: Total sales, average purchase amount, customer count, and subscription rate
- **Sales Analysis**: Breakdown of sales by product category and season
- **Customer Demographics**: Analysis of purchasing patterns by age group and gender
- **Product Insights**: Popular products by different age segments
- **Payment Analysis**: Comparison of payment methods by volume and transaction count
- **Purchase Frequency**: Analysis of customer purchase frequency patterns
- **Geographic Distribution**: Visual map of sales distribution across US states

## Data Insights

This dashboard helps answer business questions such as:

- Which product categories generate the most revenue?
- How do sales vary by season?
- What are the demographic profiles of top customers?
- Which products are popular among different age groups?
- What payment methods are preferred by customers?
- How does purchase frequency affect sales volume?
- Which geographic regions drive the most sales?

## Setup and Installation

1. Clone this repository or navigate to the project directory
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Download the Kaggle "Shopping Trends" dataset and save it as `data/shopping_trends_updated.csv` (or point the `DATA_PATH` environment variable to it).

4. Run the dashboard:

```bash
python app.py
```

5. Open your browser and navigate to http://127.0.0.1:8050/

## Data Preprocessing

The dashboard performs several preprocessing steps on the raw data:

- Converts categorical variables to appropriate types
- Transforms Yes/No columns to boolean values
- Creates age group segments for demographic analysis

## Customization

You can customize the dashboard by:

- Modifying the color schemes in the chart definitions
- Adding additional filters or visualizations
- Changing the layout structure in the app.layout section
- Updating the CSS styles in the app.index_string section

## Requirements

- Python 3.7+
- Dash
- Plotly
- Pandas
- NumPy

## License

This project is open source and available for use in personal and commercial projects.