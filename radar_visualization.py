import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from PyQt5.QtCore import QTimer
from pyqtgraph.opengl import GLGridItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui_elements import create_color_coding_ui
from PyQt5.QtMultimedia import QMediaPlayer

class RadarVisualization(QWidget):
    def __init__(self, view_widget, frame_rate=20, update_callback=None, control_handler=None, video_offset_ms=0):
        super().__init__()
        self.view_widget = view_widget
        self.frame_index = 1
        self.radar_data = None
        self.scatter_plot = None
        self.current_color_coding = None
        self.frame_rate = frame_rate
        self.video_offset_ms = video_offset_ms
        self.update_callback = update_callback
        self.control_handler = control_handler

        # Setup layout and UI
        layout = QVBoxLayout(self)
        layout.addWidget(self.view_widget)
        self.color_coding_ui = create_color_coding_ui(self.update_color_coding)
        layout.addWidget(self.color_coding_ui)

    def setup(self, csv_path):
        try:
            self.radar_data = pd.read_csv(csv_path)
            if 'Frame' not in self.radar_data.columns:
                raise ValueError("'Frame' column is missing in the data.")
        except Exception as e:
            print(f"Error loading file: {e}")

    def update(self):
        if self.frame_index < len(self.radar_data['Frame'].unique()):
            self.frame_index += 1
        else:
            self.frame_index = 1  # Loop back to the start or handle as needed

        self.update_scatter_plot_for_frame(self.frame_index)

    def get_current_frame_index(self):
        return self.frame_index

    def update_frame(self, frame_number):
        if 0 < frame_number <= len(self.radar_data['Frame'].unique()):
            self.frame_index = frame_number
            self.update_scatter_plot_for_frame(frame_number)
   
    def update_scatter_plot_for_frame(self, frame_index):
        # Check if the frame index is in the 'Frame' column of radar_data
        if frame_index in self.radar_data['Frame'].values:
            # Get the data for the specific frame
            frame_data = self.radar_data[self.radar_data['Frame'] == frame_index]

            # Extract coordinates from frame_data
            points = frame_data[['X Position (m)', 'Y Position (m)', 'Z Position (m)']].to_numpy()
            points[:, 1] *= -1  # Flip the Y-axis if needed

            # Determine the colors for the points
            colors = self.get_colors_for_frame(frame_data)

            # Update or create the scatter plot
            if self.scatter_plot is None:
                self.scatter_plot = gl.GLScatterPlotItem(pos=points, size=0.1, color=colors, pxMode=False)
                self.view_widget.addItem(self.scatter_plot)
            else:
                self.scatter_plot.setData(pos=points, color=colors)
        else:
            print(f"Frame index {frame_index} is out of radar data range.")

    def get_colors_for_frame(self, frame_data):
        # Implement the logic to get color values for each point
        # For example, you can use the same color for all points or based on some data column
        return np.array([[1, 1, 0, 1]] * len(frame_data))  # RGBA for yellow as an example
    
    def apply_simplified_color_coding(self, color_column):
        if self.radar_data is None:
            return
        color_values = self.radar_data[color_column].to_numpy()
        min_val, max_val = np.min(color_values), np.max(color_values)
        divisions = np.linspace(min_val, max_val, 7)
        division_colors = np.array([
            [1, 0, 0, 1],   # Red
            [1, 0.5, 0, 1], # Orange
            [1, 1, 0, 1],   # Yellow
            [0, 1, 0, 1],   # Green
            [0, 1, 1, 1],   # Cyan
            [0, 0, 1, 1],   # Blue
            [0.5, 0, 0.5, 1]# Purple
        ])
        division_indices = np.digitize(color_values, divisions, right=True)
        colors = division_colors[np.clip(division_indices - 1, 0, 6)]
        frame_data = self.radar_data[self.radar_data['Frame'] == self.frame_index]
        frame_colors = colors[self.radar_data['Frame'] == self.frame_index]
        self.update_scatter_plot(frame_data, frame_colors)

    def update_color_coding(self, index):
        if self.radar_data is not None:
            if index == 0:  # Default
                self.current_color_coding = None
                frame_data = self.radar_data[self.radar_data['Frame'] == self.frame_index]
                self.update_scatter_plot(frame_data, None)
            elif index == 1:  # SNR
                self.current_color_coding = 'SNR (dB)'
                self.apply_simplified_color_coding('SNR (dB)')
            elif index == 2:  # Velocity
                self.current_color_coding = 'Velocity (m/s)'
                self.apply_simplified_color_coding('Velocity (m/s)')
            else:  # Z Position
                self.current_color_coding = 'Z Position (m)'
                self.apply_simplified_color_coding('Z Position (m)')

    def set_control_handler(self, control_handler):
        self.control_handler = control_handler
    # def get_widget(self):
    #     return self.view_widget
    def redraw_current_frame(self):
        # Check if the current frame index is valid
        if self.frame_index in self.radar_data['Frame'].unique():
            # Get data for the current frame
            frame_data = self.radar_data[self.radar_data['Frame'] == self.frame_index]
            # Update the scatter plot for this frame
            self.update_scatter_plot_for_frame(self.frame_index)
        else:
            print(f"Radar frame index {self.frame_index} is out of range.")

