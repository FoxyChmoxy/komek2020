from app import db

class Komek(db.Model):
    '''
    Главная и единственная бизнес-модель
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    phone = db.Column(db.String(20), index=True, unique=False)
    city = db.Column(db.String(30), index=True, unique=False)
    service = db.Column(db.String(255), index=True, unique=False)
    is_giver = db.Column(db.Boolean, unique=False, default=True)
    flag = db.Column(db.Boolean, unique=False, default=True)

    def __repr__(self):
        return '<User {} name {} is_giver {}>'.format(self.id, self.name, self.is_giver)
