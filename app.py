import streamlit as st
import pandas as pd
import numpy as np

# streamlit input box
# commission_percentage = st.slider('Select commission_percentage', 10.0, 30.0)
# order_value = st.slider('Select order_value', 100, 1000)
commission_percentage = st.number_input('Select Commission %', 10, 30, value=28)
basket_size = st.number_input('Select Basket Size', 100, 5000, value=1000)

l = np.linspace(0.1,0.5,41)
m = [(round(i, 2), round(j, 2)) for i in l for j in l]
df = pd.DataFrame(data=m, columns=['Discount %', 'FP Share'], dtype=float)
df['Commission Percentage'] = commission_percentage / 100
df['Basket Size'] = basket_size
df['Discount Amount'] = df['Discount %'] * df['Basket Size']
df['Customer Price'] = df['Basket Size'] - df['Discount Amount']
df['ICPO'] = df['FP Share'] * df['Discount Amount']
df['Commissionable Base'] = df['Basket Size'] - df['ICPO']
df['RPO'] = df['Commissionable Base'] * df['Commission Percentage']
df['ROI'] = df['RPO'] / df['ICPO']
df = df[(df.ROI > 1.99)]
df = df[['FP Share', 'Discount %', 'ICPO', 'RPO', 'ROI']].sort_values(by='ROI', ascending=False).reset_index(drop=True)
df = df.round(2)
df = df.loc[df.groupby('FP Share')['Discount %'].agg('idxmax')]
df = df.sort_values(by=['FP Share', 'Discount %'], ascending=[False, False]).reset_index(drop=True)

table = df.style.format({
    'Discount %': '{:,.0%}'.format,
    'FP Share': '{:,.0%}'.format,
    'ICPO': '{:,.2f}'.format,
    'RPO': '{:,.2f}'.format,
    'ROI': '{:,.2f}'.format
})

# color = '#f85a40'

# def highlight():
#     return [f'background-color: {color}']*len(df) if df['ICPO'] > 500 else [f'background-color: white']*len(df)

# table = 

# df['Discount %'] = df['Discount %'].s
st.table(table)