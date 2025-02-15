from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>', methods=['PATCH', 'GET'])
def bakery_by_id(id):
    if request.method == 'GET':
        bakery = Bakery.query.filter_by(id=id).first()
        if not bakery:
            return make_response({"error": "Bakery not found"}, 404)
        return make_response(bakery.to_dict(), 200)

    elif request.method == 'PATCH':
        bakery = Bakery.query.filter_by(id=id).first()
        if not bakery:
            return make_response({"error": "Bakery not found"}, 404)
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        db.session.add(bakery)
        db.session.commit()
        return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(baked_goods_by_price_serialized, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    if not most_expensive:
        return make_response({"error": "No baked goods found"}, 404)
    return make_response(most_expensive.to_dict(), 200)

@app.route('/baked_goods', methods=['POST'])
def new_baked_good():
    if request.method == 'POST':
        new_baked = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            created_at=request.form.get("created_at"),
            updated_at=request.form.get("updated_at"),
            bakery_id=request.form.get("bakery_id"),
        )
        db.session.add(new_baked)
        db.session.commit()
        return make_response(new_baked.to_dict(), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked = db.session.get(BakedGood, id)
    if not baked:
        return make_response({"error": "Baked good not found"}, 404)
    
    
    baked_dict = baked.to_dict()
    db.session.delete(baked)
    db.session.commit()
    
    return make_response(baked_dict, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)