import socket

msg = "collect"

collect_data = {
        'x': [],
        'y': [],
        'z': []
}

# Echo client program
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 5002))
        s.sendall(msg.encode("UTF-8"))
        # Decode first byte
        data = s.recv(64).decode('UTF-8')
        batch = ''
        print(data)
        while data != '':
                data = s.recv(2048)
                data = data.decode("UTF-8")
                batch += data
        s.shutdown(0)
        s.close()
        batch = batch.split(',')
        del batch[-1]
        print(batch)
        print(len(batch))
