
# Importamos las empresas desde el csv a la bbdd de empresas, tabla GE_EMPRESAS y GE_DOMICILIOS 

import 	pandas as pd
import  MySQLdb
from 	datetime import datetime
import 	mysql.connector
import 	Importar_contactos as contact

# Función que dada una idespecialidad, me retorne su codespecialidad  concatenado con ' FORM' 
def f_dame_especialidad(idespecial):

	codigo = "FORM" 
	cursorespecial = conn.cursor()
	cursorespecial.execute("SELECT codespecialidad FROM especialidad WHERE idespecialidad = %s", (idespecial, ))
	resultados = cursorespecial.fetchall()

	for resultado in resultados:
		codigo += '/ ' + str(resultado[0]) 	

	cursorespecial.close()
	return codigo		

# Función que da de alta la dirección de la empresa pasada por parámetro
# Tener en cuenta los domicilios que ya existen, se puede comprobar por email
def f_alta_domicilio(idempresa, domicilio, cp, provincia, localidad, telefono, email, especialidad):
	# 08 - Miramos si existe o no en la bbdd por email

	if cp == 0:
		cp = ' '

	if localidad == 0:
		localidad = ' '

	cursordireccion = conn.cursor()
	cursordireccion.execute("SELECT iddomicilio FROM ge_domicilios WHERE email like %s", ("%" + str(email)+ "%",))
	resultados = cursordireccion.fetchall()
	for resultado in resultados:
		print('08 - La dirección ya existe en la BBDD. NO INSERTAMOS. ID_DOMICILIO: ****************** ', str(resultado[0]))
		f.write('08 - La dirección ya existe en la BBDD. NO INSERTAMOS. ID_DOMICILIO:  ****************** ' + str(resultado[0]))		
		cursordireccion.close()	
		return str(resultado[0])

	# 08 - Si no existe registro en la tabla, lo tendremos que dar de alta 
	if len(resultados)==0:

		# El campo del CP está acortado a 5 
		if len(str(cp)) > 5:
			cp = cp[:5]

		email = str(email)[:59]
		telefono = str(telefono)[:49]

		curinsert = conn.cursor()
		sql = "INSERT INTO ge_domicilios(idempresa, domicilio, cp, provincia, localidad, telefono, email, especialidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		val = (idempresa, domicilio, cp, provincia, localidad, telefono, email, especialidad)
		curinsert.execute(sql, val)
		conn.commit()

		print("08 - Registro insertado con la dirección: " , email)
		f.write('08 - El registro ha sido insertado correctamente para la dirección '+ str(domicilio) + ' de la empresa ' + str(idempresa) +'  \n')		
		
		# Buscamos el código del a dirección que se acaba de insertar
		cursordireccion.execute("SELECT max(iddomicilio) FROM ge_domicilios")

		resultados = cursordireccion.fetchall()
		if len(resultados) != 0: 			
			valor = resultados[0]
			valor_extaido = valor[0]
			curinsert.close()
			cursordireccion.close()	
			return str(valor_extaido)
		else:
			return -1 

	curinsert.close()
	cursordireccion.close()	

# Función que devuelve el siguiente IDEMPRESA menor que 3000 (los mayores que 3000 son PDB)
def f_dame_id_empresa():
	cursoridempresa = conn.cursor()
	cursoridempresa.execute("SELECT max(idempresa) + 1 FROM ge_empresas WHERE idempresa < 3000")
	resultados = cursoridempresa.fetchall()
	for resultado in resultados:
		newidempresa = resultado[0]
		print('07 - El nuevo IDEMPRESA retornado ES: ', newidempresa)
		f.write('07 - El nuevo  IDEMPRESA retornado ES:' + str(newidempresa))

	cursoridempresa.close()
	return newidempresa		

# Funcion que da de alta la empresa que recibe por parámetro
def f_alta_empresa(cif, nombre, convenio, fechaconvenio, web, observaciones, interesados, pdb, cliente, proveedor):
		
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

		if len(nombre) > 100:
			nombre = nombre[:99]

		if len(cif) > 12:
			cif = cif[:12]

		if not isinstance(fechaconvenio, datetime):
			fechaconvenio = datetime.now()

		proveedor = str(proveedor)
			
		sql = "INSERT INTO ge_empresas (idempresa, cif, empresa, observaciones, convenio, fechaconvenio, web, interesadobolsa, pdb, cliente, proveedor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		val = (idempresanew, cif, nombre, observaciones, convenio, fechaconvenio, web, interesados, pdb, cliente, proveedor)
		curinsert.execute(sql, val)
		conn.commit()

		print("06 - Registro insertado con la empresa: " , nombre)
		f.write('06 - El registro ha sido insertado correctamente '+ nombre + '************ \n')
		fi.write('Insertado:  ' + cif + ' ' + nombre + '\n')
		curinsert.close()

		return idempresanew

# 00 - Generamos el archivo de salida para llevar registro del LOG: archivo-salida.py
f = open ('data/log_salida.txt','w', encoding='utf-8')
f.write('****** EMPEZAMOS CON LAS EMPRESAS '+ '\n')

fi = open ('data/log_empresas_insertados.txt','w', encoding='utf-8')
fe = open ('data/log_empresas_encontrados.txt','w', encoding='utf-8')

# 01 - Cogemos los datos de las empresas y los pasamos a un excel 
df_empresa = pd.DataFrame()
"""
# Esta es la forma de Alvaro y se lee mal 
fichero = open('data/clientes.csv', 'r')
for line in fichero:
	print(line.encode())


# Esta es la forma de Larisa y se lee bien 
import csv
with open('data/clientes.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        print(', '.join(row))

		"""

