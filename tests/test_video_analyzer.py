import unittest
from unittest.mock import patch, MagicMock
from src.video_analyzer import VideoAnalyzer
from PyQt6.QtWidgets import QApplication

class TestVideoAnalyzer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.video_analyzer = VideoAnalyzer()

    @patch('cv2.VideoCapture')
    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileNames')
    def test_loadVideos(self, mock_getOpenFileNames, MockVideoCapture):
        # Mock the file dialog to return specific files
        mock_getOpenFileNames.return_value = (['video1.mp4', 'video2.mp4'], None)

        self.video_analyzer.loadVideos()
        loaded_files = [self.video_analyzer.videoList.item(i).text() for i in range(self.video_analyzer.videoList.count())]
        
        self.assertEqual(loaded_files, ['video1.mp4', 'video2.mp4'])
        print("Test loadVideos passed.")

    @patch('cv2.VideoCapture')
    def test_analyzeVideos(self, MockVideoCapture):
        mock_cap = MockVideoCapture.return_value
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 1000 if x == 0 else 30  # Mocking timestamp and fps
        
        self.video_analyzer.videoList.addItem("video1.mp4")
        self.video_analyzer.videoList.addItem("video2.mp4")
        self.video_analyzer.analyzeVideos()

        self.assertIn('Matched Videos:\nvideo1.mp4 and video2.mp4', self.video_analyzer.resultsLabel.text())
        print("Test analyzeVideos passed.")

    def tearDown(self):
        self.video_analyzer = None

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()
