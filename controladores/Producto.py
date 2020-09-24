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
			return {"mensaje":"insertado"}, 201
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

	def delete(id):
		cnx = conexion()
		cursor = cnx.cursor()
		try:
			data = (id,)
			sql = "DELETE FROM producto WHERE Nombre=%s;"
			cursor.execute(sql,data)
			cnx.commit()
			if (cursor.rowcount == 0):
				return {"mensaje":"no se encontro registro con ese id"}, 200
			else:
				return {"mensaje":"eliminado"}, 200
		finally:
			cursor.close()
			cursor = cnx.cursor()

	def update(id, body):
		cnx = conexion()
		cursor = cnx.cursor()
		try:
			parametros = ""
			for clave in body:
				parametros = parametros + str(clave) + "=%(" + clave + ")s,"
			sql = "UPDATE producto SET " + parametros[0:-1] + ";"
			cursor.execute(sql, body)
			cnx.commit()
			return {"mensaje":"modificado"}, 200
		except DatabaseError as e:
			#si los tipos de entrada no son los esperados
			return {"mensaje":"Restriccion de base de datos violada: " + str(e)}, 500
		finally:
			cursor.close()
			cursor = cnx.cursor()