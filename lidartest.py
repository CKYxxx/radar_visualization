import velodyne_decoder as vd
import numpy as np
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

class LidarTestWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.view_widget = gl.GLViewWidget()
        self.layout.addWidget(self.view_widget)

    def setup_lidar_data(self, pcap_path, model):
        self.lidar_data = self.read_lidar_data(pcap_path, model)

    def read_lidar_data(self, pcap_path, model):
        config = vd.Config(model='VLP-16', rpm=600)
        cloud_arrays = []
        for stamp, points in vd.read_pcap(pcap_path, config):
            cloud_arrays.append(points)
        return cloud_arrays

    def display_lidar_data(self):
        # Assuming the point cloud data is in the format (x, y, z)
        for points in self.lidar_data:
            pos = points[:, :3]  # Extract x, y, z positions
            # Add more code here to display the point cloud

if __name__ == "__main__":
    app = QApplication([])
    window = LidarTestWindow()
    window.setup_lidar_data('/home/s0001593/Downloads/provizio/Dataset_mid_range/Lidar/velodyne.pcap', 'VLP-16')  # Replace with your actual path and model
    window.display_lidar_data()
    window.show()
    app.exec_()
