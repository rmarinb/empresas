import  pandas as pd
import  MySQLdb

especialidades = pd.DataFrame();
especialidades = pd.read_csv('data/especialidad.csv',sep=';',encoding='ISO-8859-1');
especialidades.to_excel('data/text_especialidades.xlsx');


db = MySQLdb.connect(host="localhost",      # tu host, usualmente localhost
                     user="root",           # tu usuario
                     passwd="root",         # tu password
                     db="empresas")         # el nombre de la base de datos


especialidades.to_sql(con=db, name='especialidad', if_exists='replace', flavor='mysql')

db.close();

