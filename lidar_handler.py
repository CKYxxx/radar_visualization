import velodyne_decoder as vd
import numpy as np
import pyqtgraph.opengl as gl
from PyQt5.QtCore import QTimer

class LidarHandler:

    def __init__(self, view_widget, lidar_time_offset, radar_frame_rate):
        self.view_widget = view_widget
        self.lidar_data = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visualization)
        self.frame_index = 0
        self.lidar_time_offset = lidar_time_offset  # Time offset specific to LiDAR
        self.radar_frame_rate = radar_frame_rate  # Frame rate of the radar

    def load_data(self, pcap_path, model):
        config = vd.Config(model=model, rpm=600)
        frame_counter = 0
        for stamp, points in vd.read_pcap(pcap_path, config):
            # Append the points to the lidar_data list
            self.lidar_data.append(points)

            # Print the timestamp and structure of the first few frames for analysis
            if frame_counter < 5:
                print(f"Frame {frame_counter}, Timestamp: {stamp}, Points shape: {points.shape}")
            
            frame_counter += 1

        print("Loaded {} frames of LiDAR data".format(len(self.lidar_data)))  # Debug print

    def start_playback(self):
        if not self.lidar_data:
            print("No LiDAR data loaded")
            return
        self.frame_index = 0
        self.timer.start(100)  # Adjust interval for frame rate

    def stop_playback(self):
        self.timer.stop()

    def update_visualization(self):
        try:
            if self.frame_index < len(self.lidar_data):
                print(f"Current LiDAR frame index: {self.frame_index}")  # Print current frame index
                self.view_widget.items.clear()
                points = self.lidar_data[self.frame_index]
                pos = points[:, :3]
                color = np.full((len(points), 4), [1, 0, 0, 1])  # Example: Red color
                scatter = gl.GLScatterPlotItem(pos=pos, color=color, size=0.1)
                self.view_widget.addItem(scatter)
                self.frame_index += 1
            else:
                self.stop_playback()  # Stop when all frames are displayed
        except Exception as e:
            print(f"Error in update_visualization: {e}")


    def update_to_match_radar(self, radar_frame_index):
        lidar_frame_index = self.calculate_lidar_index(radar_frame_index)

        if 0 <= lidar_frame_index < len(self.lidar_data):
            self.view_widget.items.clear()
            points = self.lidar_data[lidar_frame_index]
            pos = points[:, :3]
            color = np.full((len(points), 4), [1, 0, 0, 1])  # Red color
            scatter = gl.GLScatterPlotItem(pos=pos, color=color, size=0.1)
            self.view_widget.addItem(scatter)

    def calculate_lidar_index(self, radar_frame_index):
        # Convert radar frame index to time
        radar_time_seconds = radar_frame_index / self.radar_frame_rate

        # Adjust for LiDAR time offset (in seconds)
        lidar_time_seconds = radar_time_seconds + self.lidar_time_offset / 1000.0

        # Find the closest LiDAR frame index to this time
        closest_lidar_index = self.find_closest_lidar_index(lidar_time_seconds)
        return closest_lidar_index

    def find_closest_lidar_index(self, lidar_time_seconds):
        closest_lidar_index = 0
        min_time_difference = float('inf')

        for index, points in enumerate(self.lidar_data):
            # Assuming the timestamp is in the first column of the points array
            timestamp = points[0, 0]  # Assuming the first element of points is the timestamp

            time_difference = abs(lidar_time_seconds - timestamp)
            if time_difference < min_time_difference:
                min_time_difference = time_difference
                closest_lidar_index = index

        return closest_lidar_index
