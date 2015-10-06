import os
import sys
import cPickle

datasets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "datasets")
dfs = {}
class Hook(object):

    @classmethod
    def dependencies(cls):
        return None

    @classmethod
    def run(cls):
        raise NotImplementedError()

    @classmethod
    def _execute(cls):
        for folder in cls.dependencies():
            pickle_path = os.path.join(datasets_dir, folder, folder+".pkl")
            if not os.path.exists(pickle_path):
                print "Failed due to dependency missing: %s" % (folder)
                sys.exit(-1)
            else:
                f = open(pickle_path,"rb")
                dfs[folder] = cPickle.load(f)
        cls.run()
