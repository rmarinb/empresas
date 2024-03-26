
# Importamos los contactos de las empresas

import 	pandas as pd
import  MySQLdb
from    sqlalchemy import create_engine
import 	mysql.connector
import	02_importar_empresas 

def	f_alta_contactos(domicilio, telefono1, telefono2, departamento, cargo, nombre, dni, especialidad):
	
	if telefono1 !=0:
		telefono = telefono1
	else:
		telefono = ' ' 
	if telefono2 !=0:
		telefono += telefono2
	if departamento !=0:
		departament = departamento
	else:
		departament = ' '
	if cargo !=0:
		carg = cargo
	else:
		carg = ' ' 
	if nombre !=0:
		nombr = nombre
	else:
		nombr = ' '
	if dni !=0:
		dn = dni
	else:
		dn = ' ' 
	if especialidad !=0:
		especialida = f_dame_especialidad(especialidad)
	else:
		especialida = ' '

	"""
	f.write('06 - Vamos a insertar la empresa:  ' + cif + '\n')
		f.write('06 - Vamos a insertar la empresa con nombre:  ' + nombre + '\n')
		print("06 - Vamos a insertar los datos de la empresa: ", nombre)
		
		curinsert = conn.cursor()

		if (fechaconvenio==0):
			fechaconvenio= datetime.now()

		if (web == 0.0):
			web = ' '

		if (convenio == 0.0):
			convenio = 0

		idempresanew = f_dame_id_empresa()

		sql = "INSERT INTO ge_empresas (idempresa, cif, empresa, observaciones, convenio, fechaconvenio, web, interesadobolsa, pdb, cliente, proveedor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		val = (idempresanew, cif, nombre, observaciones, convenio, fechaconvenio, web, interesados, pdb, cliente, proveedor)
		curinsert.execute(sql, val)
		conn.commit()

		print("06 - Registro insertado con la empresa: " , nombre)
		f.write('06 - El registro ha sido insertado correctamente '+ nombre + '************ \n')
		fi.write('Insertado:  ' + cif + ' ' + nombre + '\n')
		curinsert.close()

		return idempresanew
	"""

def f_contactos(cliente, domicilio):

	# 00 - Generamos el archivo de salida para llevar registro del LOG: archivo-salida.py
	fc = open ('data/log_salida_contactos.txt','w')
	fc.write('00 - ****** EMPEZAMOS CON LOS CONTACTOS del cliente' + cliente +  '\n')
	print("00 - ****** EMPEZAMOS CON LOS CONTACTOS del cliente ", cliente)

	# 01 - Cogemos los datos de los contactos y los pasamos a un excel 
	df_contactos = pd.DataFrame()
	df_contactos = pd.read_csv('data/contactos.csv', sep=';')

	df_contactos = df_contactos.fillna(0)
	df_contactos.to_excel('data/excel_contactos.xlsx')

	# 02 - Conectamos a la BBDD 
	conn = mysql.connector.connect(
    	host='localhost',
    	user='root',
    	password='root',
    	database='empresas'
	)
	
	cursor = conn.cursor()

	# 03 - Buscamos los contactos que haya en el dataframe para el cliente pasado por parámetro
	df_filtered = df_contactos[df_contactos['idcliente']=cliente]]

	if df_filtered.count()==0:
		return
	
	fc.write('03 - Contactos del cliente: '+ cliente + ' son' + df_filtered.count())
	print("03 - ****** Número contactos del cliente  ", df_filtered.count())

	# 04 - Recorremos el listado de contactos filtrado 
	for i in range(len(df_filtered)):
		email = df_filtered.iloc[i]['email']

		if email != 0:
			# 05 - Comprobamos si existe el contacto en la bbdd por email
			fc.write('05 - Vamos a comprobar el email: '+ email)
			print("05 - Vamos a comprobar el email: ", email)		

			cursor.execute("SELECT CAST(idcontacto as char) FROM ge_contactos WHERE email like %s", ("%" + email + "%",))
			resultados = cursor.fetchall()
		
			# 05a - No existe el registro en la BBDD, lo tenemos que dar de alta 
			if len(resultados) == 0:
				fc.write('05a - No existe el email, lo damos de alta' )
				print("05a - No existe el email, lo damos de alta" )		
				f_alta_contacto(domicilio, df_filtered.iloc[i]['telefono1'], df_filtered.iloc[i]['telefono2'], df_filtered.iloc[i]['departamento'], df_filtered.iloc[i]['cargo'],df_filtered.iloc[i]['nombre'] ,email, df_filtered.iloc[i]['dni'], df_filtered.iloc[i]['idespecialidad'])

		# 06 - El email no está informado. Metemos el contacto si o si
		else:
			fc.write('04 - No tiene email, damos de alta el contacto' )
			print("04 - No tiene email, damos de alta el contacto" )						
			f_alta_contacto(domicilio, df_filtered.iloc[i]['telefono1'], df_filtered.iloc[i]['telefono2'], df_filtered.iloc[i]['departamento'], df_filtered.iloc[i]['cargo'],df_filtered.iloc[i]['nombre'] ,email, df_filtered.iloc[i]['dni'], df_filtered.iloc[i]['idespecialidad'])

		
# 99 - Cerramos todo lo que quede abierto 			
cursor.close()
conn.close()
fc.close()


