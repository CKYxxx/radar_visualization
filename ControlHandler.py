class ControlHandler:
    def __init__(self, radar_visualization, video_player):
        self.radar_visualization = radar_visualization
        self.video_player = video_player
        # Set the radar visualization's update callback to a new method
        radar_visualization.update_callback = self.on_radar_frame_update


    def startVisualization(self):
        self.radar_visualization.start_visualization()  # Start the radar visualization
        self.video_player.play()

    def pauseVisualization(self):
        self.radar_visualization.timer.stop()
        self.video_player.pause()

    # def stepForward(self):
    #     if self.radar_visualization.frame_index < len(self.radar_visualization.radar_data):
    #         self.radar_visualization.update_frame(self.radar_visualization.frame_index + 1)
    #         current_position = self.video_player.media_player.position()
    #         self.video_player.media_player.setPosition(current_position + 1000 / 30)
    def stepForward(self):
        if self.radar_visualization.frame_index < len(self.radar_visualization.radar_data):
            new_frame_index = self.radar_visualization.frame_index + 1
            self.radar_visualization.update_frame(new_frame_index)

            # Calculate the corresponding video time
            radar_time_seconds = new_frame_index / self.radar_visualization.frame_rate
            video_time_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms

            # Update the video position
            self.video_player.media_player.setPosition(video_time_ms)


    # def stepBackward(self):
    #     if self.radar_visualization.frame_index > 1:
    #         self.radar_visualization.update_frame(self.radar_visualization.frame_index - 1)
    #         current_position = self.video_player.media_player.position()
    #         self.video_player.media_player.setPosition(max(0, current_position - 1000 / 30))
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

    def syncWithSlider(self, value):
        # Update video
        total_duration = self.video_player.media_player.duration()
        new_video_position = total_duration * value / 1000
        self.video_player.set_position(new_video_position + self.radar_visualization.video_offset_ms)

        # Update radar visualization
        radar_frame_rate = self.radar_visualization.frame_rate  # assuming frame_rate is defined in radar_visualization
        new_radar_frame = int((new_video_position + self.radar_visualization.video_offset_ms) / 1000 * radar_frame_rate)
        self.radar_visualization.update_frame(new_radar_frame)
    def update_video_position(self):
        # Calculate the corresponding video time
        radar_time_seconds = self.radar_visualization.frame_index / self.radar_visualization.frame_rate
        video_time_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
        self.video_player.media_player.setPosition(video_time_ms)
    def on_radar_frame_update(self, frame_index):
        radar_time_seconds = frame_index / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
        print(f"Setting video position: {video_position_ms} ms")  # Debug print
        self.video_player.set_position(video_position_ms)
    def update_sensors(self, frame_number):
        # Calculate the corresponding video position in milliseconds
        radar_time_seconds = frame_number / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000 + self.radar_visualization.video_offset_ms
        self.video_player.media_player.setPosition(video_position_ms)
