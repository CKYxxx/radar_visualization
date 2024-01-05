import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDockWidget
from radar_visualization import RadarVisualization
from video_player import VideoPlayer
from lidar_handler import LidarHandler
from PyQt5.QtCore import Qt
from ControlHandler import ControlHandler
from ui_elements import UIElements, create_color_coding_ui
import pyqtgraph.opengl as gl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Provizio Visualization")

        self.time_offsets = {
            'velodyne': 4550,   # +4.55s
            'oxts': 2050,       # +2.05s
            'camera': -14800    # -14.8s
        }
        self.frame_rate = 10  # Radar frame rate in Hz

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Instantiate RadarVisualization
        self.radar_visualization = RadarVisualization(parent=self, frame_rate=self.frame_rate, video_offset_ms=self.time_offsets['camera'])
        self.radar_visualization.setup('/home/s0001593/Downloads/provizio/Dataset_mid_range/Radar/radar_fft.csv')

        # Instantiate VideoPlayer
        self.video_player = VideoPlayer('/home/s0001593/Downloads/provizio/Dataset_mid_range/Camera/camera.mkv')
        self.video_player.set_offset(self.time_offsets['camera'])

        # Instantiate LidarHandler using the same GLViewWidget from RadarVisualization
        self.lidar_handler = LidarHandler(self.radar_visualization.get_widget(),self.time_offsets['velodyne'],self.frame_rate)
        self.lidar_handler.load_data('/home/s0001593/Downloads/provizio/Dataset_mid_range/Lidar/velodyne.pcap', 'VLP-16')

        # Instantiate ControlHandler
        self.control_handler = ControlHandler(self.radar_visualization, self.video_player, self.lidar_handler)
        self.radar_visualization.set_control_handler(self.control_handler)

        # UI Elements
        self.ui_elements = UIElements(self.control_handler, self.video_player, self.radar_visualization)
        main_layout.addWidget(self.ui_elements.create_control_buttons())
        main_layout.addWidget(self.ui_elements.create_video_slider())
        main_layout.addWidget(create_color_coding_ui(self.radar_visualization.update_color_coding))

        # Add Radar Visualization and Video Player as dock widgets
        self.addDockWidget(Qt.RightDockWidgetArea, self.createDockWidget("Radar Visualization", self.radar_visualization.get_widget()))
        self.addDockWidget(Qt.LeftDockWidgetArea, self.createDockWidget("Video Player", self.video_player))

    def createDockWidget(self, title, widget):
        dock_widget = QDockWidget(title, self)
        dock_widget.setWidget(widget)
        dock_widget.setFloating(True)
        dock_widget.resize(800, 600)
        return dock_widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
