import sys
from PyQt6.QtWidgets import QApplication
from src.video_analyzer import VideoAnalyzer

def main():
    app = QApplication(sys.argv)
    window = VideoAnalyzer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
