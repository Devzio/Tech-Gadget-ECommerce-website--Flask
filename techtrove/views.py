from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Category, Product, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
# Index page
def index():
    products = Product.query.order_by(Product.id).all()
    categories = Category.query.order_by(Category.id).all()
    rating = Product.query.order_by(Product.rating).all()
    return render_template('index.html', products=products, categories=categories, rating=rating)

# /category/categoryid


@bp.route('/category/<int:categoryid>')
def product(categoryid):
    products = Product.query.filter(Product.category_id == categoryid)
    category = db.session.scalar(
        db.select(Category).where(Category.id == categoryid))
    return render_template('product.html', products=products, categoryName=category.name)

# /product-details/productid


@bp.route('/product-details/<int:productid>')
def productDetails(productid):
    products = Product.query.filter(Product.id == productid)
    color = Product.query.filter(Product.color)
    color = str(color)
    color = color.split(", ")
    print(color)
    return render_template('product_details.html', products=products, color=color)


# Referred to as "Cart" to the user
@bp.route('/order', methods=['POST', 'GET'])
def order():
    product_id = request.values.get('product_id')

    # if there is an existing order
    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])

    else:
        # if there is no order
        order = None

    # create new order
    if order is None:
        order = Order(status=False, firstname='', surname='',
                      email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
            session['count_id'] = 1
        except:
            print('Failed at creating a new order')
            order = None

    # calculate totalprice
    totalprice = 0
    if order is not None:
        for product in order.products:
            totalprice = totalprice + product.price

    # adding an item
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
                session['count_id'] += 1
            except:
                return 'There was an issue adding the item to your cart'
            return redirect(url_for('main.order'))
        else:
            flash('The Item is already in the cart')
            return redirect(url_for('main.order'))
    return render_template('order.html', order=order, totalprice=totalprice)

# Delete one item


@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        product_to_delete = Product.query.get(id)
        try:
            order.products.remove(product_to_delete)
            db.session.commit()
            session['count_id'] -= 1
            return redirect(url_for('main.order'))
        except:
            return 'There was a problem deleting your item from the order'
    return redirect(url_for('main.order'))

# Empty all cart items


@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        session['count_id'] = 1
        flash('All items from Cart is cleared!')
    return redirect(url_for('main.index'))

# Checkout


@bp.route('/checkout', methods=['POST', 'GET'])
def checkout():
    form = CheckoutForm()
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])

        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for product in order.products:
                totalcost = totalcost + product.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash(
                    'Thank you! Your Order has succesfully been submitted!')
                return redirect(url_for('main.index'))
            except:
                return 'Your Order was not succesful'
    return render_template('checkout.html', form=form)

# Search bar functionality


@bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        print(query)
        product = db.session.scalars(db.select(Product).where(
            Product.description.like(query))).all()
        for prod in product:
            print(prod.name)
        return render_template('product.html', search_product=product)
    else:
        return redirect(url_for('main.index'))
