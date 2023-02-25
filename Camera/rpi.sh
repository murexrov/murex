#stream from webcam
ffmpeg -f v4l2 -i /dev/video0 -c:v h264_v4l2m2m -b:v 125000 -fflags nobuffer -flags low_delay -preset ultrafast -tune zerolatency -probesize 32 -num_output_buffers 32 -num_capture_buffers 16 -analyzeduration 0 -f mpegts udp://192.168.100.52:1234
#receive on topside computer
ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://192.168.100.1:1234