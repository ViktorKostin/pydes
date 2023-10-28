from __future__ import annotations
import copy

my_funcs = []
products = {}
new_attrs = {}
temp = []
factories = []


class AbstractFactory(type):
    def __new__(cls, clsname, bases, attrs):
        # def before_creation(self): ...
        # def after_creation(self): ...
        # def init(self):
        #     before_creation()
        #     super(self).__init__()
        #     after_creation()
        for attr, v in attrs.items():
            if attr.endswith('_create'):
                attr = attr.split('_create')[0]
                temp.append(v)
            if attr == 'before_creation':
                before_creation = v
            elif attr == 'after_creation':
                after_creation = v
            if attr.startswith('before_creation') and attr != 'before_creation':
                fn_last_name = attr.split('before_creation')[1][1:]
                if len(fn_last_name) > 1:
                    if products.get(fn_last_name, None):
                        products[fn_last_name].update({'before_creation': v})
                    else:
                        products[fn_last_name] = {'before_creation': v}
            if attr.startswith('after_creation') and attr != 'after_creation':
                fn_last_name = attr.split('after_creation')[1][1:]
                if len(fn_last_name) > 1:
                    if products.get(fn_last_name, None):
                        products[fn_last_name].update({'after_creation': v})
                    else:
                        products[fn_last_name] = {'after_creation': v}

        class Bridge:
            ...

        bridge = Bridge()
        for list_v in zip(*temp):
            name = 'Factory' + list_v[0].__name__.split('_')[-1]
            temp_class = type(list_v[0].__name__, (), {})
            for idx, v in enumerate(list_v):
                new_attrs[name] = bridge
                creator_name = v.__name__.split('_')[0]
                funcs = products.get(v.__name__, None)
                print(funcs)
                # print(funcs)
                if funcs:
                    print('from funcs')
                    specific_before_creation = funcs.get('before_creation', None)
                    specific_after_creation = funcs.get('after_creation', None)
                    if specific_before_creation:
                        print(specific_before_creation)
                    if specific_after_creation:
                        print(specific_after_creation)

                    def init(obj, *args, **kwargs):
                        print('test')
                        if specific_before_creation:
                            print('fuzzz')
                            specific_before_creation(obj)
                        super(type(obj), obj).__init__(*args, **kwargs)
                        if specific_after_creation:
                            specific_after_creation(obj)
                else:
                    def init(obj, *args, **kwargs):
                        before_creation(obj)
                        print('ok')
                        super(type(obj), obj).__init__(*args, **kwargs)
                        after_creation(obj)
                # print(init)
                # CopyOf_v = type(v.__name__, v.__bases__, dict(v.__dict__).update({'__init__', init}))
                my_funcs.append(init)
                CopyOf_v = type(v.__name__, v.__class__.__bases__, dict(v.__dict__))
                if locals().get('init', None):
                    CopyOf_v.__init__ = my_funcs[idx]
                # print(my_funcs)
                import inspect
                # d = dict(v.__dict__)
                # d.update({'__init__': my_funcs[idx]})
                # CopyOf_v = type(v.__name__, v.__class__.__bases__, d)
                # CopyOf_v.__init__ = my_funcs[idx]
                # # CopyOf_v.__init__ = copy.copy(init)
                # new_attrs[name].__setattr__('__init__', T.__init__)
                setattr(CopyOf_v, '__init__', my_funcs[idx])
                new_attrs[name].__setattr__(creator_name, CopyOf_v)
                newclass = super(AbstractFactory, cls).__new__(cls, clsname, bases, new_attrs)
        # for my_func in my_funcs:
        #     print(my_func)
        #     print(inspect.getsource(my_func))
        return newclass

    # def __init_subclass__(cls):
    #     super().before_creation_CCP_Server2()
    def __attr_collection(cls, attr_name=None, v=None, attrs={}):
        attr_exist = attrs.get(attr_name, None)
        if not attr_exist:
            attrs[attr_name] = v
        return attrs


class AbstractProduct(type):
    def __new__(cls, clsname, bases, attrs):
        new_attrs = {}
        temp = []
        for attr, v in attrs.items():
            new_attrs[attr] = v
        clsname = clsname.split('_')[-1]
        # print(clsname)
        # if attr.endswith('_create'):
        #     attr = attr.split('_create')[0]
        #     temp.append(v)
        # for idx, v in enumerate(zip(*temp)):
        #     name = v[0].__name__.split('_')[-1]
        #     new_attrs[name] = v
        return super(AbstractProduct, cls).__new__(cls, clsname, bases, new_attrs)

    def __attr_collection(cls, attr_name=None, v=None, attrs={}):
        attr_exist = attrs.get(attr_name, None)
        if not attr_exist:
            attrs[attr_name] = v
        return attrs


class Server:
    def __init__(self):
        self.create()

    def create(self):
        print(self.__class__.__name__)


class S3(Server): ...


class S3_Server1(S3): ...


class S3_Server2(S3): ...


class S3_Server3(S3): ...


class S3_Server4(S3): ...


class GCP(Server): ...


class GCP_Server1(GCP): ...


class GCP_Server2(GCP): ...


class GCP_Server3(GCP): ...


class GCP_Server4(GCP): ...


class CCP(Server): ...


class CCP_Server1(GCP): ...


class CCP_Server2(GCP): ...


class CCP_Server3(GCP): ...


class CCP_Server4(GCP): ...


class ServerFactories(metaclass=AbstractFactory):
    S3_create = [S3_Server1, S3_Server2, S3_Server3, S3_Server4]
    GCP_create = [GCP_Server1, GCP_Server2, GCP_Server3, GCP_Server4]
    CCP_create = [CCP_Server1, CCP_Server2, CCP_Server3, CCP_Server4]

    def before_creation(self):
        print('bum')

    def after_creation(self):
        print('zoom')

    def before_creation_CCP_Server2(self):
        # print(self.after_creation_GCP_Server2)
        print('\n\nYEP! before {}\n\n'.format(self.__class__.__name__))

    def after_creation_CCP_Server2(self):
        print('\n\nYEP! after {}\n\n'.format(self.__class__.__name__))
        # print(self.after_creation_GCP_Server2)
        # print('\n\nYEP! after CCP_Server2\n\n')

    def before_creation_GCP_Server2(self):
        # print(self.after_creation_GCP_Server2)
        print('\n\nYEP! before {}\n\n'.format(self.__class__.__name__))

    def after_creation_GCP_Server2(self): ...
    # print(self.after_creation_GCP_Server2)
    # print('\n\nYEP! after GCP_Server2\n\n')


server_factories = ServerFactories()
# server_factories.FactoryServer1.CCP()
server_factories.FactoryServer2.CCP()
print(server_factories.FactoryServer2.CCP.__dict__)
# server_factories.FactoryServer2.GCP()
# server_factories.FactoryServer3.CCP()
# server_factories.FactoryServer4.CCP()
