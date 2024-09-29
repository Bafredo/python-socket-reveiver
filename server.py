import socket
import cv2

HOST = "192.168.102.155"
PORT = 9000
cap = cv2.VideoCapture(0)
print(f"[HOST IP] {HOST}")

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn,addr = s.accept()
    
    
    with conn:
        print(f"Connected via {addr}")
        while True:
            ret,f = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
                b = rgb_image.tobytes()
                conn.sendall(b)
            data = conn.recv(1023)
            d = data.decode("utf-8")
            print(d + "\n")
            
cap.release()