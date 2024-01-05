import velodyne_decoder as vd
import numpy as np
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer

class LidarTestWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.view_widget = gl.GLViewWidget()
        self.layout.addWidget(self.view_widget)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.frame_index = 0

    def setup_lidar_data(self, pcap_path, model):
        self.lidar_data = self.read_lidar_data(pcap_path, model)

    def read_lidar_data(self, pcap_path, model):
        config = vd.Config(model=model, rpm=600)
        cloud_arrays = []
        for stamp, points in vd.read_pcap(pcap_path, config):
            cloud_arrays.append(points)
        return cloud_arrays

    def start_playback(self):
        self.timer.start(110)  # Adjust the interval as needed

    def stop_playback(self):
        self.timer.stop()

    def update_display(self):
        if self.frame_index < len(self.lidar_data):
            self.view_widget.items.clear()  # Clear existing points
            points = self.lidar_data[self.frame_index]
            pos = points[:, :3]  # Extract x, y, z positions
            color = np.full((len(points), 4), [1, 0, 0, 1])  # Example: Red color
            scatter = gl.GLScatterPlotItem(pos=pos, color=color, size=0.1)
            self.view_widget.addItem(scatter)
            self.frame_index += 1
        else:
            self.stop_playback()  # Stop when all frames are displayed

    def display_lidar_data(self):
        self.start_playback()  # Start displaying data

if __name__ == "__main__":
    app = QApplication([])
    window = LidarTestWindow()
    window.setup_lidar_data('/home/s0001593/Downloads/provizio/Dataset_mid_range/Lidar/velodyne.pcap', 'VLP-16')  # Replace with your actual path and model
    window.display_lidar_data()
    window.show()
    app.exec_()