# Esta es mi forma y se lee mal 
df_empresa = pd.read_csv('data/empresas.csv', sep=';', encoding='latin-1')
df_empresa = df_empresa.fillna(0)
df_empresa.to_excel('data/excel_empresas.xlsx')


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
	  
	print("03 - ************************************************* DATOS DE LA EMPRESA ******** " ,  nombreempresa  )
	f.write("03 - ************************************************* DATOS DE LA EMPRESA ******** " +  nombreempresa  + "\n" )

	if cifempresa is None or  cifempresa == 0:
		print("03 - No tiene CIF, vamos a trabajar con su nombre" , nombreempresa)		
		f.write("03 -  No tiene CIF, vamos a trabajar con su nombre: " +  nombreempresa + "\n" )
		
		# 03a - Miramos si existe o no en la bbdd po nombre
		cursor.execute("SELECT CAST(idempresa as char) FROM ge_empresas WHERE empresa like %s", ("%" + nombreempresa+ "%",))

		resultados = cursor.fetchall()
		for resultado in resultados:
			print('03a - La empresa ya existe en la base de datos. NO INSERTAMOS. ID_EMPRESA: ****************** ', resultado[0])
			f.write('03a - La empresa ya existe en la base de datos. NO INSERTAMOS. ID_EMPRESA:  ****************** ' + resultado[0] + "\n")
			fe.write('Entrontrado:  ' + nombreempresa + ', con el ID_EMPRESA ' + resultado[0] + '\n')

		# 03b - Si no existe registro en la tabla, lo tendremos que dar de alta 
		if len(resultados)==0:
			
			if df_empresa.iloc[i]['apellidos'] != 0:
				nombrecompleto = nombreempresa + ' ' + df_empresa.iloc[i]['apellidos'] 
			else:
				nombrecompleto = nombreempresa

			if nombreempresa != df_empresa.iloc[i]['razonsocial'] and df_empresa.iloc[i]['razonsocial'] != 0:
				nombrecompleto += ' ' + str(df_empresa.iloc[i]['razonsocial'])
			
			idempresanew = f_alta_empresa('0', nombrecompleto, df_empresa.iloc[i]['convenio'] , df_empresa.iloc[i]['conveniofecha'] , df_empresa.iloc[i]['web'], df_empresa.iloc[i]['observaciones'], df_empresa.iloc[i]['interesadosbolsa'], df_empresa.iloc[i]['pdb'], df_empresa.iloc[i]['cliente'], df_empresa.iloc[i]['proveedor'])
			especialidad = f_dame_especialidad(df_empresa.iloc[i]['idespecialidad'])
			domicilio = f_alta_domicilio(idempresanew, df_empresa.iloc[i]['domicilio'], df_empresa.iloc[i]['cp'], df_empresa.iloc[i]['provincia'], df_empresa.iloc[i]['municipio'], df_empresa.iloc[i]['telefono'], df_empresa.iloc[i]['email'], especialidad)
			contact.f_contactos(df_empresa.iloc[i]['idcliente'], domicilio)
	else:
		
		# 04 - Comprobamos si el CIF ya está metido en la BBDD o no: 
		print("04 - La variable no es nula y tiene el valor:", cifempresa)		
		f.write('04 - ********************** CIF:' +  cifempresa + '\n') 
		cursor.execute("SELECT CAST(idempresa as char) FROM ge_empresas WHERE cif= %s", (cifempresa,))
				
		# 05 - Obtener los datos de la empresa existente o no en la tabla
		resultados = cursor.fetchall()
		for resultado in resultados:			
			print('05 - La empresa ya existe en la base de datos. NO INSERTAMOS. IDEMPRESA: ****************** ', resultado[0])
			f.write('05 - La empresa ya existe en la base de datos. NO INSERTAMOS. IDEMPRESA:  ****************** ' + resultado[0]+ "\n")
			fe.write('Entrontrado:  ' + cifempresa + ' ' + nombreempresa + ' ' + resultado[0] + '\n')

		# 06 - Si no existe registro en la tabla, lo tendremos que dar de alta 
		if len(resultados)==0:			
			if df_empresa.iloc[i]['apellidos'] != 0:
				nombrecompleto = nombreempresa + ' ' + df_empresa.iloc[i]['apellidos'] 
			else:
				nombrecompleto = nombreempresa

			if nombreempresa != df_empresa.iloc[i]['razonsocial']:
				nombrecompleto += ' ' + str(df_empresa.iloc[i]['razonsocial']) 

			idempresanew = f_alta_empresa(df_empresa.iloc[i]['cif'], nombrecompleto, df_empresa.iloc[i]['convenio'] , df_empresa.iloc[i]['conveniofecha'] , df_empresa.iloc[i]['web'] , df_empresa.iloc[i]['observaciones'], df_empresa.iloc[i]['interesadosbolsa'], df_empresa.iloc[i]['pdb'], df_empresa.iloc[i]['cliente'], df_empresa.iloc[i]['proveedor'])
			especialidad = f_dame_especialidad(df_empresa.iloc[i]['idespecialidad'])
			domicilio = f_alta_domicilio(idempresanew, df_empresa.iloc[i]['domicilio'], df_empresa.iloc[i]['cp'], df_empresa.iloc[i]['provincia'], df_empresa.iloc[i]['municipio'], df_empresa.iloc[i]['telefono'], df_empresa.iloc[i]['email'], especialidad)
			contact.f_contactos(df_empresa.iloc[i]['idcliente'], domicilio)

# 99 - Cerramos todo lo que quede abierto 			
cursor.close()
conn.close()
f.close()
fe.close()
fi.close()
