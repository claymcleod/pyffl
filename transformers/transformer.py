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
