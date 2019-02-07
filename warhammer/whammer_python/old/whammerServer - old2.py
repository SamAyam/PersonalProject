#!/usr/bin/python           # This is server.py file

import socket, threading, pickle, struct, socketserver

class Player():
    pass

class Statue():
    pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = recv_one_message(self)
        cur_thread = threading.current_thread()
        response = "{}".format(cur_thread.name)
        send_one_message(self, response)
        #self.request.sendall(response)

class string_to_allThread (threading.Thread):
   def __init__(self, message,excpt='none'):
      threading.Thread.__init__(self)
      self.excpt=excpt
      self.message=message
   def run(self):
      for guy in clientlist:
         if guy[0]!=self.excpt[0]:
             send_one_message(guy[2], self.message)

class event_to_allThread (threading.Thread):
   def __init__(self, message,excpt='none'):
      threading.Thread.__init__(self)
      self.excpt=excpt
      self.message=message
   def run(self):
      for guy in clientlist:
         if guy[0]!=self.excpt[0]:
            send_one_message(guy[2], self.message)
            #guy.send(self.message)

class newThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global clienteventlists, clientlist, serv
        serv.listen(5)                 # Now wait for client connection.
        c, addr = serv.accept()     # Establish connection with client.
        print('Got connection from'+ str(addr))
        send_one_message(c, "Connected successfully".encode('utf-8'))
        #c.send("Connected successfully".encode("utf-8"))
        #clienteventlists.append([c, ["connected"]])
        who=recv_one_message(c).decode('utf-8')
        if who=='recv':
            parent=(recv_one_message(c).decode('utf-8'))
            for dude in clientlist:
                if dude[0]==parent:
                    dude.append(c)
                    thread1 = for_each_clientThread(dude)
                    thread1.start()
        elif who=='send':
            send_one_message(c, str(addr).encode('utf-8'))
            clientlist.append([str(addr), c])

      
      
class for_each_clientThread (threading.Thread):
   def __init__(self,guy):
      threading.Thread.__init__(self)
      self.guy=guy
   def run(self):
      global clienteventlists, clientlist
      #print(do)
      #do=self.guy.recv(16000)
      #thread2 = for_each_clientThread(self.guy)
      #thread2.start()
      self.done = False
      while self.done==False:
          do=recv_one_message(self.guy[1])
          try:
             newdo=pickle.loads(do)
             #print(newdo)
             if newdo == 'get_all_sprites':
                reply_to=self.guy[0]
                #return_events(self.guy)
                print(str([newdo,reply_to]))
                sending=event_to_allThread(pickle.dumps([newdo,reply_to]),excpt=self.guy)
                sending.start()
                sending.join()
             elif newdo[0] == 'just_one':
                #print("yaay")
                reply_to=newdo[1]
                #print(reply_to)
                reply=newdo[2]
                for dude in clientlist:
                    #print(dude[0])
                    if str(dude[0])==reply_to:
                        print("sent")
                        send_one_message(dude[2], pickle.dumps(reply))
             elif newdo == 'close':
                #add_to_list('disconnected', self.guy)
                self.guy[1].close()                # Close the connection
                self.guy[2].close()
                clientlist.remove(self.guy)
                print("Connection closed")
                self.done=True
             elif newdo ==b'testing':
                print("\nclientlist:\n"+str(clientlist))
                print("\nclienteventlists:\n"+str(clienteventlists))
             #elif newdo =="get_all_sprites":
                #print("working")
             elif newdo !="" and do!='connected'and do!='disconnected':
                   #print(newdo)
                   #add_to_list(do, self.guy)
                   #self.guy.send("server recieved info".encode("utf-8"))
                   sending=string_to_allThread(pickle.dumps(newdo),excpt=self.guy)
                   sending.start()
                   sending.join()
          except UnicodeDecodeError:
             #print(pickle.loads(do))
             #print(do)
             sending=event_to_allThread(do,excpt=self.guy)
             sending.start()
             sending.join()
          except AttributeError:
             sending=event_to_allThread(do,excpt=self.guy)
             sending.start()
             sending.join()
              
    

