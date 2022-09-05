from __future__ import print_function
import select
import Pyro4
import Pyro4.core
import Pyro4.socketutil
import rsa


@Pyro4.expose
class FileServer(object):
    def get_with_pyro(self,):
        with open('data.txt', 'r') as f:
            data = f.read()
            with open("public_key.txt", "rb") as public_file:
                publicKey = rsa.PublicKey.load_pkcs1(public_file.read())
            encryptedData=rsa.encrypt(data.encode(), publicKey)
        return encryptedData


class FileServerDaemon(Pyro4.core.Daemon):
    def __init__(self, host=None, port=0):
        super(FileServerDaemon, self).__init__(host, port)
        host, _ = self.transportServer.sock.getsockname()
        self.blobsocket = Pyro4.socketutil.createSocket(bind=(host, 0), timeout=Pyro4.config.COMMTIMEOUT, nodelay=False)
        
        
    def close(self):
        self.blobsocket.close()
        super(FileServerDaemon, self).close()

    def requestLoop(self, loopCondition=lambda: True):
        while loopCondition:
            rs = [self.blobsocket]
            rs.extend(self.sockets)
            rs, _, _ = select.select(rs, [], [], 3)
            daemon_events = []
            for sock in rs:
                if sock in self.sockets:
                    daemon_events.append(sock)
                elif sock is self.blobsocket:
                    self.handle_blob_connect(sock)
            if daemon_events:
                self.events(daemon_events)


with FileServerDaemon(host=Pyro4.socketutil.getIpAddress("")) as daemon:
    uri = daemon.register(FileServer, "example.transfer")
    print("Filetransfer server URI:", uri)
    daemon.requestLoop()
