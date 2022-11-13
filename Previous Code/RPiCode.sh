# Streamer
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert! videoscale ! 'video/x-raw,width=1920,height=1080' ! x264enc speed-preset="ultrafast" quantizer=20 sliced-threads=true tune=zerolatency ! rtph264pay ! udpsink host=<RECEIVER IP> port=1234

# Note: the host is the ip of the receiving device

# Receiver (for topside computer)
gst-launch-1.0 udpsrc port=1234 ! "application/x-rtp, payload=127" ! rtph264depay ! avdec_h264 ! glimagesink

# Create AP with Raspberry Pi, wired
# https://linuxhint.com/raspberry_pi_wired_router/
