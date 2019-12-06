import os


def load_fixture(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "fixtures", path), "r") as fd:
        return fd.read().encode("utf-8")
