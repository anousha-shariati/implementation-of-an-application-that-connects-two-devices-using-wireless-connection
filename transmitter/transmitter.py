import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QFont, QImage ,QPixmap
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QPushButton , QLCDNumber ,QFrame , QLineEdit ,QLabel, QMessageBox 
import cv2
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askokcancel
import threading
from datetime import datetime
import time
import os
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import socket
import socket
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image 

30
global ip_val, port_val , server_socket ,frame , cap ,ret



ip_val = ''
port_val = 0  # Initialize with a default value

def audio_record():
    fs = 44100  # Sample rate
    seconds = 30  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('audio.wav', fs, myrecording)  # Save as WAV file 
    QMessageBox.information(None,"audio","your voice is saved successfully")

def audio_play():
    playsound('/Users/My/Desktop/transmitter/record.wav')
    QMessageBox.information(None,"audio","this was your audio ^-^")

def picture_show():  
    image = cv2.imread('/Users/My/Desktop/transmitter/picture.jpg')
    cv2.imshow("photo",image)	
    cv2.waitKey(0)	
    QMessageBox.information(None,"photo","this is your photo ^-^")

def frame_update():
    global label
    global frame ,cap , ret
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        # Convert the frame to QImage and then to QPixmap to display in QLabel
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        pixmap = QPixmap.fromImage(p)
        label.setPixmap(pixmap)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

def video_capture():
    capt=cv2.VideoCapture(0)
    rett,framee = capt.read()
    cv2.imwrite('photo.jpg', framee)
    cv2.wait()  
    capt.release()
    QMessageBox.information(None,"video","your photo is captured successfully")

def ip_entered():
    global ip_val
    ip_val = ip_text.text()
    QMessageBox.information(None, "video", f'Your ip is {ip_val} ')

def port_entered():
    global port_val
    port_val = int(port_text.text())
    QMessageBox.information(None, "video", f'Your port is {port_val} ')

def audio_server():
    host = '0.0.0.0'
    #host= 'localhost'
    port = 500

   # host = ip_val
    #port = port_val
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Picture Server started at {host} on port {port}")
    file_to_send = 'audio.wav'  # Check this path and update it accordingly
    if not os.path.exists(file_to_send):
        print("File does not exist. Exiting...")
        return

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        with open(file_to_send, 'rb') as f:
            data = f.read()
            size = len(data)
            conn.sendall(f"{size}\n".encode('utf-8'))  # Size followed by a newline character
            conn.sendall(data)

        conn.close()
        print("Audio file sent and connection closed.")
        break  

