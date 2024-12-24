from datetime import datetime, date, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, null, DateTime, Text
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

    def __repr__(self):
        return f"{self.city}, {self.district}, {self.commune}, {self.specific}"
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(255))
    phone = Column(String(255))
    location_id = Column(Integer, ForeignKey(Location.id))
    avatar = Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    received_notes = relationship('ReceivedNote', backref='warehouse',lazy=True)
    orders = relationship('Order', backref='user', lazy=True)
    receipts_customer = relationship('Receipt', back_populates='customer',foreign_keys='Receipt.customer_id', lazy=True)
    receipts_seller = relationship('Receipt', back_populates='seller',foreign_keys='Receipt.seller_id', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name

class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    author = Column(String(255), nullable=False, default="")
    price = Column(Float, default=0)
    image = Column(String(100), nullable=False, default="")
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    received_note_details = relationship('ReceivedNoteDetail', backref='book', lazy=True)
    order_details = relationship('OrderDetail', backref='book', lazy=True)
    receipts_details = relationship('ReceiptDetail', backref='book', lazy=True)
    comments = relationship('Comment', backref='book', lazy=True)
    def __str__(self):
        return self.name




class ReceivedNote(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(Integer, ForeignKey(User.id), nullable=False)
    received_day = Column(DateTime, default=datetime.now())
    received_note_details = relationship('ReceivedNoteDetail', backref='received_note', lazy=True)


class ReceivedNoteDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    note_id = Column(Integer, ForeignKey(ReceivedNote.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    quantity = Column(Integer, nullable=False)


class Order(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    order_day = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    details = relationship('OrderDetail', backref='order',lazy=True)


class Regulation(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_cancel_time = Column(Integer, default=48)
    add_book_quantity = Column(Integer, default=150)
    iventory_quantity = Column(Integer, default=300)
    def get_order_cancel_time(self):
        return timedelta(hours=self.order_cancel_time)

class OrderDetail (db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, default=0)



class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    seller_id = Column(Integer, ForeignKey(User.id))
    created_date = Column(DateTime, default=datetime.now())

    customer = relationship('User', back_populates='receipts_customer', foreign_keys=[customer_id])
    seller = relationship('User', back_populates='receipts_seller', foreign_keys=[seller_id])
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)

class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, default=0)

class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        r = Regulation(order_cancel_time = 50,add_book_quantity=160,iventory_quantity=170)
        db.session.add(r)
        u = User(name='Phan Le Nguyen', username='admin', email='abc@com', phone='0123',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        location = [{
            "city":"Thành Phố Hồ Chí Minh",
            "district": "Nhà Bè",
            "commune":"xã Nhơn Đức",
            "specific": "Khu dân cư Nhơn Đức"
        }, {
            "city": "Thành Phố Hồ Chí Minh",
            "district": "Quận 01",
            "commune": "Phường Cô Giang",
            "specific": "35-37 Hồ Hảo Hớn"
        }, {
            "city": "Thành Phố Hồ Chí Minh",
            "district": "Quận 3",
            "commune": "Phường Võ Thị Sáu",
            "specific": "97 Võ Văn Tần"
        }, {
            "city": "Thành Phố Hồ Chí Minh",
            "district": "Quận 1",
            "commune": "Phường Đa Kao",
            "specific": "02 Mai Thị Lựu"
        }, {
            "city": "Bình Dương",
            "district": "Thành phố Thủ Dầu Một",
            "commune": "Phường Phú Lợi",
            "specific": "68 Lê Thị Trung"
        }, {
            "city": "Đồng Nai",
            "district": "Thành phố Biên Hòa",
            "commune": "Phường Long Bình Tân",
            "specific": "Đường số 9"
        }, {
            "city": "Khánh Hòa",
            "district": "Thị xã Ninh Hòa",
            "commune": "phường Ninh Hiệp",
            "specific": "Tổ dân phố 17"
        }]

        for l in location:
            loca = Location(city=l['city'],
                            district=l['district'],
                            commune=l['commune'],
                            specific=l['specific']
                            )
            db.session.add(loca)
        db.session.commit()
        c0 = Category(name='Default Book')
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
