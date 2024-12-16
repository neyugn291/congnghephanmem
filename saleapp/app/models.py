import random
from stringprep import c8_set

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from app import db, app
from enum import Enum as RoleEnum
import hashlib
from flask_login import UserMixin

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    HOUSE = 3
    SELLER = 4


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.USER)


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    author = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u = User(name='admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
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
            prod = Product(name=p['name'], author=p['author'], price=p['price'],
                           image=p['image'], category_id=p['category_id'])
            db.session.add(prod)

        db.session.commit()
