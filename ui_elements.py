#ui_elements.py

from PyQt5.QtWidgets import QPushButton,QComboBox, QVBoxLayout,QHBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt

class UIElements:
    def __init__(self, control_handler, video_player, radar_visualization, lidar_handler):
        self.control_handler = control_handler
        self.video_player = video_player
        self.radar_visualization = radar_visualization
        self.lidar_handler = lidar_handler
        # Initialize labels for video, radar, and lidar frames
        self.video_total_frames_label = QLabel("Total Video Frames: 0")
        self.video_current_frame_label = QLabel("Current Video Frame: 0")
        self.radar_total_frames_label = QLabel("Total Radar Frames: 0")
        self.radar_current_frame_label = QLabel("Current Radar Frame: 0")
        self.lidar_total_frames_label = QLabel("Total LiDAR Frames: 0")
        self.lidar_current_frame_label = QLabel("Current LiDAR Frame: 0")

        self.detections_label = QLabel("Number of Detections: 0")

    def create_control_buttons(self):
        startButton = QPushButton("Start")
        pauseButton = QPushButton("Pause")
        forwardButton = QPushButton("Forward")
        backwardButton = QPushButton("Backward")

        startButton.clicked.connect(self.control_handler.startVisualization)
        pauseButton.clicked.connect(self.control_handler.pauseVisualization)
        forwardButton.clicked.connect(self.control_handler.stepForward)
        backwardButton.clicked.connect(self.control_handler.stepBackward)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(startButton)
        controlLayout.addWidget(pauseButton)
        controlLayout.addWidget(forwardButton)
        controlLayout.addWidget(backwardButton)

        controlWidget = QWidget()
        controlWidget.setLayout(controlLayout)

        return controlWidget

    def create_video_slider(self):
        self.videoSlider = QSlider(Qt.Horizontal)
        self.videoSlider.setMinimum(0)
        self.videoSlider.setMaximum(1000)
        self.videoSlider.sliderMoved.connect(self.sliderMoved)

        return self.videoSlider

    def sliderMoved(self, position):
        video_duration = self.video_player.media_player.duration()
        new_video_position = video_duration * position / self.videoSlider.maximum()

        radar_frame_rate = 20  # Set the radar frame rate
        radar_frame_duration = 1000 / radar_frame_rate  # Duration of each radar frame in milliseconds

        # Calculate the radar frame number based on the video position and offset
        adjusted_position = new_video_position + self.radar_visualization.video_offset_ms
        radar_frame_number = adjusted_position / radar_frame_duration
        self.radar_visualization.update_frame(int(radar_frame_number))

    def update_slider_position(self, position):
        if not self.videoSlider.isSliderDown():
            video_duration = self.video_player.media_player.duration()
            if video_duration > 0:
                slider_position = self.videoSlider.maximum() * position / video_duration
                self.videoSlider.setValue(slider_position)

    def create_video_slider(self):
        self.videoSlider = QSlider(Qt.Horizontal)
        self.videoSlider.setMinimum(0)
        self.videoSlider.setMaximum(1000)
        self.videoSlider.valueChanged.connect(self.control_handler.syncWithSlider)
    def create_frame_display(self):
        # Layout for frame display widgets
        layout = QVBoxLayout()

        # Add all frame information labels to the layout
        layout.addWidget(self.video_total_frames_label)
        layout.addWidget(self.video_current_frame_label)
        layout.addWidget(self.radar_total_frames_label)
        layout.addWidget(self.radar_current_frame_label)
        layout.addWidget(self.lidar_total_frames_label)
        layout.addWidget(self.lidar_current_frame_label)
        layout.addWidget(self.detections_label)

        # Wrap the layout in a QWidget
        frame_display_widget = QWidget()
        frame_display_widget.setLayout(layout)

        return frame_display_widget

    def update_frame_display(self, video_current, video_total, radar_current, radar_total, lidar_current, lidar_total):
        self.video_total_frames_label.setText(f"Total Video Frames: {video_total}")
        self.video_current_frame_label.setText(f"Current Video Frame: {video_current}")
        self.radar_total_frames_label.setText(f"Total Radar Frames: {radar_total}")
        self.radar_current_frame_label.setText(f"Current Radar Frame: {radar_current}")
        self.lidar_total_frames_label.setText(f"Total LiDAR Frames: {lidar_total}")
        self.lidar_current_frame_label.setText(f"Current LiDAR Frame: {lidar_current}")

        return self.videoSlider
    def update_detections_display(self, num_detections):
        self.detections_label.setText(f"Number of Detections: {num_detections}")

def create_color_coding_ui(callback):
    container = QWidget()
    layout = QVBoxLayout(container)

    color_coding_combobox = QComboBox()
    color_coding_combobox.addItems(["Default", "SNR", "Velocity", "Z Position"])
    color_coding_combobox.currentIndexChanged.connect(callback)

    layout.addWidget(QLabel("Color Coding:"))
    layout.addWidget(color_coding_combobox)

    return container
