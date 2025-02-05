import os
import cv2  # Ensure OpenCV is installed: pip install opencv-python
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog, QListWidget, QLabel

class VideoAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the window title and geometry
        self.setWindowTitle('Video Analyzer Tool')
        self.setGeometry(100, 100, 800, 600)
        
        # Create a vertical layout
        self.layout = QVBoxLayout()
        
        # Add a button to load videos
        self.loadButton = QPushButton('Load Videos', self)
        self.loadButton.clicked.connect(self.loadVideos)
        self.layout.addWidget(self.loadButton)
        
        # Add a list widget to display loaded videos
        self.videoList = QListWidget(self)
        self.layout.addWidget(self.videoList)
        
        # Add a button to analyze videos
        self.analyzeButton = QPushButton('Analyze Videos', self)
        self.analyzeButton.clicked.connect(self.analyzeVideos)
        self.layout.addWidget(self.analyzeButton)
        
        # Add a label to display results
        self.resultsLabel = QLabel('Results will be displayed here.', self)
        self.layout.addWidget(self.resultsLabel)
        
        # Set the layout to a central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def loadVideos(self):
        try:
            # Open a file dialog to select video files
            files, _ = QFileDialog.getOpenFileNames(self, 'Open Video Files', '', 'Video Files (*.mp4 *.avi)')
            if files:
                # Add selected files to the video list
                for file in files:
                    self.videoList.addItem(file)
            print("Videos loaded successfully:", files)  # Debug print
        except Exception as e:
            print("Error loading videos:", e)

    def analyzeVideos(self):
        try:
            # Get the list of loaded videos
            videos = [self.videoList.item(i).text() for i in range(self.videoList.count())]
            if len(videos) < 2:
                self.resultsLabel.setText('Please load at least two videos to analyze.')
                return
            
            metadata_list = []
            for video in videos:
                cap = cv2.VideoCapture(video)
                if cap.isOpened():
                    # Extract metadata from the video
                    metadata = {
                        'filename': os.path.basename(video),
                        'fps': cap.get(cv2.CAP_PROP_FPS),
                        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                        'duration': cap.get(cv2.CAP_PROP_POS_MSEC),
                    }
                    metadata_list.append(metadata)
                cap.release()
            
            results = 'Matched Videos:\n'
            for i in range(len(metadata_list)):
                for j in range(i + 1, len(metadata_list)):
                    # Compare the duration of videos to find matches
                    if abs(metadata_list[i]['duration'] - metadata_list[j]['duration']) < 1000:
                        results += f"{metadata_list[i]['filename']} and {metadata_list[j]['filename']}\n"
            
            # Display the results
            self.resultsLabel.setText(results if results != 'Matched Videos:\n' else 'No matches found.')
            print("Video analysis complete.")  # Debug print
        except Exception as e:
            print("Error analyzing videos:", e)

# if __name__ == "__main__":