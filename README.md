# Local-Network-Remote-Desktop-Streaming-Control-System
Python based Low-latency remote desktop control application utilizing UDP for real-time input and screen sharing, featuring automatic peer discovery via IP broadcasting within a local network. Provides a peer-to-peer based architecture where either user can act as the server or client. The App additionally utilizes user friendly UI meant for ease of use.

## **Project Features** 
* Low Latency Transportation of Data: Utilizes UDP data transfer which allows for the process of sending data to be quick
* IP Broadcasting: Implemnted a IP Broadcast system which works to allow for users within the same network to be automatically connected if one is on server and the other is on client. Prevents the need for hardcoding an IP
* Peer to Peer Architecture: Utilizes a Peer to Peer based architecture structure, allowing for a user to act as either a client or server depending on the their chose (as long as their is a matching peer who acts as the opposing type).
* Real Time Screen Sharing: Server send user screen data to the client through UDP sockets. The client works to decipher and put these frames together in a way to not overload the socket and program. Allows for client to properly view the frames of servers screen with low latency.
* Input Data Transference: Client documents and immediately sends user input data to server side through UDP sockets. The server utilizes the input data as controls on local machine. This allows for the client to imitate 'Control' of the server machine.

## Simple Architecture Visualiation
<img width="1028" height="785" alt="Architecture Drawing" src="https://github.com/user-attachments/assets/8f318d9a-71b7-479a-97e9-08f0d283a5b8" />

## Usage
#### Cloning/Downloading Files
To begin the process of utilizing the application, you must move the files onto your own machine. This can be achieved through one of two ways: cloning the repo or downloading all the files.
  * Cloning would be the easier of the two, requiring the user to create a new directory within their computer desktop, and running this command within the terminal:
    - git clone https://github.com/CompleteCanoe98/Local-Network-Remote-Desktop-Streaming-Control-System.git (assuming git is installed on their machine)
  * Downloading the files would need for you to download each individual file to your computer, and would require you to ensure all the directories names and file paths stay consistent with the ones defined in the project (Unless specifically directed to go elsewhere in main)

#### Requirements
In order to properly run, any version of python 3.x that natively has tkinter is required. Additionally, the following dependencies must be installed:
 - openCV
 - numpy (Comes with OpenCV)
 - pynput
 - PyQt6
 - pyautogui
 - mss
   
It is recommended that a python virtual environment is utilized to host dependencies. Ensure all dependencies are reachable from the project directory. A requirements.txt file has been provided to allow for ease of installation. Running the command: 

* **pip install requirements.txt**

should install all required dependencies. If there exists issues doing it that way, pip installing one by one is a possible solution.

#### Application Running
After ensuring all files and dependencies are downloaded, you are now able to run the program. If using a virtual machine make sure it is activated to allow for dependencies to be active. Ensure you are in the correct working directory, then run the main.py file.

This will produce the following GUI:

<img width="803" height="629" alt="Screenshot 2025-11-23 at 10 45 59 AM" src="https://github.com/user-attachments/assets/3e68d769-cd9b-4885-9161-0ce00e8a6db8" />


This allows the user to chose one of the two following options:

- Server: Broadcasts a signal out. Will wait until a client finds server, then starts the data trasnfer process, sending frame data and recieving input data from the client.
- Client: Looks for the Broadcasted signal, if it is not found it will stop the client program from running and will require it to be pressed again. If a broadcast signal is found within the network, it will begin the data transfer process, recieving fram data and sending input data.

*This project requires that there are TWO machines that are on the same network in order to work. Will not work if there is only one machine or if the two machines are on seperate networks.

  
