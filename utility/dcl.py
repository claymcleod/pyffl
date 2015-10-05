class DynamicClassLoader(object):

    @staticmethod
    def import_transformer(name):
        mod = __import__("transformers")
        instance = getattr(mod, name)
        return instance
