from extensions import db

class User(db.Model):
    __tablename__ = 'user'

    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    phonenumber = db.Column(db.String(11), nullable=False)
    role = db.Column(db.String(12), nullable=False)  # "farmer" or "buyer"
    isVerified = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(64), nullable=False)

class Farmer(db.Model):
    __tablename__ = 'farmers'

    farmerID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)
    govermentIssuedID = db.Column(db.Integer, nullable=False)
    profilePicture = db.Column(db.String(64), nullable=False)
    resources = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)


class Buyer(db.Model):
    __tablename__ = 'buyer'

    buyerID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)
    deliveryAddress = db.Column(db.String(64), nullable=False)
    paymentMethod = db.Column(db.String(32), nullable=False)

class Farm(db.Model):
    __tablename__ = 'farms'

    farmID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmerID = db.Column(db.Integer, db.ForeignKey('farmers.farmerID'), nullable=False)
    farmAddress = db.Column(db.String(64), nullable=False)
    typesOfCrops = db.Column(db.String(128), nullable=False)
    farmSize = db.Column(db.Integer, nullable=False)

    # Relationship with Farmer model
    farmer = db.relationship('Farmer', backref=db.backref('farms', lazy=True))

    def __repr__(self):
        return f'<Farm {self.farmID}, Address: {self.farmAddress}, FarmerID: {self.farmerID}>'


class Product(db.Model):
    __tablename__ = 'product'
    productID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmerID = db.Column(db.Integer, db.ForeignKey('farmers.farmerID'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    images = db.Column(db.JSON, nullable=True)
    farmID = db.Column(db.Integer, db.ForeignKey('farms.farmID'), nullable=False)

    def __repr__(self):
        return f"<Product productID={self.productID}, name={self.name}, price={self.price}, quantity={self.quantity}>"


class Cart(db.Model):
    __tablename__ = 'cart'
    cartID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyerID = db.Column(db.Integer, db.ForeignKey('buyer.buyerID'), nullable=False)

    # Relationship with CartProduct model to link cart with products
    products = db.relationship('CartProduct', backref='cart', lazy=True)

    def __repr__(self):
        return f"<Cart cartID={self.cartID}, buyerID={self.buyerID}>"


class CartProduct(db.Model):
    __tablename__ = 'cart_products'
    cartID = db.Column(db.Integer, db.ForeignKey('cart.cartID'), nullable=False, primary_key=True)
    productID = db.Column(db.Integer, db.ForeignKey('product.productID'), nullable=False, primary_key=True)

    # This relationship is optional depending on your setup
    product = db.relationship('Product', backref='cart_products', lazy=True)

    def __repr__(self):
        return f"<CartProduct cartID={self.cartID}, productID={self.productID}>"


class Chat(db.Model):
    chatID = db.Column(db.Integer, primary_key=True)
    farmerID = db.Column(db.Integer, nullable=False)
    buyerID = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.Integer, nullable=False)


class Message(db.Model):
    messageID = db.Column(db.Integer, primary_key=True)
    chatID = db.Column(db.Integer, db.ForeignKey('chat.chatID'), nullable=False)
    sender = db.Column(db.String(8), nullable=False)  # "farmer" or "buyer"
    messageText = db.Column(db.Text, nullable=False)
    messageDateTime = db.Column(db.DateTime, nullable=False)



class Order(db.Model):
    __tablename__ = 'order'

    orderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cartID = db.Column(db.Integer, db.ForeignKey('cart.cartID'), nullable=False)
    totalPrice = db.Column(db.Integer, nullable=False)
    orderDate = db.Column(db.DateTime, nullable=True)
    orderStatus = db.Column(db.String(11), nullable=False)

    cart = db.relationship('Cart', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"<Order orderID={self.orderID}, cartID={self.cartID}, totalPrice={self.totalPrice}, orderStatus={self.orderStatus}>"
