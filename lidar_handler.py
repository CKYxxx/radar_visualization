import velodyne_decoder as vd
import numpy as np
import pyqtgraph.opengl as gl
import csv

class LidarHandler:
    def __init__(self, view_widget, lidar_time_offset, radar_frame_rate,sensor_extrinsics):
        self.view_widget = view_widget
        self.lidar_data = []
        self.frame_index = 0
        self.lidar_time_offset = lidar_time_offset
        self.radar_frame_rate = radar_frame_rate
        self.scatter_plot = None  # Initialize scatter_plot here
        self.lidar_timestamps = [] 
        self.sensor_extrinsics = sensor_extrinsics
    def load_data(self, pcap_path, model):
        config = vd.Config(model=model, rpm=600)
        frame_counter = 0
        for stamp, points in vd.read_pcap(pcap_path, config):
            self.lidar_data.append(points)
            self.lidar_timestamps.append(stamp)
            # print(f"Loading frame {frame_counter}: Timestamp: {stamp}")  # Debug print
            if frame_counter < 5:
                print(f"Frame {frame_counter}, Timestamp: {stamp}, Points shape: {points.shape}")
            frame_counter += 1
        # self.save_lidar_times_to_csv('lidar_time.csv')
        # print("Loaded {} frames of LiDAR data".format(len(self.lidar_data)))

    def update_visualization(self):
        if self.frame_index < len(self.lidar_data):
            points = self.lidar_data[self.frame_index]
            # Filter points where X > 0
            filtered_points = points[points[:, 0] > 0]

            # Extract 'x', 'y', and 'z' values
            x_values = filtered_points[:, 0]
            y_values = filtered_points[:, 1]
            z_values = filtered_points[:, 2]

            # Create a new array with 'x', 'y', 'z' values
            xyz_values = np.column_stack((x_values, y_values, z_values))

            pos = xyz_values  # Use the new 'xyz_values' array
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

    
    def update_to_match_radar(self, frame_index):
        """ Update LiDAR visualization to match the given frame index """
        # Directly use the provided frame index for updating LiDAR visualization
        self.update_visualization_for_frame(frame_index)

    # def update_to_match_radar(self, radar_frame_index):
    #     lidar_frame_index = self.calculate_lidar_index(radar_frame_index)
    #     self.update_visualization_for_frame(lidar_frame_index)
    def calculate_lidar_index(self, radar_frame_index):
        closest_lidar_index = radar_frame_index + 45
        # print(f"xxx Calculating LiDAR index for radar frame index: {radar_frame_index}")

        # # Calculate the corresponding LiDAR time using radar frame index, frame rate, and offset
        # radar_time_seconds = radar_frame_index / self.radar_frame_rate
        # lidar_time_seconds = radar_time_seconds + self.lidar_time_offset / 1000.0
        # print(f"xxx Radar time (s): {radar_time_seconds}, LiDAR time (s): {lidar_time_seconds}")

        # # Find the closest LiDAR index to the calculated LiDAR time
        # closest_lidar_index = self.find_closest_lidar_index(lidar_time_seconds)
        # print(f"xxx Closest LiDAR frame index: {closest_lidar_index}")

        return closest_lidar_index

    def find_closest_lidar_index(self, lidar_time_seconds):
        # print(f"Finding closest LiDAR index for LiDAR time (s): {lidar_time_seconds}")

        closest_lidar_index = 0
        min_time_difference = float('inf')
        for index, points in enumerate(self.lidar_data):
            # Assuming the first element of points represents the timestamp
            timestamp = points[0, 0]  # Adjust this based on your data structure
            time_difference = abs(lidar_time_seconds - timestamp)
            # print(f"LiDAR frame {index}: timestamp = {timestamp}, time difference = {time_difference}")

            if time_difference < min_time_difference:
                min_time_difference = time_difference
                closest_lidar_index = index

        # print(f"Closest LiDAR frame index: {closest_lidar_index}, with time difference: {min_time_difference}")
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

    def stop_playback(self):
        # Logic to stop the LiDAR playback
        # For example, you might want to reset the frame index and clear the visualization
        self.frame_index = 0
        self.view_widget.items.clear()  # Clear the current visualization
        print("LiDAR playback stopped.")
    def update_visualization_for_frame_with_filter(self, frame_index):
        print(f"Updating LiDAR visualization for frame: {frame_index}")

        if 0 <= frame_index < len(self.lidar_data):
            points = self.lidar_data[frame_index]
            # Apply the filter to show only points where x > 0
            filtered_points = points[points[:, 0] > 0]
            print(f"Number of filtered points: {len(filtered_points)}")

            self.update_visualization_with_filtered_points(filtered_points)
        else:
            print("Frame index out of range for LiDAR data")

    def update_visualization(self):
        if self.frame_index < len(self.lidar_data):
            points = self.lidar_data[self.frame_index]
            # Filter points where X > 0
            filtered_points = points[points[:, 0] > 0]

            # Extract 'x', 'y', 'z' values
            x_values = filtered_points[:, 0]
            y_values = filtered_points[:, 1]
            z_values = filtered_points[:, 2]

            # Create a new array with 'x', 'y', 'z' values
            xyz_values = np.column_stack((x_values, y_values, z_values))

            pos = xyz_values
            color = np.full((len(filtered_points), 4), [1, 0, 0, 1])  # Example: Red color

            if self.scatter_plot is None:
                self.scatter_plot = gl.GLScatterPlotItem(pos=pos, color=color, size=0.1)
                self.view_widget.addItem(self.scatter_plot)
            else:
                self.scatter_plot.setData(pos=pos, color=color)

            self.frame_index += 1
        else:
            self.stop_playback()  # Stop when all frames are displayed

    
    
    
    def save_lidar_times_to_csv(self, filepath):
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Frame Number', 'Timestamp'])
            for i, timestamp in enumerate(self.lidar_timestamps):
                writer.writerow([i, timestamp])

        print(f"Saved LiDAR timestamps to {filepath}")