def send_one_message(sck, data):
    length = len(data)
    sck.send(struct.pack('!I', length))
    send_again=recvall(sck, 4)
    while struct.unpack('!I', send_again)[0] != length:
        empty_socket(sck)
        sck.send(struct.pack('!I', 0))
        sck.send(struct.pack('!I', length))
        send_again=recvall(sck, 4)
    sck.send(struct.pack('!I', 1))
    sck.send(data)
    message=recvall(sck, length)
    while message!=data:
        #print(message)
        #print(data)
        empty_socket(sck)
        sck.send(struct.pack('!I', 0))
        sck.send(data)
        message=recvall(sck, length)
    sck.send(struct.pack('!I', 1))

def recv_one_message(sck):
    lengthbuf = recvall(sck, 4)
    sck.send(lengthbuf)
    got_it=recvall(sck, 4)
    while struct.unpack('!I', got_it)[0] ==0:
        empty_socket(sck)
        lengthbuf = recvall(sck, 4)
        sck.send(lengthbuf)
        got_it=sck.recv(4)
    length, = struct.unpack('!I', lengthbuf)
    message=recvall(sck, length)
    reply=sck.send(message)
    got_it=recvall(sck, 4)
    while struct.unpack('!I', got_it)[0] ==0:
        empty_socket(sck)
        message=recvall(sck, length)
        reply=sck.send(message)
        got_it=sck.recv(4)
    return message

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf            

def empty_socket(sock):
    """remove the data present on the socket"""
    #sock.recv(16000)
    pass

def return_events(thisguy):
   global clienteventlists
   templist=[]
   for client in clienteventlists:
      #if client[0]==thisguy:
      #if client[0]!=thisguy:
         for thing in client[1]:
            templist.append(thing)
   thisguy.send(str(templist).encode('utf-8'))

def add_to_list(add, towho):
   global clienteventlists
   for client in clienteventlists:
      if client[0]==towho:
         client[1].append(add)

##def for_each_client(guy):
##   global clienteventlists
##   done=False
##   while done==False:
##      do=(guy.recv(1024).decode('utf-8'))
##      if do == 'get':
##         return_events(guy)
##      elif do == 'close':
##         add_to_list('disconnected', guy)
##         #clienteventlists[guy]append([guy, "disconnected"])
##         guy.send("Disconnected".encode("utf-8"))
##         guy.close()                # Close the connection
##         clientlist.remove(guy)
##         print("Connection closed")
##         #s.listen(5)
##         #c2, addr = s.accept()     # Establish connection with client. 
##         #print('Got connection from'+ str(addr))
##         #c2.send("Connected successfully".encode("utf-8"))
##         #clientlist.append(c2)
##         #clienteventlists.append([c2, ['connected again']])
##         done=True
##      elif do =='testing':
##         print(clienteventlists)
##      elif do !="" and do!='connected'and do!='disconnected':
##            print(do)
##            add_to_list(do, guy)
##            #clienteventlists.append([guy, do])
##            guy.send("server recieved info".encode("utf-8"))
##            #print(clienteventlists)
##   print("done")

##def new_guy():
##   print("start")
##   global clienteventlists, clientlist, port, host
##   port+=1
##   s = socket.socket()
##   s.bind((host, port))        # Bind to the port
##   done=False
##   clientlist=[]
##   s.listen(5)                 # Now wait for client connection.
##   c, addr = s.accept()     # Establish connection with client. 
##   print('Got connection from'+ str(addr))
##   c.send("Connected successfully".encode("utf-8"))
##   clientlist.append(c)
##   clienteventlists.append([c, ["connected"]])
##   thread1 = threading.Thread(for_each_client(c))
##   print("and back")
##   thread2 = threading.Thread(new_guy())
##   thread1.start()
##   thread2.start()
##   #threading.start_new_thread(new_guy())
   


#clienteventlists=[]
clientlist=[]

host = socket.gethostname() # Get local machine name
port = 12345               # Reserve a port for your service.
#serv = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
#server = threading.Thread(target=serv.serve_forever)
#server.start()
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((host, port))        # Bind to the port#not needed with socketserver?

#new_guy()
print("Whammer Server Running\n\n")
while 1:
   newguy=newThread()
   newguy.start()
   newguy.join()
   #for cl in clientlist:
   #  for_each_client(cl)
