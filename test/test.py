import unittest
import logging
from surveillance.surveillance import Surveillance
from surveillance.imageUpload import ImageUpload

from test.cameraStub import CameraStub
from test.uploadProviderStub import UploadProviderStub

class TestSurveillance(unittest.TestCase):

    def test_sameImageGiveNoChange(self):
        #Arrange
        conf = {
                "min_area":5000,
                "delta_thresh":5
            }
        camera = CameraStub(["test/background.jpg", "test/background.jpg"])
        sut = Surveillance(conf, camera)
        sut.setBackground()
        sut.detectChange()

        changed, frame = sut.detectChange()
        
        self.assertFalse(changed)

    def test_differentImageGivesAChange(self):
        #Arrange
        conf = {
                "min_area":500,
                "delta_thresh":5
            }
        camera = CameraStub(["test/background.jpg","test/background_with_change.jpg"])
        sut = Surveillance(conf, camera)
        
        sut.setBackground()
        #Act
        sut.detectChange()
        #Assert
        changed, frame = sut.detectChange()
        
        self.assertTrue(changed)

    def test_UploadProviderFailsIsHandled(self):
        #Arrange
        conf = {
            "min_upload_seconds":0,
            "min_motion_frames":0
        }
        uploadProvider = UploadProviderStub()
        uploadProvider.ThrowException = True
        logging.basicConfig()
        sut = ImageUpload(conf, uploadProvider)
        frame = None

        #Act
        #Assert (Exception is not throwned)
        sut.Upload(frame, True)

if __name__ == '__main__':
    unittest.main()
