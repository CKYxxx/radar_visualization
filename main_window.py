import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDockWidget
from radar_visualization import RadarVisualization
from video_player import VideoPlayer
from PyQt5.QtCore import Qt, QTimer
from ControlHandler import ControlHandler
from ui_elements import UIElements, create_color_coding_ui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Provizio Visualization")
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Initialize radar visualization with video offset
        self.radar_visualization = RadarVisualization(parent=self)
        self.radar_visualization.setup('/home/s0001593/Downloads/provizio/Dataset_mid_range/Radar/radar_fft.csv')
        self.radar_visualization.video_offset_ms = -14800  # Set the offset

        # Initialize video player and control handler
        self.video_player = VideoPlayer('/home/s0001593/Downloads/provizio/Dataset_mid_range/Camera/camera.mkv')
        self.control_handler = ControlHandler(self.radar_visualization, self.video_player)

        # Initialize UI elements
        self.ui_elements = UIElements(self.control_handler, self.video_player, self.radar_visualization)

        # Add control buttons, video slider, and color coding UI to the layout
        main_layout.addWidget(self.ui_elements.create_control_buttons())
        main_layout.addWidget(self.ui_elements.create_video_slider())
        main_layout.addWidget(create_color_coding_ui(self.radar_visualization.update_color_coding))

        # Create and add dock widgets
        self.addDockWidget(Qt.RightDockWidgetArea, self.createDockWidget("Radar Visualization", self.radar_visualization.get_widget()))
        self.addDockWidget(Qt.LeftDockWidgetArea, self.createDockWidget("Video Player", self.video_player))


    def createDockWidget(self, title, widget):
        dock_widget = QDockWidget(title, self)
        dock_widget.setWidget(widget)
        dock_widget.setFloating(True)
        return dock_widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
