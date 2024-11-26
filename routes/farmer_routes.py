# routes/farmer_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, User, Farmer, Farm

farmer_blueprint = Blueprint('farmer', __name__)


@farmer_blueprint.route('/register', methods=['POST'])
def register_farmer():
    data = request.json
    hashed_password = generate_password_hash(data['password'])

    user = User(
        login=data['login'],
        email=data['email'],
        password=data['password'],
        phonenumber=data['phonenumber'],
        role='farmer',
        isVerified=False,
        name=data['name']
    )
    db.session.add(user)
    db.session.flush()


    farmer = Farmer(
        farmerID=user.userID,
        govermentIssuedID=data['govermentIssuedID'],
        profilePicture=data['profilePicture'],
        resources=data['resources'],
        rating=0.0
    )
    db.session.add(farmer)
    db.session.commit()
    return jsonify({"msg": "Farmer registered successfully, pending approval."}), 201

from models import db, Product


@farmer_blueprint.route('/add-product', methods=['POST'])
def add_product():
    data = request.json

    # Validate if the required fields are provided
    required_fields = ['farmerID', 'farmID', 'name', 'category', 'price', 'quantity', 'description', 'images']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    # Validate the farmer
    farmer = Farmer.query.get(data['farmerID'])
    if not farmer:
        return jsonify({"msg": "Farmer not found"}), 404

    # Validate the farm
    farm = Farm.query.get(data['farmID'])
    if not farm or farm.farmerID != data['farmerID']:
        return jsonify({"msg": "Invalid farmID for the given farmer"}), 400

    # Create the product
    product = Product(
        farmerID=data['farmerID'],
        farmID=data['farmID'],  # Associate the product with a farm
        name=data['name'],
        category=data['category'],
        price=data['price'],
        quantity=data['quantity'],
        description=data['description'],
        images=data['images']
    )

    db.session.add(product)
    db.session.commit()
    return jsonify({"msg": "Product added successfully!", "productID": product.productID}), 201


@farmer_blueprint.route('/update-product/<int:productID>', methods=['PUT'])
def update_product(productID):
    product = Product.query.get(productID)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    data = request.json

    # Validate farmID if provided
    if 'farmID' in data:
        farm = Farm.query.get(data['farmID'])
        if not farm or farm.farmerID != product.farmerID:
            return jsonify({"msg": "Invalid farmID for the given farmer"}), 400

        product.farmID = data['farmID']

    product.name = data.get('name', product.name)
    product.category = data.get('category', product.category)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    product.description = data.get('description', product.description)
    product.images = data.get('images', product.images)

    db.session.commit()
    return jsonify({"msg": "Product updated successfully!"}), 200

@farmer_blueprint.route('/delete-product/<int:productID>', methods=['DELETE'])
def delete_product(productID):
    product = Product.query.get(productID)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"msg": "Product deleted successfully!"}), 200

@farmer_blueprint.route('/add-farm/<int:farmer_id>', methods=['POST'])
def add_farm_to_farmer(farmer_id):
    farmer = Farmer.query.get(farmer_id)
    if not farmer:
        return jsonify({"error": "Farmer not found"}), 404

    data = request.get_json()
    if not data or not all(key in data for key in ['farmAddress', 'typesOfCrops', 'farmSize']):
        return jsonify({"error": "Invalid input, please provide all required fields"}), 400

    new_farm = Farm(
        farmerID=farmer_id,
        farmAddress=data['farmAddress'],
        typesOfCrops=data['typesOfCrops'],
        farmSize=data['farmSize']
    )

    db.session.add(new_farm)
    db.session.commit()

    return jsonify({"msg": f"Farm created successfully for Farmer ID {farmer_id}!", "farmID": new_farm.farmID}), 201


@farmer_blueprint.route('/profile/<int:farmer_id>', methods=['GET'])
def get_farmer_profile(farmer_id):
    farmer = Farmer.query.get(farmer_id)
    user = User.query.get(farmer_id)

    if not farmer or not user:
        return jsonify({"error": "Farmer not found"}), 404

    return jsonify({
        "name": user.name,
        "email": user.email,
        "phonenumber": user.phonenumber,
        "govermentIssuedID": farmer.govermentIssuedID,
        "profilePicture": farmer.profilePicture,
        "resources": farmer.resources,
        "rating": farmer.rating,
    }), 200

@farmer_blueprint.route('/farms/<int:farmer_id>', methods=['GET'])
def get_farms_for_farmer(farmer_id):
    try:
        # Fetch the farmer details
        farmer = Farmer.query.get(farmer_id)
        if not farmer:
            return jsonify({"error": "Farmer not found"}), 404

        # Fetch all farms associated with the farmer
        farms = Farm.query.filter_by(farmerID=farmer_id).all()
        if not farms:
            return jsonify({"msg": "No farms found for this farmer"}), 200

        # Prepare the response data
        farms_data = [
            {
                "farmID": farm.farmID,
                "farmAddress": farm.farmAddress,
                "typesOfCrops": farm.typesOfCrops,
                "farmSize": farm.farmSize,
            }
            for farm in farms
        ]

        return jsonify({"farms": farms_data}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500