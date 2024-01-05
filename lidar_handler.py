import velodyne_decoder as vd
import numpy as np
import pyqtgraph.opengl as gl

class LidarHandler:
    def __init__(self, view_widget, lidar_time_offset, radar_frame_rate):
        self.view_widget = view_widget
        self.lidar_data = []
        self.frame_index = 0
        self.lidar_time_offset = lidar_time_offset
        self.radar_frame_rate = radar_frame_rate
        self.scatter_plot = None  # Initialize scatter_plot here

    def load_data(self, pcap_path, model):
        config = vd.Config(model=model, rpm=600)
        frame_counter = 0
        for stamp, points in vd.read_pcap(pcap_path, config):
            self.lidar_data.append(points)
            if frame_counter < 5:
                print(f"Frame {frame_counter}, Timestamp: {stamp}, Points shape: {points.shape}")
            frame_counter += 1
        print("Loaded {} frames of LiDAR data".format(len(self.lidar_data)))

    def update_visualization(self):
        if self.frame_index < len(self.lidar_data):
            points = self.lidar_data[self.frame_index]
            # Filter points where X > 0
            filtered_points = points[points[:, 0] > 0]

            pos = filtered_points[:, :3]
            color = np.full((len(filtered_points), 4), [1, 0, 0, 1])  # Example: Red color

            if self.scatter_plot is None:
                self.scatter_plot = gl.GLScatterPlotItem(pos=pos, color=color, size=0.1)
                self.view_widget.addItem(self.scatter_plot)
            else:
                self.scatter_plot.setData(pos=pos, color=color)

            self.frame_index += 1
        else:
            self.stop_playback()  # Stop when all frames are displayed




    def update_visualization_for_frame(self, frame_index):
        if 0 <= frame_index < len(self.lidar_data):
            self.view_widget.items.clear()
            points = self.lidar_data[frame_index]
            pos = points[:, :3]
            color = np.full((len(points), 4), [1, 0, 0, 1])  # Red color
            scatter = gl.GLScatterPlotItem(pos=pos, color=color, size=0.1)
            self.view_widget.addItem(scatter)
        else:
            print(f"LiDAR frame index {frame_index} is out of range.")

    def update_to_match_radar(self, radar_frame_index):
        lidar_frame_index = self.calculate_lidar_index(radar_frame_index)
        self.update_visualization_for_frame(lidar_frame_index)

    def calculate_lidar_index(self, radar_frame_index):
        radar_time_seconds = radar_frame_index / self.radar_frame_rate
        lidar_time_seconds = radar_time_seconds + self.lidar_time_offset / 1000.0
        return self.find_closest_lidar_index(lidar_time_seconds)

    def find_closest_lidar_index(self, lidar_time_seconds):
        closest_lidar_index = 0
        min_time_difference = float('inf')
        for index, points in enumerate(self.lidar_data):
            timestamp = points[0, 0]
            time_difference = abs(lidar_time_seconds - timestamp)
            if time_difference < min_time_difference:
                min_time_difference = time_difference
                closest_lidar_index = index
        return closest_lidar_index
    def redraw_current_frame(self):
        # Check if the current frame index is valid
        if 0 <= self.frame_index < len(self.lidar_data):
            # Get data for the current frame
            points = self.lidar_data[self.frame_index]
            # Update the scatter plot for this frame
            self.update_visualization_for_frame(self.frame_index)
        else:
            print(f"LiDAR frame index {self.frame_index} is out of range.")
    def set_frame_index(self, frame_index):
        if 0 <= frame_index < len(self.lidar_data):
            self.frame_index = frame_index
        else:
            print("Invalid LiDAR frame index:", frame_index)