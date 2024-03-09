import pandas as pd;



# Cogemos los datos de las empresas
df_empresa = pd.DataFrame();
df_empresa = pd.read_csv('data/empresas.csv', sep=';');
# df_empresa.to_excel('data/text_empresas.xlsx')

#for col in df_empresa:
#	print(df_empresa[col])

# Recorremos el dataframe de las empresas 
for indice_fila, fila in df_empresa.iterrows():
	print(indice_fila)
	print(fila)


