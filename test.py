import velodyne_decoder as vd

# Specify the path to your PCAP file
pcap_file_path = '/home/s0001593/Downloads/provizio/Dataset_mid_range/Lidar/velodyne.pcap'  # Replace with the actual path to the PCAP file

# Create a default Velodyne Config object
config = vd.Config()

# Manually set the model for the decoder
config.model = vd.Model.VLP_16  # Or the appropriate model identifier

# Prepare to decode the point clouds
cloud_arrays = []
for stamp, points in vd.read_pcap(pcap_file_path, config):
    cloud_arrays.append(points)

# Process the decoded point clouds as needed
# ...