def picture_server():
    #host = '172.20.10.4'
    host = '0.0.0.0'
    #host= 'localhost'
    port = 505

    #host = ip_val
    #port = port_val +5

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Picture Server started at {host} on port {port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        with open('photo.jpg', 'rb') as f:
            data = f.read()
            size = len(data)
            conn.sendall(str(size).encode('utf-8'))
            conn.sendall(data)

        conn.close()
        print("Picture sent and connection closed.")
        break  # close server after sending file

def audio_client():
    host = '172.20.10.12'
    port = 510
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Assuming the first message is the size of the audio file
    size = int(client_socket.recv(1024).decode())
    data = b''
    while len(data) < size:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    # Save the received audio file
    with open('/Users/My/Desktop/transmitter/record.wav', 'wb') as f:
        f.write(data)
        

    client_socket.close()
    QMessageBox.information(None, "Audio", "Audio file received and saved successfully.")



def picture_client():

    host = '172.20.10.12'
    port = 515
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Assuming the first message is the size of the picture file
    size = int(client_socket.recv(1024).decode())
    data = b''
    while len(data) < size:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    # Save the received image file
    with open('/Users/My/Desktop/transmitter/picture.jpg', 'wb') as f:
        f.write(data)

    client_socket.close()
    QMessageBox.information(None, "Picture", "Picture file received and saved successfully.")



def tcp_connect():
    audio_client()
    picture_client()

def send_data():
    threading.Thread(target=audio_server).start()
    threading.Thread(target=picture_server).start()
    QMessageBox.information(None,"send","data is sent successfully")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QWidget()
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(1480, 1000)
    MainWindow.setStyleSheet("background-color: rgb(170, 170, 255);")
    #audio record button
    audio_btn = QPushButton("record audio",MainWindow)
    audio_btn.setGeometry(QtCore.QRect(1025, 650 , 150, 50))       
    audio_btn.setStyleSheet("background-color: rgb(221, 222, 255);")
    audio_btn.setObjectName("audio_btn")
    #video capture button
    video_btn = QPushButton("capture video",MainWindow)
    video_btn.setGeometry(QtCore.QRect(1025, 580, 150, 50))
    video_btn.setStyleSheet("background-color: rgb(221, 222, 255);")
    video_btn.setObjectName("video_btn") 
    #send button
    send_btn = QtWidgets.QPushButton("send",MainWindow)
    send_btn.setGeometry(QtCore.QRect(1025, 790, 150, 50))
    send_btn.setStyleSheet("background-color: rgb(221, 100, 0);")
    send_btn.setObjectName("send_btn")
    #ip text 
    ip_text = QLineEdit(MainWindow)
    ip_text.setGeometry(QtCore.QRect(295, 580, 150, 50))
    ip_text.setStyleSheet("background-color: rgb(119, 126, 255); color: rgb(255, 255, 255);")
    ip_text.setObjectName("ip_text")
    #port text
    port_text = QLineEdit(MainWindow)
    port_text.setGeometry(QtCore.QRect(295, 650, 150, 50))
    port_text.setStyleSheet("background-color: rgb(119, 126, 255); color: rgb(255, 255, 255);")
    port_text.setObjectName("port_text")
    #ip label
    enter_ip = QLabel("enter ip",MainWindow)
    enter_ip.setGeometry(QtCore.QRect(150,585, 100, 20))
    enter_ip.setObjectName("enter_ip")
    
    #port label
    enter_port = QLabel("enter port",MainWindow)
    enter_port.setGeometry(QtCore.QRect(150, 655, 100, 20))
    enter_port.setObjectName("enter_port")

    #audio play button
    audio_ply = QPushButton("play audio",MainWindow)
    audio_ply.setGeometry(QtCore.QRect(1300, 650 , 150, 50))       
    audio_ply.setStyleSheet("background-color: rgb(221, 222, 255);")
    audio_ply.setObjectName("audio_ply")

    #video capture button
    video_ply = QPushButton("show picture",MainWindow)
    video_ply.setGeometry(QtCore.QRect(1300, 580, 150, 50))
    video_ply.setStyleSheet("background-color: rgb(221, 222, 255);")
    video_ply.setObjectName("video_ply")

    #connect button
    connect_btn = QPushButton("connect",MainWindow)
    connect_btn.setGeometry(QtCore.QRect(295, 720, 150, 50))
    connect_btn.setStyleSheet("background-color: rgb(221, 222, 255);")
    connect_btn.setObjectName("connect_btn")

    # Label to display the camera frame
    label = QLabel(MainWindow)
    label.resize(640, 480)
    label.move(790, 50)  

    # Start video capture and update QLabel          
    timer = QTimer(MainWindow)
    timer.start(1000//30)

    #actions
    timer.timeout.connect(frame_update)
    audio_btn.clicked.connect(audio_record)
    video_btn.clicked.connect(video_capture)
    ip_text.returnPressed.connect(ip_entered)
    port_text.returnPressed.connect(port_entered)
    send_btn.clicked.connect(send_data)
    audio_ply.clicked.connect(audio_play)
    video_ply.clicked.connect(picture_show)
    connect_btn.clicked.connect(tcp_connect)


    #show window
    MainWindow.show()
    sys.exit(app.exec_()) 