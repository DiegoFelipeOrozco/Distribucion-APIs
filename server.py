from flask import Flask, request
from controladores.Producto import Producto
app = Flask(__name__)

@app.route('/productos', methods=['GET'])
def getAll():
	return (Producto.list())

@app.route('/productos', methods=['POST'])
def insertANewOne():
	return (Producto.create(request.json))

@app.route('/productos', methods=['DELETE'])
def destroy():
	return (Producto.delete(request.args.get('nombre', '')))

@app.route('/productos', methods=['PUT'])
def update():
	return (Producto.update(request.args.get('nombre', ''),request.json))

if __name__=="__main__":
	app.run(port=5000)