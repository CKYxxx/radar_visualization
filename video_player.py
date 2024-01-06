# video_player.py

#        self.frame_rate = 30

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget

class VideoPlayer(QWidget):
    def __init__(self, video_path,frame_rate, parent=None):
        super().__init__(parent)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        # self.media_player.stateChanged.connect(self.state_changed)
        # self.media_player.mediaStatusChanged.connect(self.status_changed)
        self.frame_rate = frame_rate
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        self.setLayout(layout)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))

        # Connect to the error signal of the media player
        self.media_player.error.connect(self.handle_media_player_error)

        self.video_offset_ms = 0  # Default offset


    def play(self):
        self.media_player.play()
        # print(f"Media Player State: {self.media_player.state()}")
        # print(f"Media Player Error: {self.media_player.errorString()}")

    def set_offset(self, offset_ms):
        self.video_offset_ms = offset_ms

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def handle_media_player_error(self):
        print("Error:", self.media_player.errorString())
    def state_changed(self, state):
        print(f"Player State Changed: {state}")

    def set_position(self, position):
        if position < 0:
            position = 0
        print(f"Video player position set to: {position}")  # Debug print
        self.media_player.setPosition(position)
    def get_current_frame(self):
        # Implement logic to return the current frame number
        # This is an example implementation. You need to adjust it based on how your video player is set up.
        if self.media_player.duration() == 0:
            return 0
        return int(self.media_player.position() * self.frame_rate / 1000)

    def get_total_frames(self):
        # Implement logic to return the total number of frames in the video
        # This is an example implementation. Adjust it based on your video player setup.
        if self.media_player.duration() == 0:
            return 0
        return int(self.media_player.duration() * self.frame_rate / 1000)

# End of video_player.py

