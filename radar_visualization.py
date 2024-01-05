import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from PyQt5.QtCore import QTimer
from pyqtgraph.opengl import GLGridItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui_elements import create_color_coding_ui
from PyQt5.QtMultimedia import QMediaPlayer

class RadarVisualization(QWidget):
    def __init__(self, parent=None, frame_rate=20,update_callback=None,control_handler=None,video_offset_ms=0):
        super().__init__(parent)
        self.setup_view_widget()
        self.frame_index = 1
        self.radar_data = None
        self.scatter_plot = None
        self.current_color_coding = None
        self.frame_rate = frame_rate
        self.video_offset_ms = video_offset_ms

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.update_callback = update_callback

        layout = QVBoxLayout(self)
        layout.addWidget(self.view_widget)
        self.color_coding_ui = create_color_coding_ui(self.update_color_coding)
        layout.addWidget(self.color_coding_ui)

        self.control_handler = control_handler

    def setup_view_widget(self):
        self.view_widget = gl.GLViewWidget()
        self.view_widget.opts['distance'] = 20
        self.setup_grid()

    def setup_grid(self):
        x_axis_range = 100
        y_axis_range = 50
        grid_spacing = 5

        self.grid = GLGridItem()
        self.grid.setSize(x=x_axis_range, y=y_axis_range, z=0)
        self.grid.setSpacing(x=grid_spacing, y=grid_spacing, z=1)
        self.grid.translate(x_axis_range / 2, 0, 0)
        self.view_widget.addItem(self.grid)

    def setup(self, csv_path):
        try:
            self.radar_data = pd.read_csv(csv_path)
            if 'Frame' not in self.radar_data.columns:
                raise ValueError("'Frame' column is missing in the data.")
        except Exception as e:
            print(f"Error loading file: {e}")

    def start_visualization(self):
        if not self.timer.isActive():
            self.timer.start(1000 / self.frame_rate)  # Start visualization based on frame rate

    def stop_visualization(self):
        if self.timer.isActive():
            self.timer.stop()

    def set_video_offset(self, offset_ms):
        self.video_offset_ms = offset_ms

    def update(self):
        if self.radar_data is not None and 'Frame' in self.radar_data.columns:
            frame_data = self.radar_data[self.radar_data['Frame'] == self.frame_index]
            if not frame_data.empty:
                if self.current_color_coding:
                    self.apply_simplified_color_coding(self.current_color_coding)
                else:
                    self.update_scatter_plot(frame_data)

                self.frame_index += 1
            else:
                self.frame_index = 1
        else:
            print("Data is not loaded or 'Frame' column is missing.")

        print(f"Updating radar frame: {self.frame_index}")  # Debug print



    def update_frame(self, frame_number):
        if 0 < frame_number <= len(self.radar_data['Frame'].unique()):
            self.frame_index = frame_number
            frame_data = self.radar_data[self.radar_data['Frame'] == frame_number]
            if self.current_color_coding:
                self.apply_simplified_color_coding(self.current_color_coding)
            else:
                self.update_scatter_plot(frame_data)
        else:
            print(f"Frame number {frame_number} is out of range.")

    def update_scatter_plot(self, frame_data, colors=None):
        points = frame_data[['X Position (m)', 'Y Position (m)', 'Z Position (m)']].values
        points[:, 1] *= -1  # Flip the Y-axis
        if colors is None:
            # colors = np.random.rand(len(points), 4)
            colors = np.array([[1, 1, 0, 1]] * len(points))  # RGBA for yellow
        if self.scatter_plot is None:
            self.scatter_plot = gl.GLScatterPlotItem(pos=points, size=0.1, color=colors, pxMode=False)
            self.view_widget.addItem(self.scatter_plot)
        else:
            self.scatter_plot.setData(pos=points, color=colors)

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
    def get_widget(self):
        return self.view_widget
