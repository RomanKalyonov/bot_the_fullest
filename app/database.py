from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (BigInteger, Column, String, sql)

from config import PG_HOST, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

db = Gino()


# Документация
# http://gino.fantix.pro/en/latest/tutorials/tutorial.html
class User(db.Model):
    __tablename__ = 'users'
    query: sql.Select

    user_id = Column(BigInteger, primary_key=True)

    @staticmethod
    async def get_or_create(user_id):
        user = await User.get(int(user_id))
        if user:
            return user
        else:
            new_user = await User.create(user_id=int(user_id))
            return new_user


async def create_db():
    await db.set_bind(f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PG_HOST}/{POSTGRES_DB}')

    # Create tables
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()  # Drop the db
    await db.gino.create_all()

