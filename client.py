import cv2
import socket
import struct
import pickle

# Specify the IP address and port for the Android client
server_address = '192.168.102.193'  # Replace with your Android device's IP address
server_port = 9000  # Port to use for streaming

# Create a socket
s = socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_address, server_port))
s.listen()
con,addr = s.accept()
# Open the webcam
cap = cv2.VideoCapture(0)

# Ensure the connection and camera are open
if not cap.isOpened():
    print("Error: Unable to access the camera")
    exit()

# Set the quality of the video stream
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

try:
    while True:
        # Capture frame-by-frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame as a JPEG to compress it
        result, frame_encoded = cv2.imencode('.jpg', frame, encode_param)

        # Serialize the frame using pickle
        frame_data = pickle.dumps(frame_encoded, 0)

        # Send the length of the data (4 bytes) followed by the frame itself
        frame_size = struct.pack(">L", len(frame_data))
        con.sendall(frame_size + frame_data)

finally:
    # Release the camera and close the socket
    cap.release()
    con.close()
    print("Connection closed")
