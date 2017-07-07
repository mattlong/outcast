__version__ = '0.0.1'


class DetachedModel(object):
    __attached_model__ = None
    __ignore__ = ['__init__']

    def __init__(self, attached_obj):
        if self.__attached_model__ is None:
            raise TypeError('base class DetachedModel cannot be instantiated')
        elif not isinstance(attached_obj, self.__attached_model__):
            raise ValueError('attached_obj must be of type %s' % self.__attached_model__)

        self._values = {}
        for column in attached_obj.__table__.columns:
            self._values[column.name] = getattr(attached_obj, column.name)

    class __metaclass__(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            cls.__ignore__ = set(cls.__ignore__ or [])

            attached_model = cls.__attached_model__

            # don't do anything for base DetachedModel class creation
            if attached_model is None:
                return

            # table columns
            def make_column_proxy(name):
                def proxy(self):
                    return self._values[name]
                return proxy

            for column in attached_model.__table__.columns:
                setattr(cls, column.name, property(make_column_proxy(column.name)))

            # properties and methods
            for name, value in vars(attached_model).items():
                # property
                if isinstance(value, property):
                    setattr(cls, name, value)

                # method
                elif hasattr(value, '__call__') and name not in cls.__ignore__:
                    setattr(cls, name, value)
