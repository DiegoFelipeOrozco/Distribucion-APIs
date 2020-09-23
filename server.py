from flask import Flask, request
from controladores.Producto import Producto
app = Flask(__name__)

@app.route('/productos', methods=['GET'])
def getAll():
	return (Producto.list())

@app.route('/productos', methods=['POST'])
def insertANewOne():
	body = request.json
	return (Producto.create(body))

@app.route('/productos', methods=['DELETE'])
def destroy():
	return (Producto.delete(request.args.get('nombre', '')))
