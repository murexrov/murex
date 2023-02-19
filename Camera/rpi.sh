ffmpeg -f v4l2 -i /dev/video0 -vcodec libx264 -fflags nobuffer -flags low_delay -preset ultrafast -tune zerolatency -probesize 32 -analyzeduration 0 -f mpegts udp://192.168.100.1:1234
#receive on topside computer
ffmpeg -i udp://192.168.100.1:1234