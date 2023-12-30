class ControlHandler:
    def __init__(self, radar_visualization, video_player):
        self.radar_visualization = radar_visualization
        self.video_player = video_player

    def startVisualization(self):
        self.radar_visualization.timer.start(100)  # Update every 100 ms
        self.video_player.play()

    def pauseVisualization(self):
        self.radar_visualization.timer.stop()
        self.video_player.pause()

    def stepForward(self):
        if self.radar_visualization.frame_index < len(self.radar_visualization.radar_data):
            self.radar_visualization.update_frame(self.radar_visualization.frame_index + 1)
            current_position = self.video_player.media_player.position()
            self.video_player.media_player.setPosition(current_position + 1000 / 30)

    def stepBackward(self):
        if self.radar_visualization.frame_index > 1:
            self.radar_visualization.update_frame(self.radar_visualization.frame_index - 1)
            current_position = self.video_player.media_player.position()
            self.video_player.media_player.setPosition(max(0, current_position - 1000 / 30))
