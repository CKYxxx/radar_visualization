from PyQt5.QtMultimedia import QMediaPlayer

class ControlHandler:
    def __init__(self, radar_visualization, video_player, lidar_handler, main_window):
        self.radar_visualization = radar_visualization
        self.video_player = video_player
        self.lidar_handler = lidar_handler
        self.main_window = main_window

    def startVisualization(self):
        # Start video playback
        self.video_player.play()

        # Set the initial radar and LiDAR frame indices
        current_radar_frame = self.radar_visualization.get_current_frame_index()
        self.lidar_handler.set_frame_index(self.lidar_handler.calculate_lidar_index(current_radar_frame))

        # Start the centralized timer in MainWindow
        self.main_window.visualization_timer.start(100)  # Adjust the interval as needed

    def pauseVisualization(self):
        # Pause the video player
        self.video_player.pause()
        
        # Stop the visualization timer in MainWindow
        self.main_window.visualization_timer.stop()

    def stepForward(self):
        # Step forward in radar visualization
        if self.radar_visualization.frame_index < len(self.radar_visualization.radar_data) - 1:
            new_frame_index = self.radar_visualization.frame_index + 1
            self.radar_visualization.update_frame(new_frame_index)
            self.syncWithFrameIndex(new_frame_index)

    def stepBackward(self):
        # Step backward in radar visualization
        if self.radar_visualization.frame_index > 1:
            new_frame_index = self.radar_visualization.frame_index - 1
            self.radar_visualization.update_frame(new_frame_index)
            self.syncWithFrameIndex(new_frame_index)

    def syncWithSlider(self, value):
        # Update video position based on slider value
        total_duration = self.video_player.media_player.duration()
        new_video_position = total_duration * value / 1000
        self.video_player.set_position(new_video_position + self.radar_visualization.video_offset_ms)

        # Update radar visualization frame
        radar_frame_rate = self.radar_visualization.frame_rate
        new_radar_frame = int((new_video_position + self.radar_visualization.video_offset_ms) / 1000 * radar_frame_rate)
        self.radar_visualization.update_frame(new_radar_frame)

        # Update LiDAR visualization to match the radar frame
        self.lidar_handler.update_to_match_radar(new_radar_frame)

    def syncWithFrameIndex(self, frame_index):
        # Calculate the video position based on radar frame index
        radar_time_seconds = frame_index / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms

        # Update the video position
        self.video_player.media_player.setPosition(video_position_ms)

        # Update the LiDAR visualization to match the radar frame
        self.lidar_handler.update_to_match_radar(frame_index)

    def on_radar_frame_update(self, frame_index):
        # This method can be used for additional callbacks when radar frame updates
        pass

    def update_sensors(self, frame_number):
        # Update the video position based on radar frame number
        radar_time_seconds = frame_number / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
        self.video_player.media_player.setPosition(video_position_ms)
