
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Simulate Data
def generate_data():
    np.random.seed(42)
    months = pd.date_range(start='2023-01-01', periods=12, freq='M')
    customers = [f"Customer {i}" for i in range(1, 11)]

    data = []
    for month in months:
        for customer in customers:
            invoice_amount = np.random.randint(500, 3000)
            payment = invoice_amount * np.random.uniform(0.5, 1.0)
            data.append({
                'Date': month,
                'Customer': customer,
                'Invoice Amount': round(invoice_amount, 2),
                'Cash Payment': round(payment, 2)
            })

    return pd.DataFrame(data)

# Load Data
df = generate_data()

# Sidebar Filters
st.sidebar.header("Filters")
selected_customer = st.sidebar.multiselect("Select Customers", options=df['Customer'].unique(), default=df['Customer'].unique())
df_filtered = df[df['Customer'].isin(selected_customer)]

st.title("📊 Financial Dashboard")

# KPI Row
st.subheader("Key Metrics")
total_invoice = df_filtered['Invoice Amount'].sum()
total_cash = df_filtered['Cash Payment'].sum()
st.metric("Total Invoiced", f"${total_invoice:,.2f}")
st.metric("Total Cash Received", f"${total_cash:,.2f}")

# Charts
st.subheader("Invoice Amount Over Time")
invoice_time = df_filtered.groupby('Date')['Invoice Amount'].sum().reset_index()
fig1 = px.line(invoice_time, x='Date', y='Invoice Amount', title='Monthly Invoice Amount')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Cash Payments Over Time")
payment_time = df_filtered.groupby('Date')['Cash Payment'].sum().reset_index()
fig2 = px.bar(payment_time, x='Date', y='Cash Payment', title='Monthly Cash Payments')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top 5 Customers by Invoice Amount")
top_customers = df_filtered.groupby('Customer')['Invoice Amount'].sum().nlargest(5).reset_index()
fig3 = px.pie(top_customers, names='Customer', values='Invoice Amount', title='Top Customers')
st.plotly_chart(fig3, use_container_width=True)

# Data Table
st.subheader("Customer Details Table")
st.dataframe(df_filtered.sort_values(by='Date', ascending=False).reset_index(drop=True))
