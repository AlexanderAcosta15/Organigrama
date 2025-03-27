from flask import Blueprint, request, jsonify, render_template
from app.models import Nodo
from app import db

bp = Blueprint('main', __name__)

@bp.route('/api/nodos', methods=['GET'])
def get_nodos():
    nodos = Nodo.query.all()
    return jsonify([nodo.to_dict() for nodo in nodos])

@bp.route('/api/nodos', methods=['POST'])
def create_nodo():
    data = request.get_json()
    
    nodo = Nodo(
        titulo=data['titulo'],
        descripcion=data.get('descripcion'),
        tipo=data['tipo'],
        padre_id=data.get('padre_id'),
        posicion_x=data.get('posicion_x', 0),
        posicion_y=data.get('posicion_y', 0)
    )
    
    db.session.add(nodo)
    db.session.commit()
    
    return jsonify(nodo.to_dict()), 201

@bp.route('/api/nodos/<int:id>', methods=['PUT'])
def update_nodo(id):
    nodo = Nodo.query.get_or_404(id)
    data = request.get_json()
    
    nodo.titulo = data.get('titulo', nodo.titulo)
    nodo.descripcion = data.get('descripcion', nodo.descripcion)
    nodo.tipo = data.get('tipo', nodo.tipo)
    nodo.padre_id = data.get('padre_id', nodo.padre_id)
    nodo.posicion_x = data.get('posicion_x', nodo.posicion_x)
    nodo.posicion_y = data.get('posicion_y', nodo.posicion_y)
    
    db.session.commit()
    
    return jsonify(nodo.to_dict())

@bp.route('/api/nodos/<int:id>', methods=['DELETE'])
def delete_nodo(id):
    nodo = Nodo.query.get_or_404(id)
    db.session.delete(nodo)
    db.session.commit()
    return jsonify({'message': 'Nodo eliminado'})

@bp.route('/api/nodos/reorganizar', methods=['POST'])
def reorganizar_nodos():
    try:
        nodos = Nodo.query.all()
        nodos_dict = {nodo.id: nodo for nodo in nodos}
        nodos_raiz = [nodo for nodo in nodos if nodo.padre_id is None]

        ANCHO_NODO = 180
        MARGEN_HORIZONTAL = 100
        MARGEN_VERTICAL = 150
        POSICION_INICIAL_Y = 100

        def posicionar_nodos(nodo_padre, nivel, x_inicio, ancho_disponible):
            hijos = [n for n in nodos if n.padre_id == nodo_padre.id]
            if not hijos:
                return x_inicio + ancho_disponible / 2
            
            espacio_entre_nodos = ancho_disponible / len(hijos)
            x_actual = x_inicio
            
            for hijo in hijos:
                x_hijo = x_actual + espacio_entre_nodos / 2 - ANCHO_NODO / 2
                hijo.posicion_x = x_hijo
                hijo.posicion_y = POSICION_INICIAL_Y + nivel * MARGEN_VERTICAL
                x_actual = posicionar_nodos(hijo, nivel + 1, x_actual, espacio_entre_nodos)
            
            return x_actual

        x_actual = 0
        espacio_por_raiz = 3000 / max(1, len(nodos_raiz))
        
        for raiz in nodos_raiz:
            raiz.posicion_x = x_actual + espacio_por_raiz / 2 - ANCHO_NODO / 2
            raiz.posicion_y = POSICION_INICIAL_Y
            posicionar_nodos(raiz, 1, x_actual, espacio_por_raiz)
            x_actual += espacio_por_raiz
        
        db.session.commit()
        
        return jsonify({
            'message': 'Árbol reorganizado correctamente',
            'nodos_actualizados': len(nodos)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al reorganizar el árbol',
            'detalles': str(e)
        }), 500

@bp.route('/')
def index():
    return render_template('index.html')