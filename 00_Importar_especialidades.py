import  pandas as pd
import  MySQLdb
from    sqlalchemy import create_engine

especialidades = pd.DataFrame()
especialidades = pd.read_csv('data/especialidad.csv',sep=';',encoding='ISO-8859-1', index_col=0)
especialidades = especialidades.drop(columns=['nombreespecialidad_a']) # quitamos el campo que nos sobra

engine = create_engine('mysql+mysqlconnector://root:root@localhost/empresas')
engine = engine.execution_options(autocommit=True)
especialidades.to_sql('especialidad',con=engine, if_exists='append')


