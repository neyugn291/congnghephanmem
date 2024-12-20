from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = "wJjEU-Oq-vGf5fWSkbfdQ7pWM00"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4" % quote('Demo@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4



db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(
    cloud_name="dzbkb9zaz",
    api_key="591363178267761",
    api_secret="wJjEU-Oq-vGf5fWSkbfdQ7pWM00",  # Click 'View API Keys' above to copy your API secret
    secure=True
)


