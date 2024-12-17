
from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime, date
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, null
from app import db, app
from enum import Enum as RoleEnum
import hashlib
from flask_login import UserMixin


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    WAREHOUSE = 3
    SELLER = 4


class Location(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(255), nullable=False)  # Thành phố
    district = Column(String(255), nullable=False)  # Quận Huyện
    commune = Column(String(255), nullable=False)  # Xã
    specific = Column(String(255), nullable=False)  # Cụ thể : số nhà, số đường

    users = relationship('User', backref='location', lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    password = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255))
    phone = Column(String(255))
    location_id = Column(Integer, ForeignKey(Location.id))
    avatar = Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    orders = relationship('Order', backref='user', lazy=True)
    invoices_customer = relationship('Invoice', back_populates='customer',foreign_keys='Invoice.customer_id', lazy=True)
    invoices_seller = relationship('Invoice', back_populates='seller',foreign_keys='Invoice.seller_id', lazy=True)



class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


# class Product(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)
#     author = Column(String(255), nullable=True)
#     price = Column(Float, default=0)
#     image = Column(String(100), nullable=True)
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#
#     def __str__(self):
#         return self.name


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    author = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=True)
    description = Column(String(255), default='')
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    received_note_details = relationship('ReceivedNoteDetail', backref='book', lazy=True)

    def __str__(self):
        return self.name


class ReceivedNote(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    received_day = Column(DATETIME, default=datetime.now(), nullable=False)

    received_note_details = relationship('ReceivedNoteDetail', backref='note', lazy=True)


class ReceivedNoteDetail(db.Model):
    note_id = Column(Integer, ForeignKey(ReceivedNote.id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id), primary_key=True)
    quantity = Column(Integer, nullable=True)


class Order(db.Model):
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    order_day = Column(DATETIME, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=True)


class Invoice(db.Model):
    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    seller_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    invoice_day = Column(DATETIME, nullable=False)
    quantity = Column(Integer, nullable=False)

    customer = relationship('User', back_populates='invoices_customer', foreign_keys=[customer_id])
    seller = relationship('User', back_populates='invoices_seller', foreign_keys=[seller_id])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u = User(name='Phan Le Nguyen', username='admin',email='abc@com',phone='0123', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        c1 = Category(name='Thieu nhi')
        c2 = Category(name='Giao khoa')
        c3 = Category(name='Du ky')
        c4 = Category(name='Ky su')
        c5 = Category(name='Kinh di')
        c6 = Category(name='Ngon tinh')
        c7 = Category(name='Tho ca')
        c8 = Category(name='Tieu thuyet')
        c9 = Category(name='Trinh tham')
        c10 = Category(name='Truyen cuoi')

        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])
        db.session.commit()

        data = [{
            "name": "Khoản tiết kiệm của mẹ",
            "author": "",
            "price": 170000,
            "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846487/image-ThieuNhi_3_ova65g.jpg",
            "category_id": 1
        }, {
            "name": "Mẹ không phải người giúp việc",
            "author": "",
            "price": 160000,
            "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846486/image-ThieuNhi_2_h67bft.jpg",
            "category_id": 1
        }, {
            "name": "Nguồn năng lượng tích cực",
            "author": "",
            "price": 82000,
            "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846491/image-ThieuNhi_1_rsimyy.jpg",
            "category_id": 1
        }, {
            "name": "Bài tập tin học 6",
            "author": "",
            "price": 20000,
            "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846492/image-GiaoKhoa_3_djbatm.jpg",
            "category_id": 2
        }, {
            "name": "Tiếng viêt 3",
            "author": "",
            "price": 30000,
            "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846491/image-GiaoKhoa_2_fybyon.jpg",
            "category_id": 2
        }, {
            "name": "Bài tập ngữ văn 7",
            "author": "",
            "price": 20000,
            "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846492/image-GiaoKhoa_1_tguxox.jpg",
            "category_id": 2
        }, {
            "name": "Giấc mơ Nhật",
            "author": "",
            "price": 120000,
            "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846492/image-GiaoKhoa_3_djbatm.jpg",
            "category_id": 3
        }, {
                "name": "Châu Âu vạn dặm",
                "author": "",
                "price": 89000,
                "image": "https://res.cloudinary.com/dh8lb3zxg/image/upload/v1733846492/image-GiaoKhoa_3_djbatm.jpg",
                "category_id": 3
        }]

        for p in data:
            prod = Book(name=p['name'], author=p['author'], price=p['price'],
                           image=p['image'], category_id=p['category_id'])
            db.session.add(prod)

        db.session.commit()
