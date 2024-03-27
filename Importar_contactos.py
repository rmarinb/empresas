
# Importamos los contactos de las empresas

import 	pandas as pd
import  MySQLdb
from    sqlalchemy import create_engine
import 	mysql.connector

# Función que dada una idespecialidad, me retorne su codespecialidad  concatenado con ' FORM' 
def f_dame_especialidad(fc, conn, idespecial):

	codigo = "FORM" 
	cursorespecial = conn.cursor()
	cursorespecial.execute("SELECT codespecialidad FROM especialidad WHERE idespecialidad = %s", (idespecial, ))
	resultados = cursorespecial.fetchall()

	for resultado in resultados:
		codigo = codigo +  ' / ' + str(resultado[0]) 	

	cursorespecial.close()
	return codigo		

def f_update_contacto(fc, conn, contacto, especialidad):
	
	fc.write('07 - Vamos a actualizar el contacto:  ' + str(contacto) +  '\n')
	print("07 - Vamos a actualizar el contacto: ", str(contacto))

	curupdate = conn.cursor()
	
	if len(especialidad) == 0:
		especialidad = 'FORM'
	else:
		especialidad += ' / FORM'

	sql = "UPDATE ge_contactos SET especialidad = %s WHERE idcontacto = %s"
	val = (especialidad, contacto)
	
	curupdate.execute(sql, val)
	conn.commit()

	print("07 - Registro actualizado del contacto: " , str(contacto))
	fc.write('07 - Registro actualizado del contacto '+ str(contacto) + '************ \n')

	curupdate.close()

def	f_alta_contacto(conn, fc, domicilio, telefono1, telefono2, departamento, cargo, nombre, dni, especialidad, email):

	fc.write('06 - Vamos a insertar el contacto con los datos:  ' + str(nombre) + ' ' + str(dni) + ' ' + str(cargo) + ' ' + str(especialidad) +  '\n')
	print("06 - Vamos a insertar el contacto con los datos: ", nombre)

	if domicilio == 0 or domicilio == None:
		fc.write('06 - El id de domicilio no está informado, no podemos insertar \n')
		print("06 - El id de domicilio no está informado, no podemos insertar. ")
		return -1 
	
	if email == 0:
		email =''

	if telefono1 !=0:
		telefono = telefono1
	else:
		telefono = ' ' 

	if telefono2 !=0:
		telefono = telefono + ' ' + telefono2

	departamento = str(departamento)[:45]

	if departamento != '0':
		departament = departamento
	else:
		departament = ' '

	if cargo !=0:
		carg = cargo
	else:
		carg = ' ' 

	carg = carg[:99]
	
	email = str(email)[:99]

	if nombre !=0:
		nombr = nombre
	else:
		nombr = ' '

	dni = str(dni)[:10]

	if dni !='0':
		dn = dni
	else:
		dn = ' ' 

	if str(especialidad) != '0':
		especialida = f_dame_especialidad(fc, conn, especialidad) + ' / FORM'
	else:
		especialida = 'FORM'
		
	curinsert = conn.cursor()
	
	telefono = str(telefono)[:49]

	sql = "INSERT INTO ge_contactos (iddomicilio, dni, nombre, email, telefono, cargo, observaciones, especialidad, departamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (domicilio, dn, str(nombr), email, str(telefono), str(carg), 'De escuela empresa', str(especialida), str(departament))
	
	curinsert.execute(sql, val)
	conn.commit()

	print("06 - Registro insertado con el contacto: " , nombr)
	fc.write('06 - Registro insertaco con el contacto '+ nombr + '************ \n')

	curinsert.close()

	return 1

def f_contactos(cliente, domicilio):

	# 00 - Generamos el archivo de salida para llevar registro del LOG: archivo-salida.py
	fc = open ('data/log_salida_contactos.txt','a', encoding='utf-8')
	fc.write('00 - ****** EMPEZAMOS CON LOS CONTACTOS del cliente ' + str(cliente) +  '\n')
	print("00 - ****** EMPEZAMOS CON LOS CONTACTOS del cliente ", str(cliente))

	# 01 - Cogemos los datos de los contactos y los pasamos a un excel 
	df_contactos = pd.DataFrame()
	df_contactos = pd.read_csv('data/contactos.csv', sep=';', encoding='latin-1')

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
	
	fc.write('03 - Contactos del cliente: '+ str(cliente) + ' son ' + str(df_filtered.count()) + "\n")
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
				fc.write('05a - No existe el email, lo damos de alta'  + "\n")
				print("05a - No existe el email, lo damos de alta" )		
				f_alta_contacto(conn, fc, domicilio, df_filtered.iloc[i]['telefono1'], df_filtered.iloc[i]['telefono2'], df_filtered.iloc[i]['departamento'], df_filtered.iloc[i]['cargo'],df_filtered.iloc[i]['nombre'] , df_filtered.iloc[i]['dni'], df_filtered.iloc[i]['idespecialidad'], email)
			else:
				fc.write('05b - Existe el email, lo vamos a actualizar ' + email + "\n" )
				print("05b - Existe el email, lo vamos a actualizar ", email )	

				for fila in resultados:
					print("Valor del campo 1:", fila[0])
					print("Valor del campo 2:", fila[1])
					
					if len(fila[0]) > 0:
						contacto = fila[0]
						if len(fila[1]) > 0:
							especialidad = fila[1]
						else:	
							especialidad = '' 
						f_update_contacto(fc, conn, contacto, especialidad)

		# 06 - El email no está informado. Metemos el contacto si o si
		else:
			fc.write('04 - No tiene email, damos de alta el contacto' + "\n")
			print("04 - No tiene email, damos de alta el contacto" )						
			f_alta_contacto(conn, fc, domicilio, df_filtered.iloc[i]['telefono1'], df_filtered.iloc[i]['telefono2'], df_filtered.iloc[i]['departamento'], df_filtered.iloc[i]['cargo'],df_filtered.iloc[i]['nombre'] ,df_filtered.iloc[i]['dni'], df_filtered.iloc[i]['idespecialidad'], email)
			
	fc.close()
	cursor.close()
	conn.close()






