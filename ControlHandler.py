from PyQt5.QtMultimedia import QMediaPlayer

class ControlHandler:
    def __init__(self, radar_visualization, video_player, lidar_handler, main_window):
        self.radar_visualization = radar_visualization
        self.video_player = video_player
        self.lidar_handler = lidar_handler
        self.main_window = main_window

    def startVisualization(self, current_radar_frame):
        # Check if lidar_handler is not None before calling its methods
        if self.lidar_handler is not None:
            lidar_index = self.lidar_handler.calculate_lidar_index(current_radar_frame)
            self.lidar_handler.set_frame_index(lidar_index)

        # Determine the correct time to start the video based on the radar frame and time offset
        if self.main_window.time_offsets['camera'] >= 0:
            # Positive or zero offset: Start video at a specific position
            video_start_position_ms = self.main_window.time_offsets['camera']
            self.video_player.media_player.setPosition(video_start_position_ms)
            self.video_player.play()
        else:
            # Negative offset: Delay video start until the corresponding radar frame
            # Calculate the radar frame at which to start the video
            delay_in_frames = abs(self.main_window.time_offsets['camera']) / 1000 * self.radar_visualization.frame_rate
            self.main_window.delayed_video_start_frame = int(delay_in_frames)

        # Set the initial radar frame index and start visualization
        current_radar_frame = self.radar_visualization.get_current_frame_index()

        # Check again if lidar_handler is not None before setting the lidar frame index
        if self.lidar_handler is not None:
            self.lidar_handler.set_frame_index(self.lidar_handler.calculate_lidar_index(current_radar_frame))

        self.main_window.visualization_timer.start(100)  # Adjust the interval as needed




    def pauseVisualization(self):
        # Pause the video player
        self.video_player.pause()
        
        # Stop the visualization timer in MainWindow
        self.main_window.visualization_timer.stop()

    def stepForward(self):
        print("Stepping forward")
        if self.radar_visualization.frame_index < len(self.radar_visualization.radar_data) - 1:
            new_frame_index = self.radar_visualization.frame_index + 1
            print(f"New radar frame index: {new_frame_index}")
            self.radar_visualization.update_frame(new_frame_index)
            self.lidar_handler.update_visualization_for_frame_with_filter(new_frame_index)
            self.radar_visualization.redraw_current_frame()
            self.lidar_handler.redraw_current_frame()
            self.main_window.visualization_widget.update()

    def stepBackward(self):
        print("Stepping backward")
        if self.radar_visualization.frame_index > 0:
            new_frame_index = self.radar_visualization.frame_index - 1
            self.radar_visualization.update_frame(new_frame_index)
            self.lidar_handler.update_visualization_for_frame_with_filter(new_frame_index)
            self.radar_visualization.redraw_current_frame()
            self.lidar_handler.redraw_current_frame()
            self.main_window.visualization_widget.update()

    def syncWithSlider(self, value):
        print(f"Syncing with slider value: {value}")
        total_duration = self.video_player.media_player.duration()
        new_video_position = total_duration * value / 1000
        self.video_player.set_position(new_video_position)

        radar_frame_rate = self.radar_visualization.frame_rate
        new_radar_frame = int(new_video_position / 1000 * radar_frame_rate)
        self.radar_visualization.update_frame(new_radar_frame)
        self.lidar_handler.update_visualization_for_frame_with_filter(new_radar_frame)
        self.radar_visualization.redraw_current_frame()
        self.lidar_handler.redraw_current_frame()


    def syncWithFrameIndex(self, frame_index):
        print(f"Syncing with frame index: {frame_index}")
        radar_time_seconds = frame_index / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000
        self.video_player.media_player.setPosition(video_position_ms)

        self.radar_visualization.update_frame(frame_index)
        self.lidar_handler.update_visualization_for_frame(frame_index)
        self.radar_visualization.redraw_current_frame()
        self.lidar_handler.redraw_current_frame()

    def update_sensors(self, frame_number):
        print(f"Updating sensors for frame number: {frame_number}")
        radar_time_seconds = frame_number / self.radar_visualization.frame_rate
        video_position_ms = radar_time_seconds * 1000
        self.video_player.media_player.setPosition(video_position_ms)

        self.radar_visualization.update_frame(frame_number)
        self.lidar_handler.update_visualization_for_frame(frame_number)
        self.radar_visualization.redraw_current_frame()
        self.lidar_handler.redraw_current_frame()
