from flask import jsonify
from db.conexion import conexion
from mysql.connector.errors import IntegrityError,DatabaseError

class Producto():
		
	def list():
		cnx = conexion()
		cursor = cnx.cursor()
		try:
			lista = []
			cursor.execute("SELECT Nombre, Unidades, Peso_unitario, Volumen_unitario, Periodo_caducidad, Precio_unitario, Tipo FROM producto")
			rows = cursor.fetchall()
			columns = [i[0] for i in cursor.description]
			for row in rows:
				registros = zip(columns,row)
				json = dict(registros)
				lista.append(json)
			return jsonify(lista)
		finally:
			cursor.close()
			cnx.close()

	def create(body):
		cnx = conexion()
		cursor = cnx.cursor()
		try:
			#si llegan mas propiedades de las necesarias se ignoran
			bodySchema = {
				"nombre":body["nombre"],
				"unidades":body["unidades"],
				"peso":body["peso"],
				"volumen":body["volumen"],
				"caducidad":None,
				"precio":body["precio"],
				"tipo":body["tipo"],
				"imagen":None
			}
			bodySchema.update(body)
			data = (bodySchema["nombre"],bodySchema["unidades"],bodySchema["peso"],bodySchema["volumen"],bodySchema["caducidad"],bodySchema["precio"],bodySchema["tipo"],bodySchema["imagen"])
			sql = "INSERT INTO producto (Nombre, Unidades, Peso_unitario, Volumen_unitario, Periodo_caducidad, Precio_unitario, Tipo, Imagen) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
			cursor.execute(sql,data)
			cnx.commit()
			return {"estado":"insertado"}, 200
		except KeyError:
			#si no es un json simple lo que llega o si llegan menos propiedades de las necesarias
			return {"mensaje":"Propiedad necesaria no pasada"}, 400
		except IntegrityError:
			#si las entradas coinciden con un registro ya insertado
			return {"mensaje":"Registro ya insertado"}, 422
		except DatabaseError as e:
			#si los tipos de entrada no son los esperados
			return {"mensaje":"Restriccion de base de datos violada: " + str(e)}, 500
		finally:
			cursor.close()
			cursor = cnx.cursor()