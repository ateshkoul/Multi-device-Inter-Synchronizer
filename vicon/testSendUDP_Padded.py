import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

UDP_IP = "172.16.130.173"
UDP_PORT = 30

FOLDER_PATH = "E:\\try_ses\\"
CAPTURE_NAME = "testing 55"
PACKET_ID = 0
MESSAGE_START = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?><CaptureStart><Name VALUE=\"" + CAPTURE_NAME + "\"/><Notes VALUE=\"aa\"/><Description VALUE=\"bb\"/><DatabasePath VALUE=\"" + FOLDER_PATH + "\"/><Delay VALUE=\"\"/><PacketID VALUE=\"" + str(PACKET_ID) + "\"/></CaptureStart>"
MESSAGE_STOP = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?><CaptureStop RESULT=\"SUCCESS\"><Name VALUE=\"" + CAPTURE_NAME + "\"/><DatabasePath VALUE=\"" + FOLDER_PATH + "\"/><Delay VALUE=\"\"/><PacketID VALUE=\"" + str(PACKET_ID+1) + "\"/></CaptureStop>"

targetLength=500	#must pad to equal length
MESSAGE_START = MESSAGE_START + ' '*(targetLength - len(MESSAGE_START))
MESSAGE_STOP = MESSAGE_STOP + ' '*(targetLength - len(MESSAGE_STOP))

# Send Start message
sock.sendto(MESSAGE_START.encode(), ("155.100.55.100", UDP_PORT))
print(MESSAGE_START)
print("Socket sent to %s:%d" %(UDP_IP,UDP_PORT))

time.sleep(5)

# Send Stop message
sock.sendto(MESSAGE_STOP.encode(), (UDP_IP, UDP_PORT))
print(MESSAGE_STOP)
print("Socket sent to %s:%d" %(UDP_IP,UDP_PORT))
