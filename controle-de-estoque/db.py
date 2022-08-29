from flask_mysqldb import MySQL
from config import app, cursor, conn

mysql = MySQL(app)

sql ='''CREATE TABLE IF NOT EXISTS tb_produto(
   ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   nome VARCHAR(20),
   valor_compra FLOAT,
   valor_venda FLOAT,
   quantidade_estoque INT,
   quantidade_minima INT
)'''
cursor.execute(sql)
conn.close()
