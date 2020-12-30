from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject

# 서버 소켓에서 정보를 받아 윈도우에 띄워주기
class Signal(QObject):
    conn_signal = pyqtSignal()
    recv_signal = pyqtSignal(str)



class ServerSocket:

    def __init__(self, parent):
        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []
        self.conn = Signal()
        self.recv = Signal()
        self.conn.conn_signal.connect(self.parent.updateClient)
        self.recv.recv_signal.connect(self.parent.updateMsg)

    def __del__(self):
        self.stop()

    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)

        try:
            self.server.bind((ip, port))
        except Exception as e:
            print('Bind Error : ', e)
            return False
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.start()
            print('Server Listening...')

        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('서버 멈춤')


    # 클라이언트가 접속할 때마다 새로운 연결을 반복적으로 생성
    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept() # 클라이언트가 접속할 때까지 무한대기
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:
                self.clients.append(client) # 클라이언트 접속시 accept 함수 탈출
                self.ip.append(addr)
                self.conn.conn_signal.emit()
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

        self.removeAllClients()
        self.server.close()


    # 클라이언트가 접속할 때 마다 생성되는 스레드에 의해 실행되는 함수
    def receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.send(msg)
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]:', addr, msg)

        self.removeClient(addr, client)

    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)

    def removeClient(self, addr, client):
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        self.conn.conn_signal.emit()

        i = 0
        for t in self.threads[:]:
            if not t.isAlive():
                del (self.threads[i])
            i += 1

        self.resourceInfo()

    def removeAllClients(self):
        for c in self.clients:
            c.close()

        self.ip.clear()
        self.clients.clear()
        self.threads.clear()

        self.conn.conn_signal.emit()

        self.resourceInfo()



    def translateLanguage(self, msg):
        try:
            for c in self.clients:
                c.send(msg.encode())
        except Exception as e:
            print('Translate() Error : ', e)



    def resourceInfo(self):
        print('Client ip 개수\t: ', len(self.ip))
        print('Client socket 개수\t: ', len(self.clients))
        print('Client thread 개\t: ', len(self.threads))