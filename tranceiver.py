import socket
import cv2
import struct
import threading


def send_video_frames(conn):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        

        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()


        conn.sendall(struct.pack("!I", len(data)))
        conn.sendall(data)

    cap.release()


def receive_data(conn):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(data)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.102.193', 9000))
server_socket.listen(1)

print("Waiting for a connection...")
conn, addr = server_socket.accept()
print(f"Connection from {addr}")


send_thread = threading.Thread(target=send_video_frames, args=(conn,))
receive_thread = threading.Thread(target=receive_data, args=(conn,))


send_thread.start()
receive_thread.start()


send_thread.join()
receive_thread.join()


conn.close()
server_socket.close()
