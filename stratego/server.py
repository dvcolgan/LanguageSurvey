import socket
import select
import cPickle

board = [
['red1','red2','red3','red3','.','.','.','.','.','.','.','.','.','.','.','.','blue1','blue2','blue3','blue3'],
['red4','red4','red4','red5','.','.','.','.','.','.','.','.','.','.','.','.','blue4','blue4','blue4','blue5'],
['red5','red5','red5','red6','.','.','.','.','.','.','.','.','.','.','.','.','blue5','blue5','blue5','blue6'],
['red6','red6','red6','red7','.','.','.','.','.','.','.','.','.','.','.','.','blue6','blue6','blue6','blue7'],
['red7','red7','red7','red8','.','.','.','.','.','.','.','.','.','.','.','.','blue7','blue7','blue7','blue8'],
['red8','red8','red8','red8','.','.','.','.','.','.','.','.','.','.','.','.','blue8','blue8','blue8','blue8'],
['red9','red9','red9','red9','.','.','.','.','.','.','.','.','.','.','.','.','blue9','blue9','blue9','blue9'],
['red9','red9','red9','red9','.','.','.','.','.','.','.','.','.','.','.','.','blue9','blue9','blue9','blue9'],
['reds','redb','redb','redb','.','.','.','.','.','.','.','.','.','.','.','.','blues','blueb','blueb','blueb'],
['redb','redb','redb','redf','.','.','.','.','.','.','.','.','.','.','.','.','blueb','blueb','blueb','bluef']
]

class StrategoServer:

    def __init__(self, port):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen(5)

        self.allsocks = [self.sock]
        print 'Started Stratego server on port %s' % self.port

    def run(self):

        while 1:
            (sread, swrite, sexc) = select.select(self.allsocks, [], [])
            for sock in sread:
                if sock == self.sock:
                    self.new_connection()
                else:
                    msg = sock.recv(10000)
                    """
                    Packet format
                    'tag:msg'
                    tags from the client:
                    chat = 'chat:Hello this is a chat'
                    move = 'move:((0,1), (0,2))' <- tuple is pickled
                    
                    """
                    if msg == '':
                        host, port = sock.getpeername()
                        self.allsocks.remove(sock)
                        print 'player disconnected'
                    else:
                        try:
                            tag, body = msg.split(':',1)
                            if tag == 'chat':
                                self.broadcast(body)
                                print body
                            elif tag == 'move':
                                ((x1, y1), (x2, y2)) = cPickle.loads(body)
                                if board[y2][x2] == '.' and board[y1][x1] != '.':
                                    board[y2][x2] = board[y1][x1]
                                    board[y1][x1] = '.'
                                    print (x1, y1, x2, y2)
                            self.broadcast(cPickle.dumps(board))
                        except:
                            print 'got bad packet: %s' % msg

    def broadcast(self, msg):
        for sock in self.allsocks:
            if sock != self.sock:
                sock.send(msg)

    def new_connection(self):
        sock, (host, port) = self.sock.accept()
        self.allsocks.append(sock)
        print 'Client joined from %s:%s' % (host, port)
        sock.send(cPickle.dumps(board))

if __name__ == "__main__":
    server = StrategoServer(9999)
    server.run()


