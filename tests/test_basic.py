from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import types
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from unittest import TestCase

from outcast import DetachedModel


metadata = MetaData()
BaseModel = declarative_base()
engine = create_engine('postgresql+psycopg2:///outcast', echo=True)
Session = sessionmaker(bind=engine)


if True:
    class Model(BaseModel):
        __tablename__ = 'model'

        id = Column(types.Integer, primary_key=True)
        name = Column(types.String)
        description = Column(types.String)

        @property
        def fancy_name(self):
            return self.name + '...so fancy!'

        def get_greeting(self, prefix):
            return '%s, %s!' % (prefix, self.name)

else:
    model = Table('model', metadata,
        Column('id', types.Integer, primary_key=True),
        Column('name', types.String),
        Column('description', types.String),
    )

    class Model(object):
        def __init__(self, name, description=None):
            self.name = name
            self.description = description

        @property
        def fancy_name(self):
            return self.name + '...so fancy!'

        def get_greeting(self, prefix):
            return '%s, %s!' % (prefix, self.name)

    mapper(Model, model)


if False:
    class DetachedModel(DetachedModel):
        __attached_model__ = Model


class FooTest(TestCase):

    def test_begin(self):
        session = Session()
        session.begin(subtransactions=True)


def smart_begin_nested(session):
    session.begin(subtransactions=True, nested=False)

class BasicTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        engine.echo = False
        session = Session()
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        cls.existing_name = 'Matt'
        bm = Model(name=cls.existing_name, description='')
        session.add(bm)
        session.commit()
        engine.echo = True

    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.rollback()

    def test_begin(self):
        print('\n==========')

        smart_begin_nested(self.session)
        import ipdb; ipdb.set_trace()
        bm1 = self.session.query(Model).filter_by(name=self.existing_name).first()

        smart_begin_nested(self.session)

        bm2 = self.session.query(Model).filter_by(name=self.existing_name).first()
        self.session.rollback()

        self.session.rollback()
        print('==========')


    def test_columns(self):
        import ipdb; ipdb.set_trace()
        bm = self.session.query(Model).filter_by(name=self.existing_name).first()
        #dmb = DetachedModel(bm)
        #self.assertEqual(dmb.name, self.existing_name)

    def test_properties(self):
        bm = self.session.query(Model).filter_by(name=self.existing_name).first()
        #dmb = DetachedModel(bm)
        #self.assertEqual(dmb.fancy_name, self.existing_name + '...so fancy!')

    def test_methods(self):
        bm = self.session.query(Model).filter_by(name=self.existing_name).first()
        #dmb = DetachedModel(bm)
        #self.assertEqual(dmb.get_greeting('Hello'), 'Hello, %s!' % self.existing_name)


