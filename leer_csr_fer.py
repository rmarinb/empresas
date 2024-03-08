import pandas as pd;

df = pd.DataFrame();

df = pd.read_csv('data/clientes.csv', sep=';');

df.to_excel('data/text.xlsx')

print(df);