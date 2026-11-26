import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import datetime
import base64
import io

# Load and preprocess the data
# Use absolute path to ensure the file is found correctly
data_path = os.environ.get(
    'DATA_PATH',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'shopping_trends_updated.csv'),
)
df = pd.read_csv(data_path)
print(f"Loaded data from: {data_path}")

# Data preprocessing
def preprocess_data(df):
    # Convert categorical variables to appropriate types
    categorical_cols = ['Gender', 'Category', 'Location', 'Size', 'Color', 'Season', 
                        'Subscription Status', 'Shipping Type', 'Discount Applied', 
                        'Promo Code Used', 'Payment Method', 'Frequency of Purchases']
    
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    
    # Convert Yes/No columns to boolean
    bool_cols = ['Subscription Status', 'Discount Applied', 'Promo Code Used']
    for col in bool_cols:
        df[col] = df[col].map({'Yes': True, 'No': False})
    
    # Create age groups
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    return df

# Apply preprocessing
df = preprocess_data(df)

# Get current date and time for dashboard update timestamp
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Initialize the Dash app
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server
app.title = "Retail Analytics Dashboard"

# Define app layout
app.layout = html.Div([
    html.Div([
        html.H1("Retail Analytics Dashboard", className="dashboard-title"),
        html.P("Comprehensive analysis of shopping trends and customer behavior", className="dashboard-description"),
        html.Div([
            html.Span("Last updated: "),
            html.Span(current_datetime)
        ], className="update-time")
    ], className="header"),
    
    html.Div([
        html.Div([
            html.H3("Filters", className="filter-title"),
            html.Label("Select Category"),
            dcc.Dropdown(
                id="category-filter",
                options=[{"label": cat, "value": cat} for cat in sorted(df["Category"].unique())],
                value=None,
                multi=True,
                placeholder="All Categories"
            ),
            html.Label("Select Season"),
            dcc.Dropdown(
                id="season-filter",
                options=[{"label": season, "value": season} for season in sorted(df["Season"].unique())],
                value=None,
                multi=True,
                placeholder="All Seasons"
            ),
            html.Label("Age Group"),
            dcc.Dropdown(
                id="age-filter",
                options=[{"label": age, "value": age} for age in sorted(df["Age Group"].unique())],
                value=None,
                multi=True,
                placeholder="All Age Groups"
            ),
            html.Label("Gender"),
            dcc.Dropdown(
                id="gender-filter",
                options=[{"label": gender, "value": gender} for gender in sorted(df["Gender"].unique())],
                value=None,
                multi=True,
                placeholder="All Genders"
            ),
            html.Div([
                html.Button("Reset Filters", id="reset-button", className="reset-button"),
                html.Button("Download Data", id="download-button", className="download-button"),
                dcc.Download(id="download-dataframe-csv"),
            ], className="filter-buttons")
        ], className="filter-panel"),
        
        html.Div([
            # Loading spinner for the entire dashboard content
            dcc.Loading(
                id="loading-dashboard",
                type="circle",
                children=[
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H4("Total Sales", className="card-title"),
                                html.Div(id="total-sales", className="card-value")
                            ], className="metric-card"),
                            html.Div([
                                html.H4("Average Purchase", className="card-title"),
                                html.Div(id="avg-purchase", className="card-value")
                            ], className="metric-card"),
                            html.Div([
                                html.H4("Total Customers", className="card-title"),
                                html.Div(id="total-customers", className="card-value")
                            ], className="metric-card"),
                            html.Div([
                                html.H4("Subscription Rate", className="card-title"),
                                html.Div(id="subscription-rate", className="card-value")
                            ], className="metric-card"),
                        ], className="metrics-container"),
                        
                        html.Div([
                            html.Div([
                                html.H3("Sales by Category", className="chart-title"),
                                dcc.Graph(id="category-sales")
                            ], className="chart-container"),
                            html.Div([
                                html.H3("Sales by Season", className="chart-title"),
                                dcc.Graph(id="season-sales")
                            ], className="chart-container"),
                        ], className="charts-row"),
                        
                        html.Div([
                            html.Div([
                                html.H3("Purchase Amount Distribution", className="chart-title"),
                                dcc.Graph(id="purchase-distribution")
                            ], className="chart-container"),
                            html.Div([
                                html.H3("Customer Demographics", className="chart-title"),
                                dcc.Graph(id="customer-demographics")
                            ], className="chart-container"),
                        ], className="charts-row"),
                        
                        html.Div([
                            html.Div([
                                html.H3("Popular Products by Age Group", className="chart-title"),
                                dcc.Graph(id="age-products")
                            ], className="chart-container"),
                            html.Div([
                                html.H3("Payment Method Analysis", className="chart-title"),
                                dcc.Graph(id="payment-analysis")
                            ], className="chart-container"),
                        ], className="charts-row"),
                        
                        html.Div([
                            html.H3("Purchase Frequency Analysis", className="chart-title"),
                            dcc.Graph(id="purchase-frequency")
                        ], className="full-chart-container"),
                        
                        html.Div([
                            html.H3("Geographic Distribution of Sales", className="chart-title"),
                            dcc.Graph(id="geo-distribution")
                        ], className="full-chart-container"),
                    ], id="dashboard-content")
                ]
            )
        ], className="dashboard-content")
    ], className="main-container"),
    
    # Footer
    html.Footer([
        html.Div([
            html.P("© 2023 Retail Analytics Dashboard. All rights reserved."),
            html.P(["Created with ", html.A("Dash", href="https://dash.plotly.com/", target="_blank"), " and ", 
                   html.A("Plotly", href="https://plotly.com/", target="_blank"), "."])
        ], className="footer-content")
    ], className="footer")
], className="app-container")

