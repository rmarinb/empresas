
# Importamos los contactos de las empresas

import 	pandas as pd
import  MySQLdb
from    sqlalchemy import create_engine
import 	mysql.connector

# 00 - Generamos el archivo de salida para llevar registro del LOG: archivo-salida.py
fc = open ('data/log_salida_contactos.txt','w')
fc.write('****** EMPEZAMOS CON LOS CONTACTOS '+ '\n')

# 01 - Cogemos los datos de los contactos y los pasamos a un excel 
df_contactos = pd.DataFrame()
df_contactos = pd.read_csv('data/contactos.csv', sep=';')

df_contactos = df_contactos.fillna(0)
df_contactos.to_excel('data/excel_contactos.xlsx')

"""

# 02 - Conectamos a la BBDD 
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='empresas'
)
cursor = conn.cursor()

# 03 - Recorremos el dataframe de los contactos y realizamos la comprobación de existencia del contacto en la tabla de ge_contactos
for i in range(len(df_contactos)):

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
			fe.write('Entrontrado:  ' + cifempresa + ' ' + nombreempresa + ' ' + resultado[0] + '\n')

		# 03b - Si no existe registro en la tabla, lo tendremos que dar de alta 
		if len(resultados)==0:
			
			if df_empresa.iloc[i]['apellidos'] != 0:
				nombrecompleto = nombreempresa + ' ' + df_empresa.iloc[i]['apellidos'] 
			else:
				nombrecompleto = nombreempresa

			if nombreempresa != df_empresa.iloc[i]['razonsocial']:
				nombrecompleto += ' ' + df_empresa.iloc[i]['razonsocial'] 
			
			idempresanew = f_alta_empresa('0', nombrecompleto, df_empresa.iloc[i]['convenio'] , df_empresa.iloc[i]['conveniofecha'] , df_empresa.iloc[i]['web'], df_empresa.iloc[i]['observaciones'], df_empresa.iloc[i]['interesadosbolsa'], df_empresa.iloc[i]['pdb'], df_empresa.iloc[i]['cliente'], df_empresa.iloc[i]['proveedor'])
			especialidad = f_dame_especialidad(df_empresa.iloc[i]['idespecialidad'])
			f_alta_domicilio(idempresanew, df_empresa.iloc[i]['domicilio'], df_empresa.iloc[i]['cp'], df_empresa.iloc[i]['provincia'], df_empresa.iloc[i]['municipio'], df_empresa.iloc[i]['telefono'], df_empresa.iloc[i]['email'], especialidad)
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
			fe.write('Entrontrado:  ' + cifempresa + ' ' + nombreempresa + ' ' + resultado[0] + '\n')

		# 06 - Si no existe registro en la tabla, lo tendremos que dar de alta 
		if len(resultados)==0:			
			if df_empresa.iloc[i]['apellidos'] != 0:
				nombrecompleto = nombreempresa + ' ' + df_empresa.iloc[i]['apellidos'] 
			else:
				nombrecompleto = nombreempresa

			if nombreempresa != df_empresa.iloc[i]['razonsocial']:
				nombrecompleto += ' ' + df_empresa.iloc[i]['razonsocial'] 

			idempresanew = f_alta_empresa(df_empresa.iloc['cif'], nombrecompleto, df_empresa.iloc[i]['convenio'] , df_empresa.iloc[i]['conveniofecha'] , df_empresa.iloc[i]['web'] , df_empresa.iloc[i]['observaciones'], df_empresa.iloc[i]['interesadosbolsa'], df_empresa.iloc[i]['pdb'], df_empresa.iloc[i]['cliente'], df_empresa.iloc[i]['proveedor'])
			especialidad = f_dame_especialidad(df_empresa.iloc[i]['idespecialidad'])
			f_alta_domicilio(idempresanew, df_empresa.iloc[i]['domicilio'], df_empresa.iloc[i]['cp'], df_empresa.iloc[i]['provincia'], df_empresa.iloc[i]['municipio'], df_empresa.iloc[i]['telefono'], df_empresa.iloc[i]['email'], especialidad)

# 99 - Cerramos todo lo que quede abierto 			
cursor.close()
conn.close()
"""
fc.close()
