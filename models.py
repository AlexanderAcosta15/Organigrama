from app import db

class Nodo(db.Model):
    __tablename__ = 'nodos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(20), nullable=False)
    padre_id = db.Column(db.Integer, db.ForeignKey('nodos.id'))
    posicion_x = db.Column(db.Integer)
    posicion_y = db.Column(db.Integer)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())
    fecha_actualizacion = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    hijos = db.relationship('Nodo', backref=db.backref('padre', remote_side=[id]), lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'padre_id': self.padre_id,
            'posicion_x': self.posicion_x,
            'posicion_y': self.posicion_y
        }