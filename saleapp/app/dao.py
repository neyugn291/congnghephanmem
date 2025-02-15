from app.models import Category, Book, User, UserRole, Receipt, ReceiptDetail, ReceivedNote, Comment, \
    ReceivedNoteDetail, Order, OrderDetail, Regulation
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime

def load_categories():
    return Category.query.order_by("id").all()


def load_books(cate_id=None, kw=None, page=1, page_size = 0):
    query = Book.query

    if kw:
        query = query.filter(Book.name.contain(kw))

    if cate_id:
        query = query.filter(Book.category_id == cate_id)

    query = query.filter(Book.id > 1)
    if not page_size:
        page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    query = query.offset(start).limit(page_size)

    return query.all()





def count_books():
    return Book.query.count()


def get_category_by_id(id):
    return Category.query.get(id)

def get_book_by_id(id):
    return Book.query.get(id)


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(UserRole.ADMIN))
    return u.first()


def add_user(name, username, password, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()

def add_receipt_online(cart):
    if cart:
        r = Receipt(customer=current_user, created_date = func.now())

        db.session.add(r)
        for c in cart.values():
            d = ReceiptDetail(quantity=c['quantity'], price=c['price'],
                               receipt=r, book_id=c['id'])
            db.session.add(d)

            book = db.session.query(Book).filter(Book.id == c['id']).first()
            if book:
                book.quantity -= c['quantity']
                db.session.add(book)

        db.session.commit()

def add_receipt_sell(receipts):
    if receipts:

        rec = Receipt(seller = current_user, created_date = func.now(), customer_id=1)

        print(receipts)
        print(receipts.values())
        db.session.add(rec)
        #db.session.commit()

        for r in receipts.values():
            print(type(r['book_id']),type(r['quantity']),type(r['id']),type(r['price']))
            rd = ReceiptDetail(receipt=rec , book_id=r['book_id'],
                               quantity=r['quantity'], price=r['price'])
            db.session.add(rd)

            book = db.session.query(Book).filter(Book.id == r['id']).first()
            if book:
                book.quantity -= r['quantity']
                db.session.add(book)

    db.session.commit()

def add_receipt_order(receipts):
    if receipts:

        rec = Receipt(seller = current_user, customer_id = receipts['1']['customer_id'], created_date = func.now())

        db.session.add(rec)

        for r in receipts.values():
            print(type(r['book_id']), type(r['quantity']), type(r['id']), type(r['price']))
            rd = ReceiptDetail(receipt=rec, book_id=r['book_id'], quantity=r['quantity'], price=r['price'])

            db.session.add(rd)

            book = db.session.query(Book).filter(Book.id == r['id']).first()
            if book:
                book.quantity -= r['quantity']
                db.session.add(book)

    db.session.commit()

def add_receive_note(receives):
    if receives:

        rn = ReceivedNote(warehouse_id = current_user.id, received_day = func.now())

        print(receives)
        print(receives.values())
        db.session.add(rn)
        #db.session.commit()

        for r in receives.values():
            print(type(r['book_id']),type(r['quantity']),type(rn.id))
            rnd = ReceivedNoteDetail(received_note=rn ,book_id=int(r['book_id']),quantity=r['quantity'])

            db.session.add(rnd)
            book = db.session.query(Book).filter(Book.id == r['book_id']).first()
            if book:
                book.quantity += r['quantity']
                db.session.add(book)

    db.session.commit()

def load_comments(book_id):
    return Comment.query.filter(Comment.book_id.__eq__(book_id)).order_by(-Comment.id).all()


def add_comment(content, book_id):
    c = Comment(content=content, book_id=book_id, user=current_user, created_date = datetime.now())
    db.session.add(c)
    db.session.commit()

    return c

def add_order(orders):
    if orders:
        order = Order(user=current_user, order_day=func.now())
        db.session.add(order)
        # db.session.commit()
        for o in orders.values():
            #print(type(r['book_id']), type(r['quantity']), type(rn.id))
            od = OrderDetail(order=order, book_id=int(o['id']),
                             quantity=int(o['quantity']), price=float(o['price']))
            db.session.add(od)
    db.session.commit()

def get_order_details_by_order_id(order_id):
    return OrderDetail.query.filter(OrderDetail.order_id.__eq__(order_id)).order_by(OrderDetail.id).all()

def revenue_stats():
    return db.session.query(Book.id, Book.name, func.sum(ReceiptDetail.quantity * ReceiptDetail.price))\
                     .join(ReceiptDetail, ReceiptDetail.book_id.__eq__(Book.id)).group_by(Book.id).all()


def revenue_time(time='month', year=datetime.now().year):
    return db.session.query(func.extract(time, Receipt.created_date),
                            func.sum(ReceiptDetail.quantity * ReceiptDetail.price))\
                    .join(ReceiptDetail,
                          ReceiptDetail.receipt_id.__eq__(Receipt.id)).filter(func.extract("year", Receipt.created_date).__eq__(year))\
                    .group_by(func.extract(time, Receipt.created_date)).order_by(func.extract(time, Receipt.created_date)).all()

def frequency_stats():
    return db.session.query(Book.id, Book.name, func.sum(ReceiptDetail.quantity))\
                     .join(ReceiptDetail, ReceiptDetail.book_id == Book.id)\
                     .group_by(Book.id).all()

def frequency_time(time='month', year=datetime.now().year):
    return db.session.query(func.extract(time, Receipt.created_date),
                            func.sum(ReceiptDetail.quantity))\
                    .join(ReceiptDetail, ReceiptDetail.receipt_id == Receipt.id)\
                    .filter(func.extract("year", Receipt.created_date) == year)\
                    .group_by(func.extract(time, Receipt.created_date))\
                    .order_by(func.extract(time, Receipt.created_date)).all()


def get_cancel_time():
    result = db.session.query(Regulation.order_cancel_time).first()
    if result:
        return result[0]
    return None

def get_inventory_quantity():
    result = db.session.query(Regulation.inventory_quantity).first()
    if result:
        return result[0]
    return None

def get_add_book_quantity():
    result = db.session.query(Regulation.add_book_quantity).first()
    if result:
        return result[0]
    return None

def books_stats():
    return db.session.query(Category.id, Category.name, func.count(Book.id))\
                .join(Book, Book.category_id.__eq__(Category.id), isouter=True).group_by(Category.id).all()

if __name__ == '__main__':
    with app.app_context():
        print(revenue_time())
