import bluetooth
import math

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

server_sock.bind(("", bluetooth.PORT_ANY ))
port = server_sock.getsockname()[1]
server_sock.listen(1)
print "listening on port %d" % port

uuid = "2f3b0104-fcb0-4bcf-8dda-6b06390c3c1a"
bluetooth.advertise_service( server_sock, "FooBar Service", uuid )

client_sock,address = server_sock.accept()
print "Accepted connection from ",address

try:
    while True:
        data = client_sock.recv(1024)
        print "received [%s]" % data

        dataInt = int(data)
        sendData = ""
        
        for i in range(dataInt):
            sendData = sendData + str(math.sin(i * math.pi * 6 / float(dataInt)) * float(i)) + " "

        sendData = sendData + "s "

        for i in range(dataInt):
            sendData = sendData + str(float(i) / float(2)) + " "

        sendData = sendData + "w"    
            
            
        print "now sending [%s]" % sendData
        client_sock.send(sendData)
except IOError:
    pass
        
client_sock.close()
server_sock.close()
