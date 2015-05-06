from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
photo = Table('photo', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('filename', String(length=36)),
    Column('text', String(length=36), default=ColumnDefault('')),
    Column('copies', Integer, default=ColumnDefault(1)),
    Column('user_id', Integer),
)

order = Table('order', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('UserName', VARCHAR(length=50)),
    Column('UserPhone', VARCHAR(length=36)),
    Column('UserAddress', VARCHAR(length=500)),
    Column('UserComment', VARCHAR(length=500)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].columns['user_id'].create()
    pre_meta.tables['order'].columns['user_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].columns['user_id'].drop()
    pre_meta.tables['order'].columns['user_id'].create()
