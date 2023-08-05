import traceback
import os

class Service:
    def __init__(self):
        self.services = {}

    def __getattr__(self, name):
        if name not in self.services:
            if name[0]=='_':
                print('服务未找到:{}'.format(name))
                os._exit(1)
        
            try:
                method = getattr(self, "_{}".format(name))
            except AttributeError as e:
                traceback.print_exc(e)
                print('服务未找到:{}'.format(name))
                os._exit(1)
                #raise Exception('服务未找到:{}'.format(name))

            self.services[name] = method()

        return self.services.get(name)
