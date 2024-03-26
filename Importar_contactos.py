
# Importamos los contactos de las empresas

import 	pandas as pd
import  MySQLdb
from    sqlalchemy import create_engine
import 	mysql.connector

# Función que dada una idespecialidad, me retorne su codespecialidad  concatenado con ' FORM' 
def f_dame_especialidad(conn, idespecial):

	codigo = "FORM" 
	cursorespecial = conn.cursor()
	cursorespecial.execute("SELECT codespecialidad FROM especialidad WHERE idespecialidad = %s", (idespecial, ))
	resultados = cursorespecial.fetchall()

	for resultado in resultados:
		codigo += '/ ' + resultado[0] 	

	print('08 - La especialidad  ES: ', codigo)
	f.write('08 - La especialidad ES:' + codigo)
	cursorespecial.close()
	return codigo		

def f_update_contacto(fc, conn, contacto, especialidad):
	
	fc.write('07 - Vamos a actualizar el contacto:  ' + contacto +  '\n')
	print("07 - Vamos a actualizar el contacto: ", contacto)

	curupdate = conn.cursor()
	
	especialidad += ' / FORM'

	sql = "UPDATE ge_contactos SET especialidad = %s WHERE idcontacto = %s"
	val = (especialidad, contacto)
	
	curupdate.execute(sql, val)
	conn.commit()

	print("07 - Registro actualizado del contacto: " , contacto)
	fc.write('06 - Registro actualizado del contacto '+ contacto + '************ \n')

	curupdate.close()

def	f_alta_contacto(conn, fc, domicilio, telefono1, telefono2, departamento, cargo, nombre, dni, especialidad, email):
											
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
		especialida = f_dame_especialidad(conn, especialidad)
	else:
		especialida = ' '

	fc.write('06 - Vamos a insertar el contacto con los datos:  ' + nombr + ' ' + dn + ' ' + carg + ' ' + especialida +  '\n')
	print("06 - Vamos a insertar el contacto con los datos: ", nombr)

	curinsert = conn.cursor()
	
	sql = "INSERT INTO ge_contactos (iddomicilio, dni, nombre, email, telefono, cargo, observaciones, especialidad, departamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (domicilio, dn, nombr, email, telefono, carg, 'De escuela empresa', especialida, departament)
	
	curinsert.execute(sql, val)
	conn.commit()

	print("06 - Registro insertado con el contacto: " , nombr)
	fc.write('06 - Registro insertaco con el contacto '+ nombr + '************ \n')

	curinsert.close()

def f_contactos(cliente, domicilio):

	# 00 - Generamos el archivo de salida para llevar registro del LOG: archivo-salida.py
	fc = open ('data/log_salida_contactos.txt','w', encoding='utf-8')
	fc.write('00 - ****** EMPEZAMOS CON LOS CONTACTOS del cliente' + str(cliente) +  '\n')
	print("00 - ****** EMPEZAMOS CON LOS CONTACTOS del cliente ", str(cliente))

	# 01 - Cogemos los datos de los contactos y los pasamos a un excel 
	df_contactos = pd.DataFrame()
	df_contactos = pd.read_csv('data/contactos.csv', sep=';', encoding='utf-8')

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
	df_filtered = df_contactos.loc[df_contactos['idcliente']==cliente]

	if df_filtered.count().sum()==0:
		return
	
	fc.write('03 - Contactos del cliente: '+ str(cliente) + ' son' + str(df_filtered.count().sum()) + "\n")
	print("03 - ****** Número contactos del cliente  ", df_filtered.count().sum())

	# 04 - Recorremos el listado de contactos filtrado 
	for i in range(len(df_filtered)):
		email = df_filtered.iloc[i]['email']

		if email != 0:
			# 05 - Comprobamos si existe el contacto en la bbdd por email
			fc.write('05 - Vamos a comprobar el email: '+ email + "\n")
			print("05 - Vamos a comprobar el email: ", email)		

			cursor.execute("SELECT CAST(idcontacto as char), especialidad  FROM ge_contactos WHERE email like %s", ("%" + email + "%",))
			resultados = cursor.fetchall()
		
			# 05a - No existe el registro en la BBDD, lo tenemos que dar de alta 
			if len(resultados) == 0:
				fc.write('05a - No existe el email, lo damos de alta' )
				print("05a - No existe el email, lo damos de alta" )		
				f_alta_contacto(conn, fc, domicilio, df_filtered.iloc[i]['telefono1'], df_filtered.iloc[i]['telefono2'], df_filtered.iloc[i]['departamento'], df_filtered.iloc[i]['cargo'],df_filtered.iloc[i]['nombre'] , df_filtered.iloc[i]['dni'], df_filtered.iloc[i]['idespecialidad'], email)
			else:
				f_update_contacto(fc, conn, resultados[0], resultados[1])

		# 06 - El email no está informado. Metemos el contacto si o si
		else:
			fc.write('04 - No tiene email, damos de alta el contacto' + "\n")
			print("04 - No tiene email, damos de alta el contacto" )						
			f_alta_contacto(conn, fc, domicilio, df_filtered.iloc[i]['telefono1'], df_filtered.iloc[i]['telefono2'], df_filtered.iloc[i]['departamento'], df_filtered.iloc[i]['cargo'],df_filtered.iloc[i]['nombre'] ,df_filtered.iloc[i]['dni'], df_filtered.iloc[i]['idespecialidad'], email)
			
	fc.close()
	cursor.close()
	conn.close()






