from __future__ import print_function

NO_OF_CLIENTS = 3 #number of clients to be connected with server
win_score = 5     #points to win the game

import random, socket, sys, threading, time

all_connections = []
all_address = []
first_to_answer = []

# Creating a socket 

def create_socket():
    try:
        global host  #address of server
        global port  #server port
        global  a
        host = ""
        port = 55557
        a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        return a

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections

def binding_socket(a):
    try:
        global host
        global port

        print("Binding the port " + str(port))

        a.bind((host,port))
        a.listen(NO_OF_CLIENTS)

    except socket.error as msg:
        print("Socket Binding error" + str(msg))
        binding_socket()

# Establishing connection with a client(socket must be listening) and clearing all previous data from list so when this file runs all_connections list mustbe empty

def socket_accept(a,all_connections,all_address,num_of_questions):
    for i in all_connections:
        i.close() #clearing previos connections

    #del all_connections[:] #deleting previous connections
    #del all_address[:]

    for i in range(0,NO_OF_CLIENTS):
        try:
            conn,address = a.accept()
            conn.setblocking(1)            #prevents timeout from happening
            all_connections.append(conn)
            all_address.append(address)
            print("Connection has been established " + "IP " + address[0] + " PORT " + str(address[1]))
            time.sleep(0.01)
            all_connections[i].send(str(i))
            time.sleep(0.01)
            all_connections[i].send(str(num_of_questions))

        except socket.error as msg:
            print("Error establishing connection" + str(msg)) 
    
#setting jobs for 2nd thread which are 
# 1) see all clients and select anyone specifically
# 2) interact with them
# turtle> list show all clients list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port

#selecting targets 

def get_target(command):
    try:
        target = command.replace('select ','') #target = id
        target = int(target)
        conn = all_connections(target)
        print("You are now connected to :" + str(all_address[target]))
        print(str(all_address[target][0]) + ">", end="")
        return conn

        #192.160.0.4>.....

    except:
        print("Selection not valid")
        return None
    
#checking the commands

def start_turtle(conn):
    while True:
        command = input()
        if command == 'quit':
            conn.close()
            a.close()
            sys.exit()

        elif command == 'list':
            list_connections()

        elif 'select' in command:
            conn = get_target(command)
            if conn is not None:
                send_target_commands(conn)

        elif command == 'Questions':
            for i in all_connections():
                send_questions(i)

        else:
            print("Command not recognized")

#sending the commands or questions to the clients

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break

            if len(str.encode(cmd)) > 0:
                time.sleep(0.01)
                conn.send(str.encode(cmd))
                client_response= str(conn.recv(20480),"utf-8") #utf-8 for the rsponse to convert in the string
                print(client_response, end="")

        except:
            print("Error sending commands")
            break
            
#display all current active conections with the clients

def list_connections():
    results = ''
    time.sleep(0.01)
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        
        except:
            #del all_connections(i)
            #del all_address(i)
            continue

        results = str(i) + " " + str(all_address[i][0]) + " " + str(all_address[i][1])

    print("--------Clients------" + "\n" + results)

#threading to clients

def threading_clients(all_connections, first_to_answer, all_address, question, pointTable):
    player = []
    for i,conn in enumerate(all_connections):
        player.append(threading.Thread(target = communicate, args = (all_connections, i, question, first_to_answer, pointTable)))

    for i,conn in enumerate(all_connections):
        player[i].start()

    for i,conn in enumerate(all_connections):
        player[i].join()
        
#sending questions to client

def communicate(all_connections, i, question, first_to_answer, pointTable):
    client = all_connections[i]
    time.sleep(0.01)
    client.send(question[0].encode("utf-8"))
    if len(first_to_answer) == 0:
        buzzer = client.recv(1024)    
    if len(first_to_answer) == 0 and buzzer == "y":
        first_to_answer.append(i)
        time.sleep(0.01)
        client.send("1")
        answer = client.recv(1024)
        print("Received answer from client %d is: %s" %(i+1, answer))
        if(answer == question[1]):
            time.sleep(0.01)
            client.send("1")
            pointTable[i] += 1
            print("Correct answer")
            return
        print("Wrong")
        time.sleep(0.01)
        client.send("0")
        return
    time.sleep(0.01)
    client.send("0")
    return
        
#game start_up

def game_start():
    try:
        a = create_socket()
        binding_socket(a)
        print("Waiting for your competitors....")
        Qn_list ={"q1":"a1",\
                  "q2":"a2",\
                  "q3":"a3",\
                  "q4":"a4",\
                  "q5":"a5",\
                  "q6":"a6",\
                  "q7":"a7",\
                  "q8":"a8",\
                  "q9":"a9",\
                  "q10":"a10",\
                  "q11":"a11",\
                  "q12":"a12",\
                  "q13":"a13",\
                  "q14":"a14",\
                  "q15":"a15",\
                  "q16":"a16",\
                  "q17":"a17",\
                  "q18":"a18",\
                  "q19":"a19",\
                  "q20":"a20",\
                  }
        num_of_questions = len(Qn_list)
        socket_accept(a,all_connections,all_address,num_of_questions)
        print("\nGame has started\n")
        play_game(all_connections, Qn_list,first_to_answer)
    except Exception as e:
        print(e)
    finally:
        a.close()

# for playing game

def play_game(all_connections, Qn_list,first_to_answer):
    pointTable = [0]*len(all_connections)
    question = 0
    max_index = 0
    max_score = 0
    while len(Qn_list) !=0:
        question = random.choice(list(Qn_list.items()))
        Qn_list.pop(question[0])
        print("Question : %s" %question[0])
        threading_clients(all_connections,first_to_answer,all_address, question, pointTable)
        if len(first_to_answer)!=0:
            first_to_answer.pop(0)
        try:
            winner = pointTable.index(win_score)
            points = ""
            for i in range(len(all_connections)):
                points = points + " " + str(pointTable[i])
            for i in range(len(all_connections)):
                time.sleep(0.01)
                all_connections[i].send(points)
                time.sleep(0.1)
                all_connections[i].send("Game is Over. Winner is Player %s" %str(winner+1))
                time.sleep(0.01)
                all_connections[i].close()
            print("Game Over. Winner is Player %s" %str(winner+1))
            a.close()
            return
        except ValueError:
            points = ""
            for i in range(len(all_connections)):
                points = points + " " + str(pointTable[i])
            for i in range(len(all_connections)):
                time.sleep(0.01)
                all_connections[i].send(points)
            temp_max = max(pointTable)
            if max_score < temp_max:
                max_score = temp_max
                max_Index = pointTable.index(temp_max)
            time.sleep(1)
    if max_score == 0:
        for conn in all_connections:
            time.sleep(0.01)
            conn.send("Game over. No Winner. ALL players have same points")
        print("Game over. No winner.")
        conn.close()
        a.close()
        return
    for conn in all_connections:
        time.sleep(0.01)
        conn.send("Game Over. Winner is %s" %str(max_Index+1)) #client close
    print("Game Over. Winner is %s" %str(max_Index+1))
    conn.close()
    a.close()
    return
game_start()
    
