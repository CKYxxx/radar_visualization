# radar_visualization.py

import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout, QSlider, QLabel, QWidget

class RadarVisualization:
    def __init__(self, parent_widget):
        self.view_widget = gl.GLViewWidget(parent_widget)
        # self.view_widget.setMinimumSize(640, 480)  # Set a reasonable minimum size
        self.view_widget.opts['distance'] = 20
        self.scatter_plot = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.frame_index = 1
        self.data = None
        self.grid_scale = 2  # Initial grid scale

    def setup(self, csv_path):
        # Create a grid to add to the GLViewWidget (if not done already)
        self.grid = gl.GLGridItem()
        self.grid.scale(self.grid_scale, self.grid_scale, 1)
        self.view_widget.addItem(self.grid)

        self.load_radar_data(csv_path)
        self.timer.start(100)  # Update every 100 ms

    def create_grid_scale_slider(self):
        # Create a widget to hold the slider and label
        widget = QWidget()
        layout = QVBoxLayout()

        # Create a label for the slider
        label = QLabel("Grid Scale")
        layout.addWidget(label)

        # Create a slider to adjust the grid scale
        self.grid_scale_slider = QSlider(Qt.Horizontal)
        self.grid_scale_slider.setMinimum(1)
        self.grid_scale_slider.setMaximum(10)  # Adjust the maximum value as needed
        self.grid_scale_slider.setValue(self.grid_scale)
        self.grid_scale_slider.valueChanged.connect(self.update_grid_scale)

        layout.addWidget(self.grid_scale_slider)
        widget.setLayout(layout)

        return widget

    def update_grid_scale(self):
        # Update the grid scale when the slider is moved
        self.grid_scale = self.grid_scale_slider.value()
        self.grid.scale(self.grid_scale, self.grid_scale, 1)





    def load_radar_data(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.update()  # Initial update

    def update(self):
        print(f"Updating frame {self.frame_index}")
        if self.data is not None and 'Frame' in self.data.columns:
            frame_data = self.data[self.data['Frame'] == self.frame_index]
            if not frame_data.empty:
                points = frame_data[['X Position (m)', 'Y Position (m)', 'Z Position (m)']].values
                self.update_radar_data(points)
                self.frame_index += 1
            else:
                print(f"No data for frame {self.frame_index}")
                self.frame_index = 0  # Reset to loop the data or handle the end of data
        else:
            print("Data is not loaded or 'Frame' column is missing.")


    def update_radar_data(self, points):
        print(f"Points to plot: {points.shape[0]}")  # Check how many points are being plotted
        if self.scatter_plot is None:
            # Create a new scatter plot item
            colors = np.random.rand(len(points), 4)
            self.scatter_plot = gl.GLScatterPlotItem(pos=points, size=1.0, color=colors, pxMode=False)  # Increase size for visibility
            self.view_widget.addItem(self.scatter_plot)
        else:
            # Update existing scatter plot item
            self.scatter_plot.setData(pos=points)


    def get_widget(self):
        return self.view_widget
    def resizeEvent(self, event):
        self.view_widget.resize(event.size())  # This line ensures the GLViewWidget resizes.
        event.accept()
