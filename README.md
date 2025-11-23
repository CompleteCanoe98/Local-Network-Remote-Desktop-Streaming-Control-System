# Local-Network-Remote-Desktop-Streaming-Control-System
Low-latency remote desktop control application utilizing UDP for real-time input and screen sharing, featuring automatic peer discovery via IP broadcasting within a local network. Provides a peer-to-peer based architecture where either user can act as the server or client. The App additionally utilizes user friendly UI meant for ease of use.

## **Project Features** 
* Low Latency Transportation of Data: Utilizes UDP data transfer which allows for the process of sending data to be quick
* IP Broadcasting: Implemnted a IP Broadcast system which works to allow for users within the same network to be automatically connected if one is on server and the other is on client. Prevents the need for hardcoding an IP
* Peer to Peer Architecture: Utilizes a Peer to Peer based architecture structure, allowing for a user to act as either a client or server depending on the their chose (as long as their is a matching peer who acts as the opposing type).
* Real Time Screen Sharing: Server send user screen data to the client through UDP sockets. The client works to decipher and put these frames together in a way to not overload the socket and program. Allows for client to properly view the frames of servers screen with low latency.
* Input Data Transference: Client documents and immediately sends user input data to server side through UDP sockets. The server utilizes the input data as controls on local machine. This allows for the client to imitate 'Control' of the server machine.
