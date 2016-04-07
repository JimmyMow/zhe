from app import db
from app import models

db.session.remove()
db.drop_all()
