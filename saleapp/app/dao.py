from app.models import Category, Book, User, UserRole, Receipt, ReceiptDetail, ReceivedNote, Comment, ReceivedNoteDetail
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
        query = query.filter(Book.name.like(f"{kw}%"))

    if cate_id:
        query = query.filter(Book.category_id == cate_id)

    if not page_size:
        page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

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
        r = Receipt(customer=current_user, received_day = func.now())

        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetail(quantity=c['quantity'], price=c['price'],
                               receipt=r, book_id=c['id'])
            db.session.add(d)

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
            rd = ReceiptDetail(receipt=rec , book_id=int(r['book_id']), quantity=r['quantity'], price=float(r['price']))

            db.session.add(rd)

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

    db.session.commit()


def revenue_stats():
    return db.session.query(Book.id, Book.name, func.sum(ReceiptDetail.quantity * ReceiptDetail.price))\
                     .join(ReceiptDetail, ReceiptDetail.book_id.__eq__(Book.id)).group_by(Book.id).all()


def revenue_time(time='month', year=datetime.now().year):
    return db.session.query(func.extract(time, Receipt.created_date),
                            func.sum(ReceiptDetail.quantity * ReceiptDetail.price))\
                    .join(ReceiptDetail,
                          ReceiptDetail.receipt_id.__eq__(Receipt.id)).filter(func.extract("year", Receipt.created_date).__eq__(year))\
                    .group_by(func.extract(time, Receipt.created_date)).order_by(func.extract(time, Receipt.created_date)).all()


def books_stats():
    return db.session.query(Category.id, Category.name, func.count(Book.id))\
                .join(Book, Book.category_id.__eq__(Category.id), isouter=True).group_by(Category.id).all()


def load_comments(book_id):
    return Comment.query.filter(Comment.book_id.__eq__(book_id)).order_by(-Comment.id).all()


def add_comment(content, book_id):
    c = Comment(content=content, book_id=book_id, user=current_user, created_date = datetime.now())
    db.session.add(c)
    db.session.commit()

    return c

if __name__ == '__main__':
    with app.app_context():
        print(revenue_time())
