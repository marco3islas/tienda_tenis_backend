import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = "f02834cddc43ff08ec46bcf040faba74ddd79fea8fdfe13db8464265fa909e30"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///tenis.db"
db = SQLAlchemy(app)


class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(100))
    titulo = db.Column(db.String(80))
    description = db.Column(db.String(300))
    precio = db.Column(db.String(10))
    tallas = db.Column(db.String(10))

    def to_json(self):
        return {
            'id': self.id,
            'imagen': self.imagen,
            'titulo' : self.titulo,
            'description': self.description,
            'precio' : self.precio,
            'tallas' : self.tallas
        }


@app.route('/productos', methods=['GET'])
def get_data():
    productos = Productos.query.all()
    productos_json = [producto.to_json() for producto in productos]
    print(jsonify(productos_json))
    return jsonify(productos_json)

@app.route('/productos/<int:item_id>', methods=['GET'])
def get_item(item_id):
    producto = Productos.query.get(item_id)
    if producto is None:
        return jsonify({
            'error': 'Producto not found'
        }), 404
    print(producto)
    return jsonify(producto.to_json())
    

if __name__=='__main__':
    if not os.path.exists("tenis.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True, port=5500)
    
