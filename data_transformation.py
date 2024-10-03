# Import libraries and packages
import pandas as pd

# Load the first data file
store = pd.read_csv('pedido_loja.csv', sep=';')

# Load the second data file
store2 = pd.read_csv('pedido_loja2.csv', sep=';')

# Generate the first dataframe by combining both files
orders = pd.concat([store, store2], ignore_index=True)

# Format the data for consistency
orders['Total dos Produtos'] = orders['Total dos Produtos'].str.replace('.', '').str.replace(',', '.').astype(float)
orders['Valor total'] = orders['Valor total'].str.replace('.', '').str.replace(',', '.').astype(float)
orders['Desconto'] = orders['Desconto'].astype(str).replace('%', '', regex=True).astype(float)
orders['Número do pedido'] = orders['Número do pedido'].astype('str')
orders['Número do pedido multiloja'] = orders['Número do pedido multiloja'].astype('str')
orders['Número'] = orders['Número'].astype('str')
orders['Data'] = pd.to_datetime(orders['Data'], format="%d/%m/%Y")

# Load the third data file
shipping = pd.read_csv('frete.csv', sep=';')

# Load the fourth data file
shipping2 = pd.read_csv('frete2.csv', sep=';')

# Generate the second dataframe by combining both files
shippings = pd.concat([shipping, shipping2], ignore_index=True)

# Format the shipping data for consistency
shippings['Data'] = pd.to_datetime(shippings['Data'], format="%d/%m/%Y")
shippings['Número do pedido'] = shippings['Número do pedido'].astype('str')
shippings['Frete'] = shippings['Frete'].str.replace('.', '').str.replace(',', '.').astype(float)
shippings['Valor previsto'] = shippings['Valor previsto'].str.replace('.', '').str.replace(',', '.').astype(float)
shippings['Total da Venda'] = shippings['Total da Venda'].str.replace('.', '').str.replace(',', '.').astype(float)

# Merge the shipping and orders dataframes
merged_data = pd.merge(shippings, orders, on='Número do pedido', how='outer')

# Filter for Shopify-specific data, creating a new dataframe
shopify_data = merged_data[merged_data['Nome da Loja'] == 'Shopify']

# Remove duplicate rows
shopify_data = shopify_data.drop_duplicates(subset=['Número do pedido'])

# Drop unnecessary columns
shopify_data = shopify_data.drop(columns=['Valor total', 
                                          'UF_y', 
                                          'Nome_y',
                                          'Nome da Loja',
                                          'Nome da plataforma',
                                          'Número',
                                          'Número do pedido multiloja',
                                          'Número da remessa',
                                          'Data_y',
                                          'Valor previsto'])

# Add new columns required by the new system that were not present in the retired system
shopify_data.loc[:, 'Imposto'] = 0
shopify_data.loc[:, 'Reembolso'] = 0
shopify_data.loc[:, 'Receita total'] = 0
shopify_data.loc[:, 'Receita Líquida'] = shopify_data['Total da Venda'] - shopify_data['Frete']

# Reorder columns to meet the requirements of the new system
shopify_data = shopify_data[['Data_x', 
                             'Nome_x', 
                             'UF_x', 
                             'Número do pedido', 
                             'Total da Venda', 
                             'Frete', 
                             'Imposto', 
                             'Desconto', 
                             'Total dos Produtos',
                             'Reembolso', 
                             'Receita total', 
                             'Receita Líquida']]

# Drop rows with missing data
shopify_data = shopify_data.dropna()

# Generate a '.csv' file for loading into the new system
shopify_data.to_csv('shopify_history.csv', index=False)
