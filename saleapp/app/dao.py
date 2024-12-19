from app.models import Category, Book, User, UserRole, Receipt, ReceiptDetail
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime

def load_categories():
    return Category.query.order_by("id").all()


def load_books(cate_id=None, kw=None, page=1):
    query = Book.query

    if kw:
        query = query.filter(Book.name.contains(kw))

    if cate_id:
        query = query.filter(Book.category_id == cate_id)

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()


def count_books():
    return Book.query.count()


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

def add_receipt(cart):
    if cart:
        r = Receipt(customer=current_user)

        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetail(quantity=c['quantity'], price=c['price'],
                               receipt=r, book_id=c['id'])
            db.session.add(d)

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


def get_book_by_id(id):
    return Book.query.get(id)



if __name__ == '__main__':
    with app.app_context():
        print(revenue_time())
