import socket



class tcp_data():
    def __init__(self,host,port):
        
        # host = socket.gethostname()
        host = "151.100.55.49"
        port = 30                   # The same port as used by the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_tcp(self):
        self.s.connect((host, port))
        
    def send_data(self,data):
        self.s.sendall(b'hello')
        rec_data = self.s.recv(1024)
        self.s.close()
        print('Received', repr(rec_data))