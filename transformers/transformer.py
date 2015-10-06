import os

class Transformer(object):

    @staticmethod
    def setup():
        raise NotImplementedError()

    @staticmethod
    def parse_game(game, year, week):
        raise NotImplementedError()

    @staticmethod
    def finish():
        raise NotImplementedError()

    @staticmethod
    def get_pickle_filename(classname):
        parent_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", classname)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        return os.path.join(parent_dir, classname+".pkl")

    @staticmethod
    def get_csv_filename(classname):
        parent_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", classname)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        return os.path.join(parent_dir, classname+".csv")
