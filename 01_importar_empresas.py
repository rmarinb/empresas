import 	pandas as pd
import  MySQLdb
from    sqlalchemy import create_engine
import 	mysql.connector

#archivo-salida.py
f = open ('data/log_salida.txt','w')
f.write('******Empezamos con las empresas')

# Cogemos los datos de las empresas
df_empresa = pd.DataFrame()
df_empresa = pd.read_csv('data/empresas.csv', sep=';')
df_empresa.to_excel('data/excel_empresas.xlsx')

# Conectamos a la BBDD 
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='empresas'
)
cursor = conn.cursor()

# Recorremos el dataframe de las empresas y realizamos el algoritmo 
for i in range(len(df_empresa)):
	cifempresa 		= df_empresa.iloc[i]['cif']  
	nombreempresa 	= df_empresa.iloc[i]['nombre']   
	print("el cif es: ")
	print(cifempresa)
	print("el nombre es: ")
	print(nombreempresa)
	if cifempresa is None:
   		 print("La variable es nula.")
	else:
    	print("La variable no es nula y tiene el valor:", cifempresa)
		consulta="SELECT idempresa FROM ge_empresas WHERE cif  =%s"
		cursor.execute(consulta, (cifempresa,))

	# Obtener los resultados de la consulta
	resultados = cursor.fetchall()
	for resultado in resultados:
		print(resultado)

cursor.close()
conn.close()
f.close()

