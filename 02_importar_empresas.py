
# Importamos las empresas desde el csv a la bbdd de empresas, tabla GE_EMPRESAS 

import 	pandas as pd
import  MySQLdb
from    sqlalchemy import create_engine
from 	datetime import datetime
import 	mysql.connector

# Funcion que da de alta la empresa que recibe por parámetro
def f_alta_empresa(cif, nombre, convenio, fechaconvenio, web):
		f.write('06 - Vamos a insertar la empresa:  ' + cif + '\n')
		f.write('06 - Vamos a insertar la empresa con nombre:  ' + nombre + '\n')
		print("06 - Vamos a insertar los datos de la empresa: ", nombre)
		
		curinsert = conn.cursor()

		if (fechaconvenio==0):
			fechaconvenio= datetime.now()

		sql = "INSERT INTO ge_empresas (cif, empresa, observaciones, convenio, fechaconvenio, web) VALUES (%s, %s, %s, %s, %s, %s)"
		val = (cif, nombre, "** PRUEBAS **", convenio, fechaconvenio, web)
		curinsert.execute(sql, val)
		conn.commit()

		print("06 - Registro insertado con la empresa: " , nombre)
		f.write('06 - El registro ha sido insertado correctamente '+ nombre + '************ \n')


# 00 - Generamos el archivo de salida para llevar registro del LOG: archivo-salida.py
f = open ('data/log_salida.txt','w')
f.write('****** EMPEZAMOS CON LAS EMPRESAS '+ '\n')

# 01 - Cogemos los datos de las empresas y los pasamos a un excel 
df_empresa = pd.DataFrame()
df_empresa = pd.read_csv('data/empresas_copy.csv', sep=';')

df_empresa = df_empresa.fillna(0)
df_empresa.to_excel('data/excel_empresas_copy.xlsx')

# 02 - Conectamos a la BBDD 
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='empresas'
)
cursor = conn.cursor()

# 03 - Recorremos el dataframe de las empresas y realizamos la comprobación de existencia de empresa en la tabla 
for i in range(len(df_empresa)):

	cifempresa 		= df_empresa.iloc[i]['cif']  
	nombreempresa 	= df_empresa.iloc[i]['nombre'] 
	  
	print("03 - ************************************************* DATOS DE LA EMPRESA ******** " ,  nombreempresa ,  cifempresa )
	f.write("03 - ************************************************* DATOS DE LA EMPRESA ******** " +  nombreempresa + " - " + str(cifempresa) + "\n" )

	if cifempresa is None or  cifempresa == 0:
		print("03 - No tiene CIF, vamos a trabajar con su nombre" , nombreempresa)		
		f.write("03 -  No tiene CIF, vamos a trabajar con su nombre: " +  nombreempresa + "\n" )
		
		# 03a - Miramos si existe o no en la bbdd po nombre
		cursor.execute("SELECT CAST(idempresa as char) FROM ge_empresas WHERE empresa like %s", ("%" + nombreempresa+ "%",))

		resultados = cursor.fetchall()
		for resultado in resultados:
			print('03a - La empresa ya existe en la base de datos. NO INSERTAMOS. ID_EMPRESA: ****************** ', resultado[0])
			f.write('03a - La empresa ya existe en la base de datos. NO INSERTAMOS. ID_EMPRESA:  ****************** ' + resultado[0])
		
		# 03b - Si no existe registro en la tabla, lo tendremos que dar de alta 
		if len(resultados)==0:
			f_alta_empresa('0', nombreempresa, df_empresa.iloc[i]['convenio'] , df_empresa.iloc[i]['conveniofecha'] , df_empresa.iloc[i]['web'] )
	else:
		
		# 04 - Comprobamos si el CIF ya está metido en la BBDD o no: 
		print("04 - La variable no es nula y tiene el valor:", cifempresa)		
		f.write('04 - ********************** CIF:' +  cifempresa + '\n') 
		cursor.execute("SELECT CAST(idempresa as char) FROM ge_empresas WHERE cif= %s", (cifempresa,))
				
		# 05 - Obtener los datos de la empresa existente o no en la tabla
		resultados = cursor.fetchall()
		for resultado in resultados:			
			print('05 - La empresa ya existe en la base de datos. NO INSERTAMOS. IDEMPRESA: ****************** ', resultado[0])
			f.write('05 - La empresa ya existe en la base de datos. NO INSERTAMOS. IDEMPRESA:  ****************** ' + resultado[0])
		
		# 06 - Si no existe registro en la tabla, lo tendremos que dar de alta 
		if len(resultados)==0:
			f_alta_empresa(df_empresa.iloc['cif'], df_empresa.iloc['nombre'], df_empresa.iloc[i]['convenio'] , df_empresa.iloc[i]['conveniofecha'] , df_empresa.iloc[i]['web'] )
		

# 99 - Cerramos todo lo que quede abierto 
			
cursor.close()
conn.close()
f.close()

