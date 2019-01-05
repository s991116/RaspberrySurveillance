import unittest
from surveillance.surveillance import Surveillance
from cameraStub import CameraStub

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

if __name__ == '__main__':
    unittest.main()