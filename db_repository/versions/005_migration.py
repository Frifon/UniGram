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
    Column('timestamp', DateTime),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('UserName', String(length=50)),
    Column('UserPhone', String(length=36)),
    Column('UserAddress', String(length=500)),
    Column('UserComment', String(length=500)),
    Column('timestamp', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].columns['timestamp'].create()
    post_meta.tables['order'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].columns['timestamp'].drop()
    post_meta.tables['order'].columns['timestamp'].drop()
