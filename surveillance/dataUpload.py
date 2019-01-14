class DataUpload:
    def __init__(self, dbConnection):
        self.dbConnection = dbConnection
        return

    def Upload(self, data):
        self.dbConnection.insert_one(data)
        return