class Test:
    def __init__(self):
        self.lst = (1,2,3)

    def get_list(self):
        return self.lst

x = Test()
lst = tuple(x.get_list())
lst.append(4)
print x.get_list()
