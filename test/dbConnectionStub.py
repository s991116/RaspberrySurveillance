class DbConnectionStub:
    def __init__(self):
        self.table = []
        return

    def insert_one(self, data):
        self.table.append(data)