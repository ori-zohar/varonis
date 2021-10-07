from collections import UserList


class MagicList(UserList):

    def __init__(self, cls_type=None):
        super().__init__()
        self._cls_type = cls_type

    def __setitem__(self, i, item):
        if len(self.data) == i or i == -1:
            self.data.append(item)
        else:
            super().__setitem__(i, item)

    def __getitem__(self, i):
        if len(self.data) == i or i == -1:
            self.data.append(self._cls_type())
        return super().__getitem__(i)