# Callback for reset button
@app.callback(
    [Output("category-filter", "value"),
     Output("season-filter", "value"),
     Output("age-filter", "value"),
     Output("gender-filter", "value")],
    [Input("reset-button", "n_clicks")],
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    return None, None, None, None

# Callback for download button
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("download-button", "n_clicks")],
    [State("category-filter", "value"),
     State("season-filter", "value"),
     State("age-filter", "value"),
     State("gender-filter", "value")],
    prevent_initial_call=True
)
def download_csv(n_clicks, categories, seasons, age_groups, genders):
    # Filter the dataframe based on selections
    filtered_df = df.copy()
    
    if categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(categories)]
    if seasons:
        filtered_df = filtered_df[filtered_df["Season"].isin(seasons)]
    if age_groups:
        filtered_df = filtered_df[filtered_df["Age Group"].isin(age_groups)]
    if genders:
        filtered_df = filtered_df[filtered_df["Gender"].isin(genders)]
    
    return dcc.send_data_frame(filtered_df.to_csv, "retail_data_export.csv", index=False)

# Define callback to update all charts based on filters
@app.callback(
    [
        Output("total-sales", "children"),
        Output("avg-purchase", "children"),
        Output("total-customers", "children"),
        Output("subscription-rate", "children"),
        Output("category-sales", "figure"),
        Output("season-sales", "figure"),
        Output("purchase-distribution", "figure"),
        Output("customer-demographics", "figure"),
        Output("age-products", "figure"),
        Output("payment-analysis", "figure"),
        Output("purchase-frequency", "figure"),
        Output("geo-distribution", "figure"),
        Output("dashboard-content", "style")
    ],
    [
        Input("category-filter", "value"),
        Input("season-filter", "value"),
        Input("age-filter", "value"),
        Input("gender-filter", "value"),
    ]
)
def update_charts(categories, seasons, age_groups, genders):
    # Filter the dataframe based on selections
    filtered_df = df.copy()
    
    if categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(categories)]
    if seasons:
        filtered_df = filtered_df[filtered_df["Season"].isin(seasons)]
    if age_groups:
        filtered_df = filtered_df[filtered_df["Age Group"].isin(age_groups)]
    if genders:
        filtered_df = filtered_df[filtered_df["Gender"].isin(genders)]
    
    # Calculate metrics
    total_sales = f"${filtered_df['Purchase Amount (USD)'].sum():,.2f}"
    avg_purchase = f"${filtered_df['Purchase Amount (USD)'].mean():,.2f}"
    total_customers = f"{filtered_df['Customer ID'].nunique():,}"
    subscription_rate = f"{(filtered_df['Subscription Status'].mean() * 100):.1f}%"
    
    # Create charts
    # 1. Sales by Category
    category_sales_fig = px.bar(
        filtered_df.groupby("Category")["Purchase Amount (USD)"].sum().reset_index(),
        x="Category",
        y="Purchase Amount (USD)",
        color="Category",
        title="Total Sales by Product Category"
    )
    category_sales_fig.update_layout(xaxis_title="Category", yaxis_title="Sales (USD)")
    
    # 2. Sales by Season
    season_sales_fig = px.pie(
        filtered_df.groupby("Season")["Purchase Amount (USD)"].sum().reset_index(),
        values="Purchase Amount (USD)",
        names="Season",
        hole=0.4,
        title="Sales Distribution by Season"
    )
    
    # 3. Purchase Amount Distribution
    purchase_dist_fig = px.histogram(
        filtered_df,
        x="Purchase Amount (USD)",
        nbins=20,
        title="Distribution of Purchase Amounts"
    )
    purchase_dist_fig.update_layout(xaxis_title="Purchase Amount (USD)", yaxis_title="Count")
    
    # 4. Customer Demographics
    demo_df = filtered_df.groupby(["Age Group", "Gender"])["Purchase Amount (USD)"].sum().reset_index()
    demo_fig = px.bar(
        demo_df,
        x="Age Group",
        y="Purchase Amount (USD)",
        color="Gender",
        barmode="group",
        title="Purchase Amount by Age Group and Gender"
    )
    demo_fig.update_layout(xaxis_title="Age Group", yaxis_title="Total Purchase Amount (USD)")
    
    # 5. Popular Products by Age Group
    age_products_df = filtered_df.groupby(["Age Group", "Item Purchased"])["Purchase Amount (USD)"].sum().reset_index()
    top_products_by_age = age_products_df.sort_values(["Age Group", "Purchase Amount (USD)"], ascending=[True, False])
    top_products_by_age = top_products_by_age.groupby("Age Group").head(5)
    
    age_products_fig = px.bar(
        top_products_by_age,
        x="Item Purchased",
        y="Purchase Amount (USD)",
        color="Age Group",
        facet_col="Age Group",
        facet_col_wrap=3,
        title="Top Products by Age Group"
    )
    age_products_fig.update_layout(xaxis_title="Product", yaxis_title="Sales (USD)")
    age_products_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    age_products_fig.update_xaxes(tickangle=45)
    
    # 6. Payment Method Analysis
    payment_df = filtered_df.groupby("Payment Method")["Purchase Amount (USD)"].agg(["sum", "count"]).reset_index()
    payment_df.columns = ["Payment Method", "Total Amount", "Transaction Count"]
    
    payment_fig = px.bar(
        payment_df,
        x="Payment Method",
        y="Total Amount",
        color="Transaction Count",
        title="Payment Method Analysis"
    )
    payment_fig.update_layout(xaxis_title="Payment Method", yaxis_title="Total Amount (USD)")
    
    # 7. Purchase Frequency Analysis
    freq_df = filtered_df.groupby("Frequency of Purchases")["Purchase Amount (USD)"].agg(["sum", "mean", "count"]).reset_index()
    freq_df.columns = ["Purchase Frequency", "Total Sales", "Average Purchase", "Customer Count"]
    
    # Create a custom order for frequency
    freq_order = ["Daily", "Weekly", "Bi-Weekly", "Fortnightly", "Monthly", "Quarterly", "Annually"]
    freq_df["Purchase Frequency"] = pd.Categorical(freq_df["Purchase Frequency"], categories=freq_order, ordered=True)
    freq_df = freq_df.sort_values("Purchase Frequency")
    
    freq_fig = go.Figure()
    freq_fig.add_trace(go.Bar(
        x=freq_df["Purchase Frequency"],
        y=freq_df["Total Sales"],
        name="Total Sales",
        marker_color="royalblue"
    ))
    freq_fig.add_trace(go.Scatter(
        x=freq_df["Purchase Frequency"],
        y=freq_df["Customer Count"],
        name="Customer Count",
        mode="lines+markers",
        yaxis="y2",
        marker_color="firebrick"
    ))
    freq_fig.update_layout(
        title="Purchase Frequency Analysis",
        xaxis_title="Purchase Frequency",
        yaxis_title="Total Sales (USD)",
        yaxis2=dict(
            title="Customer Count",
            overlaying="y",
            side="right"
        ),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255, 255, 255, 0.5)")
    )
    
    # 8. Geographic Distribution of Sales
    geo_df = filtered_df.groupby("Location")["Purchase Amount (USD)"].sum().reset_index()
    geo_fig = px.choropleth(
        geo_df,
        locations="Location",
        locationmode="USA-states",
        color="Purchase Amount (USD)",
        scope="usa",
        color_continuous_scale="Viridis",
        title="Sales Distribution by State"
    )
    
    # Set display style
    dashboard_style = {"display": "block"}
    
    return (
        total_sales,
        avg_purchase,
        total_customers,
        subscription_rate,
        category_sales_fig,
        season_sales_fig,
        purchase_dist_fig,
        demo_fig,
        age_products_fig,
        payment_fig,
        freq_fig,
        geo_fig,
        dashboard_style
    )

