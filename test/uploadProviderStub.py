class UploadProviderStub:
    ThrowException = False  

    def __init__(self):
        exit


    def Upload(self, frame, timestamp):
        if(self.ThrowException):
            raise Exception("Upload provider exception")
        exit