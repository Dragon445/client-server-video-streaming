import socket,cv2, pickle,struct,time

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = input("addr: ") # paste your server ip address here
port = 9999
client_socket.connect((host_ip,port)) # a tuple
data = b""
capture = cv2.VideoCapture(0)
payload_size = struct.calcsize("Q")
while True:
        ret,frame = capture.read()
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        client_socket.sendall(message)

        time.sleep(0.01)
        while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet: break
                data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
	
        while len(data) < msg_size:
                data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
                break
client_socket.close()
