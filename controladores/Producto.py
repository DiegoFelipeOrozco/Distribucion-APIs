from flask import jsonify
from db.conexion import conexion

class Producto():
	global cursor
	cursor = conexion.cursor()
		
	def list():
		lista = []
		cursor.execute("SELECT Nombre, Unidades, Peso_unitario, Volumen_unitario, Periodo_caducidad, Precio_unitario, Tipo FROM producto")
		rows = cursor.fetchall()
		columns = [i[0] for i in cursor.description]
		for row in rows:
			registros = zip(columns,row)
			json = dict(registros)
			lista.append(json)
		return jsonify(lista)
		cursor.close()
		conexion.close()

	def create(body):
		data = (body["nombre"],body["unidades"],body["peso"],body["volumen"],body["caducidad"],body["precio"],body["tipo"])
		sql = "INSERT INTO producto (Nombre, Unidades, Peso_unitario, Volumen_unitario, Periodo_caducidad, Precio_unitario, Tipo, Imagen) VALUES(%s, %s, %s, %s, %s, %s, %s, DEFAULT);"
		cursor.execute(sql,data)
		conexion.commit()
		#si no es un json simple lo que llega
		#si llegan mas propiedades de las necesarias
		#si llegan menos propiedades de las necesarias
		#si los tipos de dato no son los esperados
		#si las entradas no cumplen las restricciones de negocio
		return {"estado":"insertado"}, 200
		cursor.close()
		conexion.close()