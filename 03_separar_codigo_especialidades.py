import 	mysql.connector

# Conectamos a la BBDD 
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='empresas'
)

cursor = conn.cursor()
cursorupdate = conn.cursor()

cursor.execute("select 	idespecialidad, mid(mid(nombreespecialidad, 7),1, locate('(', mid(nombreespecialidad, 7))-1) as especialidad, mid(nombreespecialidad, locate('(', nombreespecialidad)+1, 6) as codigo from especialidad where nombreespecialidad like 'FCT%';")

sql="update especialidad set nombreespecialidad=%s, codespecialidad=%s where idespecialidad=%s"

# Obtener los resultados de la consulta
resultados = cursor.fetchall()
for resultado in resultados:
    print('IDespecialidad:', resultado[0]) 
    print('Nombre especialidad', resultado[1]) 
    print('Código especialidad', resultado[2]) 

    datos=(resultado[1], resultado[2], resultado[0])
    cursorupdate.execute(sql, datos)
    conn.commit()
    
cursor.close()
cursorupdate.close()
conn.close()
