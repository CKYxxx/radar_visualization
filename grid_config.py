# grid_config.py
import numpy as np
from pyqtgraph.opengl import GLGridItem

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
        self.init_grid()

    def init_grid(self):
        self.set_grid_size(self.x_axis_range, self.y_axis_range, self.grid_spacing)
    def initialize_grid(self):
        # Initialize the grid with default settings
        self.grid = GLGridItem()
        self.set_grid_size(self.x_axis_range, self.y_axis_range, self.grid_spacing)
        self.view_widget.addItem(self.grid)

    def set_grid_size(self, width, height, spacing):
        # Set the size and spacing of the grid
        self.grid.setSize(x=width, y=height, z=0)
        self.grid.setSpacing(x=spacing, y=spacing, z=1)
        # Adjust translation to center the grid
        self.grid.translate(-width / 2, -height / 2, 0)
        self.view_widget.update()

    def add_grid_to_view(self):
        if not self.grid.parent():
            self.view_widget.addItem(self.grid)
        else:
            self.view_widget.update()
