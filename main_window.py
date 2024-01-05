import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDockWidget
from radar_visualization import RadarVisualization
from video_player import VideoPlayer
from lidar_handler import LidarHandler
from PyQt5.QtCore import Qt, QTimer
from ControlHandler import ControlHandler
from ui_elements import UIElements, create_color_coding_ui
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Provizio Visualization")
        # Initialize the first_update attribute
        self.first_update = True
        
        self.time_offsets = {
            'velodyne': 4550,   # +4.55s
            'oxts': 2050,       # +2.05s
            'camera': -14800    # -14.8s
        }
        self.sensor_extrinsics = {
            'radar': {
                'position': {'x': 1.98, 'y': -0.005, 'z': 1.36},
                'orientation': {'yaw': 0, 'pitch': 0, 'roll': 0}
            },
            'velodyne': {
                'position': {'x': 1.158, 'y': 0.0, 'z': 1.65},
                'orientation': {'yaw': 1, 'pitch': 0, 'roll': 0}
            },
            'camera': {
                'position': {'x': 1.602, 'y': 0.106, 'z': 1.72},
                'orientation': {'yaw': 0, 'pitch': 2, 'roll': 0}
            }
        }
        
        self.frame_rate = 10  # Radar frame rate in Hz

        self.initUI()
        self.visualization_timer = QTimer(self)
        self.visualization_timer.timeout.connect(self.update_visualization)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Single GLViewWidget for both Radar and LiDAR
        self.visualization_widget = GLViewWidget()

        # Instantiate RadarVisualization
        self.radar_visualization = RadarVisualization(self.visualization_widget, frame_rate=self.frame_rate, video_offset_ms=self.time_offsets['camera'],sensor_extrinsics=self.sensor_extrinsics)
        self.radar_visualization.setup('/home/s0001593/Downloads/provizio/Dataset_mid_range/Radar/radar_fft.csv')

        # Instantiate VideoPlayer
        self.video_player = VideoPlayer('/home/s0001593/Downloads/provizio/Dataset_mid_range/Camera/camera.mkv')
        self.video_player.set_offset(self.time_offsets['camera'])

        # Instantiate LidarHandler using the same GLViewWidget from RadarVisualization
        self.lidar_handler = LidarHandler(self.visualization_widget, self.time_offsets['velodyne'], self.frame_rate,self.sensor_extrinsics)
        self.lidar_handler.load_data('/home/s0001593/Downloads/provizio/Dataset_mid_range/Lidar/velodyne.pcap', 'VLP-16')

        # Instantiate ControlHandler
        self.control_handler = ControlHandler(self.radar_visualization, self.video_player, self.lidar_handler, self)
        self.radar_visualization.set_control_handler(self.control_handler)

        # UI Elements
        self.ui_elements = UIElements(self.control_handler, self.video_player, self.radar_visualization)
        main_layout.addWidget(self.ui_elements.create_control_buttons())
        main_layout.addWidget(self.ui_elements.create_video_slider())
        main_layout.addWidget(create_color_coding_ui(self.radar_visualization.update_color_coding))

        # Add Radar Visualization and Video Player as dock widgets
        self.addDockWidget(Qt.TopDockWidgetArea, self.createDockWidget("Visualization", self.visualization_widget))
        self.addDockWidget(Qt.BottomDockWidgetArea, self.createDockWidget("Video Player", self.video_player))

    def update_visualization(self):
        # Clear previous visualization items
        # self.visualization_widget.items.clear()

        # Update radar visualization
        self.radar_visualization.update()
        self.radar_visualization.redraw_current_frame()
        # In autoplay mode, update LiDAR independently
        self.lidar_handler.update_visualization()
        # Update LiDAR visualization to match the current radar frame only once at the start
        # Subsequent updates will be independent in autoplay
        # if self.first_update:
        #     current_radar_frame = self.radar_visualization.get_current_frame_index()
        #     self.lidar_handler.update_to_match_radar(current_radar_frame)
        #     self.lidar_handler.redraw_current_frame()
        #     self.first_update = False

   
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
