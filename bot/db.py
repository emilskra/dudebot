import os
import sqlalchemy as db

engine = db.create_engine(os.getenv("DATABASE_URL"))