# Add CSS for styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Global Styles */
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
                color: #2c3e50;
            }
            
            .app-container {
                width: 100%;
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
            }
            
            /* Header Styles */
            .header {
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                color: white;
                padding: 20px 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                position: relative;
            }
            
            .dashboard-title {
                margin: 0;
                font-size: 2.2rem;
                font-weight: 700;
            }
            
            .dashboard-description {
                margin: 10px 0 0;
                font-size: 1.1rem;
                opacity: 0.9;
            }
            
            .update-time {
                position: absolute;
                top: 20px;
                right: 30px;
                font-size: 0.9rem;
                opacity: 0.8;
            }
            
            /* Main Container */
            .main-container {
                display: flex;
                gap: 20px;
            }
            
            /* Filter Panel */
            .filter-panel {
                flex: 0 0 250px;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                height: fit-content;
            }
            
            .filter-title {
                margin-top: 0;
                margin-bottom: 20px;
                font-size: 1.3rem;
                color: #2c3e50;
                border-bottom: 2px solid #e0e6ed;
                padding-bottom: 10px;
            }
            
            .filter-panel label {
                display: block;
                margin: 15px 0 5px;
                font-weight: 600;
                color: #4a5568;
            }
            
            .filter-buttons {
                margin-top: 25px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            .reset-button, .download-button {
                padding: 8px 12px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: 600;
                transition: background-color 0.3s;
            }
            
            .reset-button {
                background-color: #e53e3e;
                color: white;
            }
            
            .download-button {
                background-color: #38a169;
                color: white;
            }
            
            .reset-button:hover {
                background-color: #c53030;
            }
            
            .download-button:hover {
                background-color: #2f855a;
            }
            
            /* Dashboard Content */
            .dashboard-content {
                flex: 1;
            }
            
            /* Metrics Container */
            .metrics-container {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .metric-card {
                flex: 1;
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                text-align: center;
            }
            
            .card-title {
                margin: 0 0 10px;
                font-size: 0.9rem;
                color: #718096;
                font-weight: 600;
            }
            
            .card-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #2c3e50;
            }
            
            /* Charts */
            .charts-row {
                display: flex;
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .chart-container {
                flex: 1;
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .full-chart-container {
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
            }
            
            .chart-title {
                margin: 0 0 15px;
                font-size: 1.1rem;
                color: #2d3748;
                font-weight: 600;
            }
            
            /* Footer */
            .footer {
                margin-top: 30px;
                padding: 20px;
                background-color: #2c3e50;
                color: white;
                border-radius: 10px;
                text-align: center;
            }
            
            .footer-content p {
                margin: 5px 0;
            }
            
            .footer-content a {
                color: #90cdf4;
                text-decoration: none;
            }
            
            .footer-content a:hover {
                text-decoration: underline;
            }
            
            /* Responsive Design */
            @media (max-width: 1200px) {
                .main-container {
                    flex-direction: column;
                }
                
                .filter-panel {
                    flex: none;
                    width: auto;
                }
                
                .charts-row {
                    flex-direction: column;
                }
                
                .update-time {
                    position: static;
                    display: block;
                    margin-top: 10px;
                }
            }
            
            @media (max-width: 768px) {
                .metrics-container {
                    flex-wrap: wrap;
                }
                
                .metric-card {
                    flex: 0 0 calc(50% - 10px);
                }
                
                .filter-buttons {
                    flex-direction: row;
                }
                
                .reset-button, .download-button {
                    flex: 1;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)