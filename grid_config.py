# grid_config.py
import numpy as np
from pyqtgraph.opengl import GLGridItem,GLScatterPlotItem,GLLinePlotItem
class GridConfig:
    def __init__(self, view_widget, x_axis_range=100, y_axis_range=50, grid_spacing=5):
        self.view_widget = view_widget
        self.grid = GLGridItem()
        self.x_axis_range = x_axis_range
        self.y_axis_range = y_axis_range
        self.grid_spacing = grid_spacing
        self.view_widget = view_widget
        self.x_axis_range = 100  # Default x-axis range
        self.y_axis_range = 50   # Default y-axis range
        self.grid_spacing = 5    # Default grid spacing
        self.initialize_grid()

 
    def initialize_grid(self):
        # Initialize the grid with default settings
        self.grid = GLGridItem()
        self.set_grid_size(self.x_axis_range, self.y_axis_range, self.grid_spacing)
        self.view_widget.addItem(self.grid)
        self.add_axes_markers()

    def set_grid_size(self, width, height, spacing):
        # Set the size and spacing of the grid
        self.grid.setSize(x=width, y=height, z=0)
        self.grid.setSpacing(x=spacing, y=spacing, z=1)
        # Adjust translation to center the grid
        self.grid.translate(width / 2, 0, 0)
        self.view_widget.update()

    def add_grid_to_view(self):
        if not self.grid.parent():
            self.view_widget.addItem(self.grid)
        else:
            self.view_widget.update()

    def add_axes_markers(self):
        # Axis length and colors
        axis_length = 5  # Adjust as needed
        colors = np.array([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])  # RGB colors

        # X-axis (Red)
        x_axis = np.array([[0, 0, 0], [axis_length, 0, 0]])
        x_line = GLLinePlotItem(pos=x_axis, color=colors[0], width=2, antialias=True)
        self.view_widget.addItem(x_line)

        # Y-axis (Green)
        y_axis = np.array([[0, 0, 0], [0, axis_length, 0]])
        y_line = GLLinePlotItem(pos=y_axis, color=colors[1], width=2, antialias=True)
        self.view_widget.addItem(y_line)

        # Z-axis (Blue)
        z_axis = np.array([[0, 0, 0], [0, 0, axis_length]])
        z_line = GLLinePlotItem(pos=z_axis, color=colors[2], width=2, antialias=True)
        self.view_widget.addItem(z_line)