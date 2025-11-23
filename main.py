import PyQt6
import sys
import os

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QMovie
from PyQt6.QtCore import Qt, QProcess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Keep track of all processes
        self.p_server_video = None
        self.p_server_input = None
        self.p_client_video = None
        self.p_client_input = None

        self.setWindowTitle("Stream App")
        self.resize(800, 600)
        self.setStyleSheet("background-color: black;")

        # --- DYNAMIC PATH SETUP ---
        # This finds the folder where main.py is running
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct paths to your scripts regardless of user/computer
        self.path_server_video = os.path.join(self.base_dir, "Server", "serverVideo.py")
        self.path_server_input = os.path.join(self.base_dir, "Server", "serverInput.py")
        self.path_client_video = os.path.join(self.base_dir, "Client", "clientVideo.py")
        self.path_client_input = os.path.join(self.base_dir, "Client", "clientInput.py")

        layout = QVBoxLayout(self)

        mainLabel = QLabel("Screen Streaming Application")
        mainLabel.setFont(QFont("Comic Sans MS", 35, QFont.Weight.Bold))
        mainLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        mainLabel.setStyleSheet("color: white;") # Added color so it's visible on black

        gifLabel = QLabel()
        # Make sure monkey_wave.gif is in the same folder as main.py
        gif_path = os.path.join(self.base_dir, "monkey_wave.gif")
        if os.path.exists(gif_path):
            gif = QMovie(gif_path)
            gifLabel.setMovie(gif)
            gif.start()
        else:
            gifLabel.setText("(GIF not found)")
            gifLabel.setStyleSheet("color: white;")

        labelForChoice = QLabel("Choose to be a Server or Client")
        labelForChoice.setFont(QFont("Comic Sans MS", 20))
        labelForChoice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        labelForChoice.setStyleSheet("color: white;")

        button1 = QPushButton("Server")
        button1.setFont(QFont("Comic Sans MS", 30))
        button1.setStyleSheet("background-color: #444; color: white;")
        button1.clicked.connect(self.on_server_button_clicked)

        button2 = QPushButton("Client")
        button2.setFont(QFont("Comic Sans MS", 30))
        button2.setStyleSheet("background-color: #444; color: white;")
        button2.clicked.connect(self.on_client_button_clicked)

        layout.addWidget(mainLabel)
        layout.addWidget(gifLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(labelForChoice)
        layout.addWidget(button1)
        layout.addWidget(button2)

    # ----------------------------
    # Server Button
    # ----------------------------
    def on_server_button_clicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Server Selected")
        msg.setText("Starting Video Stream and Input Server...")
        msg.exec()

        # UI for the active server state
        exit_window = QWidget()
        exit_window.setWindowTitle("Server Mode")
        exit_window.resize(600, 300)
        
        exit_label = QLabel("Server is Live.\nVideo & Input Active.\nPress Exit to stop.", exit_window)
        exit_label.setFont(QFont("Comic Sans MS", 18))
        exit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        exit_button = QPushButton("Exit", exit_window)
        exit_button.setFont(QFont("Comic Sans MS", 24))

        layout = QVBoxLayout(exit_window)
        layout.addWidget(exit_label)
        layout.addWidget(exit_button)
        exit_window.show()

        # --- START PROCESSES ---
        # 1. Start Video Server
        self.p_server_video = QProcess(self)
        self.p_server_video.start(sys.executable, [self.path_server_video])

        # 2. Start Input Server
        self.p_server_input = QProcess(self)
        self.p_server_input.start(sys.executable, [self.path_server_input])

        def stop_server():
            # Kill both processes
            if self.p_server_video:
                self.p_server_video.kill()
            if self.p_server_input:
                self.p_server_input.kill()
            exit_window.close()

        exit_button.clicked.connect(stop_server)

    # ----------------------------
    # Client Button
    # ----------------------------
    def on_client_button_clicked(self):
        msg = QMessageBox()
        msg.setText("Client starting...\nLooking for Server...")
        msg.exec()

        # --- START PROCESSES ---
        # 1. Start Video Client
        self.p_client_video = QProcess(self)
        self.p_client_video.start(sys.executable, [self.path_client_video])

        # 2. Start Input Client
        self.p_client_input = QProcess(self)
        self.p_client_input.start(sys.executable, [self.path_client_input])

    # Ensure we kill processes if the main window is closed
    def closeEvent(self, event):
        if self.p_server_video: self.p_server_video.kill()
        if self.p_server_input: self.p_server_input.kill()
        if self.p_client_video: self.p_client_video.kill()
        if self.p_client_input: self.p_client_input.kill()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())