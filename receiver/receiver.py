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
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image 


global ip_val, port_val

def audio_play():
    playsound('/Users/My/Desktop/receiver/audio.wav')
    QMessageBox.information(None,"audio","this was your audio ^-^")

def picture_show():  
    image = cv2.imread('/Users/My/Desktop/receiver/photo.jpg')
    cv2.imshow("photo",image)	
    cv2.waitKey(0)	
    QMessageBox.information(None,"photo","this is your photo ^-^")

def ip_entered():
    global ip_val, port_val
    ip_val = ip_text.text()

def port_entered():
    global ip_val, port_val
    port_val = int(port_text.text())



def audio_client():
    host = 'localhost'
    port = 500
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
    with open('/Users/My/Desktop/receiver/audio.wav', 'wb') as f:
        f.write(data)

    client_socket.close()
    QMessageBox.information(None, "Audio", "Audio file received and saved successfully.")


def picture_client():
    host = 'localhost'
    port = 505
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
    with open('/Users/My/Desktop/receiver/photo.jpg', 'wb') as f:
        f.write(data)

    client_socket.close()
    QMessageBox.information(None, "Picture", "Picture file received and saved successfully.")

def tcp_connect(): #for send button
  #threading.Thread(target=audio_client, daemon=True).start()    
  #threading.Thread(target=picture_client, daemon=True).start()
    audio_client()
    picture_client()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QWidget()
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(1480, 1000)
    MainWindow.setStyleSheet("background-color: rgb(170, 170, 255);")
    #audio play button
    audio_btn = QPushButton("play audio",MainWindow)
    audio_btn.setGeometry(QtCore.QRect(1025, 650 , 150, 50))       
    audio_btn.setStyleSheet("background-color: rgb(221, 222, 255);")
    audio_btn.setObjectName("audio_btn")
    #video capture button
    video_btn = QPushButton("show picture",MainWindow)
    video_btn.setGeometry(QtCore.QRect(1025, 580, 150, 50))
    video_btn.setStyleSheet("background-color: rgb(221, 222, 255);")
    video_btn.setObjectName("video_btn")
    #connect button
    connect_btn = QPushButton("connect",MainWindow)
    connect_btn.setGeometry(QtCore.QRect(295, 720, 150, 50))
    connect_btn.setStyleSheet("background-color: rgb(221, 222, 255);")
    connect_btn.setObjectName("connect_btn")
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
    
    #actions
    audio_btn.clicked.connect(audio_play)
    video_btn.clicked.connect(picture_show)
    #ip_text.returnPressed.connect(ip_entered)
    #port_text.returnPressed.connect(port_entered)
    connect_btn.clicked.connect(tcp_connect)

    #show window
    MainWindow.show()
    sys.exit(app.exec_()) 