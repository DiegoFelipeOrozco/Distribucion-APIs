import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from controladores.Producto import Producto

UPLOAD_FOLDER = os.path.join('recursos','subidos','imagenes','productos')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/productos', methods=['GET'])
def getAll():
	return (Producto.list())

@app.route('/productos', methods=['POST'])
def insertANewOne():
	dataRequest = {}
	gestionarImagenes(request.files, dataRequest)
	dataRequest.update(request.form)
	return (Producto.create(dataRequest))

@app.route('/productos', methods=['DELETE'])
def destroy():
	return (Producto.delete(request.args.get('nombre', '')))

@app.route('/productos', methods=['PUT'])
def update():
	dataRequest = {}
	gestionarImagenes(request.files, dataRequest)
	dataRequest.update(request.form)
	return (Producto.update(request.args.get('nombre', ''),dataRequest))

'''Almacena las imagenes en el servidor y las direcciona en dataRequest
'''
def gestionarImagenes(files, dataRequest):
	if 'imagen' in files and files['imagen'].filename != '':
		app.logger.debug('hay archivo')
		file = files['imagen']
		if allowed_file(file.filename):
			app.logger.debug('el archivo tiene extension valida')
			fileAdress = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
			file.save(fileAdress)
			dataRequest.update({"imagen": fileAdress})

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
