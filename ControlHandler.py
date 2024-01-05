from PyQt5.QtMultimedia import QMediaPlayer

class ControlHandler:
    def __init__(self, radar_visualization, video_player,lidar_handler):
        self.radar_visualization = radar_visualization
        self.video_player = video_player
        self.lidar_handler = lidar_handler
        # Set the radar visualization's update callback to a new method
        radar_visualization.update_callback = self.on_radar_frame_update


    def startVisualization(self):
        self.radar_visualization.start_visualization()  # Start the radar visualization
        # Calculate the corresponding video time
        radar_time_seconds = self.radar_visualization.frame_index / self.radar_visualization.frame_rate
        video_time_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
        # print(f"Current video time (ms): {video_time_ms}")        # Check if the calculated video time is non-negative
        # if video_time_ms >= 0:
        #     # Update the video position and start playback
        #     self.video_player.set_position(video_time_ms)
        #     self.video_player.play()
        # else:
        #     # If the position is negative, do not start the video yet
        #     self.video_player.set_position(0)
        self.video_player.play()
        self.lidar_handler.start_playback()

    def pauseVisualization(self):
        self.radar_visualization.timer.stop()
        self.video_player.pause()
        self.lidar_handler.stop_playback()


    def stepForward(self):
        if self.radar_visualization.frame_index < len(self.radar_visualization.radar_data) - 1:
            # Move to the next radar frame
            new_frame_index = self.radar_visualization.frame_index + 1
            self.radar_visualization.update_frame(new_frame_index)

            # Calculate the corresponding video time
            radar_time_seconds = new_frame_index / self.radar_visualization.frame_rate
            video_time_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms

            # Update the video position
            self.video_player.media_player.setPosition(video_time_ms)

            # Update the LiDAR visualization to match the new radar frame
            self.lidar_handler.update_to_match_radar(new_frame_index)

    
    def stepBackward(self):
        # Check if the current frame is greater than the first frame
        if self.radar_visualization.frame_index > 1:
            # Move to the previous radar frame
            new_frame_index = self.radar_visualization.frame_index - 1
            self.radar_visualization.update_frame(new_frame_index)

            # Calculate the corresponding video time
            radar_time_seconds = new_frame_index / self.radar_visualization.frame_rate
            video_time_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms

            # Update the video position
            self.video_player.media_player.setPosition(video_time_ms)

            # Update the LiDAR visualization to match the new radar frame
            self.lidar_handler.update_to_match_radar(new_frame_index)

    # def syncWithSlider(self, value):
    #     # Update video
    #     total_duration = self.video_player.media_player.duration()
    #     new_video_position = total_duration * value / 1000
    #     self.video_player.set_position(new_video_position + self.radar_visualization.video_offset_ms)

    #     # Update radar visualization
    #     radar_frame_rate = self.radar_visualization.frame_rate  # assuming frame_rate is defined in radar_visualization
    #     new_radar_frame = int((new_video_position + self.radar_visualization.video_offset_ms) / 1000 * radar_frame_rate)
    #     self.radar_visualization.update_frame(new_radar_frame)
    #     # Calculate the corresponding video time
    #     radar_time_seconds = self.radar_visualization.frame_index / self.radar_visualization.frame_rate
    #     video_time_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
    #     self.video_player.media_player.setPosition(video_time_ms)
    def syncWithSlider(self, value):
        # Update video
        total_duration = self.video_player.media_player.duration()
        new_video_position = total_duration * value / 1000
        self.video_player.set_position(new_video_position + self.radar_visualization.video_offset_ms)

        # Update radar visualization
        radar_frame_rate = self.radar_visualization.frame_rate
        new_radar_frame = int((new_video_position + self.radar_visualization.video_offset_ms) / 1000 * radar_frame_rate)
        self.radar_visualization.update_frame(new_radar_frame)

        # Update LiDAR visualization to match the new radar frame
        self.lidar_handler.update_to_match_radar(new_radar_frame)

        # Optionally, update the video position again to ensure synchronization
        radar_time_seconds = new_radar_frame / self.radar_visualization.frame_rate
        video_time_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
        self.video_player.media_player.setPosition(video_time_ms)
    def on_radar_frame_update(self, frame_index):
        # Calculate the video position based on the radar frame
        radar_time_seconds = frame_index / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms

        # Update video player position
        self.video_player.media_player.setPosition(video_position_ms)

        # Pause the video player if it's currently playing
        if self.video_player.media_player.state() == QMediaPlayer.PlayingState:
            self.video_player.media_player.pause()
    def update_sensors(self, frame_number):
        # Calculate the corresponding video position in milliseconds
        radar_time_seconds = frame_number / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
        self.video_player.media_player.setPosition(video_position_ms)
