import os

class KeyValueStorage(dict):
    def __init__(self, path):
        self._path = os.path.abspath(path)
        if not os.path.isfile(self._path):
            with open(self._path, 'w'):
                f.write(str())
        assert os.path.isfile(self._path)

        super().__init__()
        with open(self._path, 'r') as f:
            items = [item.split('\n') for item in f.read().split('\n\n')]
            if len(items) == 1 and len(items[0]) == 1 and items[0][0] == str():
                items = list()
            for item in items:
                assert len(item) == 2
                self.__setitem__(str(eval(item[0])), str(eval(item[1])))

    def store(self):
        assert os.path.isdir(os.path.dirname(self._path))
        _repr = '\n\n'.join(['\n'.join(list(map(lambda s: repr(str(s)), item))) for item in self.items()])
        with open(self._path, 'w') as f:
            f.write(_repr)
