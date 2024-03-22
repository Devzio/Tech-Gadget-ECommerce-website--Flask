from . import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    products = db.relationship('Product', backref='Category',
                               cascade="all, delete-orphan")

    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {}\n"
        str = str.format(self.id, self.name, self.description, self.image)
        return str


orderdetails = db.Table('orderdetails',
                        db.Column('order_id', db.Integer, db.ForeignKey(
                            'orders.id'), nullable=False),
                        db.Column('product_id', db.Integer, db.ForeignKey(
                            'products.id'), nullable=False),
                        db.PrimaryKeyConstraint('order_id', 'product_id'))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(64))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    rating = db.Column(db.Integer)

    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {}, Price: {}, Category: {}, Rating: {}\n"
        str = str.format(self.id, self.name, self.description,
                         self.image, self.price, self.category_id, self.rating)
        return str


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    products = db.relationship(
        "Product", secondary=orderdetails, backref="orders")

    def __repr__(self):
        str = "ID: {}, Status: {}, First Name: {}, Surname: {}, Email: {}, Phone: {}, Date: {}, Products: {}, Total Cost: {}\n"
        str = str.format(self.id, self.status, self.firstname, self.surname,
                         self.email, self.phone, self.date, self.products, self.totalcost)
        return str
