import mysql.connector
import os, time

def create_database(db_connection,db_name,cursor):
    cursor.execute(f"COMMIT;")
    cursor.execute(f"CREATE DATABASE {db_name};")
    cursor.execute(f"COMMIT;")
    cursor.execute(f"USE {db_name};")
    cursor.execute(f"COMMIT;")
    
    cursor.execute('''CREATE TABLE Programa (
        id INT NOT NULL AUTO_INCREMENT,
        nombre varchar(255) NOT NULL,
        director varchar(255),
        correo varchar(255),
        PRIMARY KEY (id)
        );''')
    cursor.execute("COMMIT;") 

    cursor.execute('''CREATE TABLE Estudiante (
        rut varchar(15) NOT NULL PRIMARY KEY, 
        nombre varchar(255) NOT NULL,
        correo varchar(255),
        id_programa INT NOT NULL,
        FOREIGN KEY (id_programa) REFERENCES Programa (id)
        );''')
    cursor.execute("COMMIT;") 

    cursor.execute('''CREATE TABLE Tener_arancel (
        id INT NOT NULL AUTO_INCREMENT,
        año int NOT NULL,
        valor int NOT NULL,
        id_programa INT NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (id_programa) REFERENCES Programa (id)
        );''')
    cursor.execute("COMMIT;") 

    cursor.execute('''CREATE TABLE Becas (
        id INT NOT NULL AUTO_INCREMENT,
        nombre varchar(255),
        porcentaje INT NOT NULL,
        año INT NOT NULL,
        semestre INT NOT NULL,
        rut_estudiante varchar(15) NOT NULL, 
        PRIMARY KEY (id),
        FOREIGN KEY (rut_estudiante) REFERENCES Estudiante (rut)
        );''')
    cursor.execute("COMMIT;") 

    cursor.execute('''CREATE TABLE Comprobante (
        num_boleta INT NOT NULL PRIMARY KEY, 
        monto INT NOT NULL,
        fecha_pago DATE,
        arancel_matricula VARCHAR(32),
        enlace_foto VARCHAR(255),
        rut_estudiante varchar(15) NOT NULL, 
        FOREIGN KEY (rut_estudiante) REFERENCES Estudiante (rut)
        );''')
    cursor.execute("COMMIT;") 

def insert_data(cursor):
    cursor.execute('INSERT INTO Programa (nombre, director, correo) VALUES ("Ingeniería Civil","Juan Pérez","juan.perez@example.com");')
    cursor.execute("INSERT INTO Programa (nombre, director, correo) VALUES ('Ingeniería Industrial', 'Ana Martínez', 'ana.martinez@example.com');")
    cursor.execute("INSERT INTO Programa (nombre, director, correo) VALUES ('Ingeniería Informática', 'Carlos Rodríguez', 'carlos.rodriguez@example.com');")
    cursor.execute("COMMIT;") 

    cursor.execute("INSERT INTO Tener_arancel (año, valor, id_programa) VALUES (2020, 100000, 1);")
    cursor.execute("INSERT INTO Tener_arancel (año, valor, id_programa) VALUES (2021, 120000, 2);")
    cursor.execute("INSERT INTO Tener_arancel (año, valor, id_programa) VALUES (2021, 120000, 3);")
    cursor.execute("INSERT INTO Tener_arancel (año, valor, id_programa) VALUES (2022, 1000000, 3);")
    cursor.execute("INSERT INTO Tener_arancel (año, valor, id_programa) VALUES (2022, 27000, 2);")
    cursor.execute("INSERT INTO Tener_arancel (año, valor, id_programa) VALUES (2022, 12000000, 1);")
    cursor.execute("COMMIT;") 

    cursor.execute(''' INSERT INTO Estudiante (nombre, rut, correo, id_programa) VALUES
    ("Juan Pérez", "12345678-9", "juan.perez@example.com", 1),
    ("Ana Martínez", "98765432-1", "ana.martinez@example.com", 2),
    ("Carlos Rodríguez", "12312312-3", "carlos.rodriguez@example.com", 3),
    ("Mónica Gómez", "45678901-2", "monica.gomez@example.com", 1),
    ("Sofía Díaz", "78901234-5", "sofia.diaz@example.com", 2),
    ("Pablo Martín", "78901234-6", "pablo.martin@example.com", 3),
    ("Laura Ruiz", "78901234-7", "laura.ruiz@example.com", 2);''')
    cursor.execute("COMMIT;") 

    cursor.execute('''INSERT INTO Becas (nombre, porcentaje, año, semestre, rut_estudiante) VALUES 
        ('Beca A', 50, 2020, 1, '12312312-3'), 
        ('Beca B', 75, 2022, 2, '12345678-9'), 
        ('Beca C', 25, 2021, 1, '98765432-1')
        ;''')
    cursor.execute("COMMIT;") 

    cursor.execute('''INSERT INTO Comprobante (num_boleta, monto, fecha_pago, arancel_matricula, enlace_foto, rut_estudiante)
    VALUES 
    (1, 100000, '2020-01-01', 'Arancel', 'https://example.com/comprobante1.jpg', '12312312-3'),
    (2, 120000, '2021-01-01', 'Arancel', 'https://example.com/comprobante2.jpg', '12345678-9'),
    (123, 70000, '2021-01-07', 'Matrícula', 'https://example.com/comprobante123.jpg', '12345678-9'),
    (3, 140000, '2022-01-01', 'Arancel', 'https://example.com/comprobante3.jpg', '98765432-1');''')
    cursor.execute("COMMIT;") 

#######################
DATABASE = "proyecto"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "teodiomysql"

not_connected = True

while(not_connected):
	try:
		print(DATABASE_IP,"IP")
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,password=DATABASE_USER_PASSWORD)
		not_connected = False

	except Exception as e:
		time.sleep(3)
		print(e, "error!!!")
		print("can't connect to mysql server, might be intializing")
		
cursor = db_connection.cursor()

try:
    cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
    cursor.execute(f"USE {DATABASE}")
    print(f"Database: {DATABASE} already exists")
except Exception as e:
    create_database(db_connection,DATABASE,cursor)
    insert_data(cursor)
    print(f"Succesfully created: {DATABASE}")