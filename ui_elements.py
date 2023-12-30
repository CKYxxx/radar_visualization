#ui_elements.py

from PyQt5.QtWidgets import QPushButton,QComboBox, QVBoxLayout,QHBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt

class UIElements:
    def __init__(self, control_handler, video_player, radar_visualization):
        self.control_handler = control_handler
        self.video_player = video_player
        self.radar_visualization = radar_visualization

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
        self.video_player.media_player.setPosition(new_video_position)

        radar_frame_rate = 20
        adjusted_position = new_video_position + self.radar_visualization.video_offset_ms
        if adjusted_position < 0:
            return

        radar_frame_number = adjusted_position / 1000 * radar_frame_rate
        self.radar_visualization.update_frame(int(radar_frame_number))

    def update_slider_position(self, position):
        if not self.videoSlider.isSliderDown():
            video_duration = self.video_player.media_player.duration()
            if video_duration > 0:
                slider_position = self.videoSlider.maximum() * position / video_duration
                self.videoSlider.setValue(slider_position)


def create_color_coding_ui(callback):
    container = QWidget()
    layout = QVBoxLayout(container)

    color_coding_combobox = QComboBox()
    color_coding_combobox.addItems(["Default", "SNR", "Velocity", "Z Position"])
    color_coding_combobox.currentIndexChanged.connect(callback)

    layout.addWidget(QLabel("Color Coding:"))
    layout.addWidget(color_coding_combobox)

    return container
