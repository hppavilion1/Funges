class stack(list):
    def __init__(self, *args, **kwargs):
        list.__init___(self, *args, **kwargs)

    def pop(self):
        x=self[-1]
        del self[-1]
        return x

    def push(self, item):
        self.append(item)
