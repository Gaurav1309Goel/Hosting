from __future__ import print_function

import socket, threading, sys, time
host = ""
port = 55557
score = 5
global win
global client
global client_number
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
client_number = client.recv(1024)
print("You are a player %s" %client_number)
print("Press y if you know the answer otherwise press n")

def game():
    win = 1
    num_question = int(client.recv(1024))
    for i in range(num_question):
        question = client.recv(1024)

        print(question[:-23] + "\n" + question[-23:])

        buzzer = raw_input()
        client.send(buzzer)

        checking = client.recv(1024)

        if checking == "0":
            print("Not your chance")

        else:
            print("Answee the following question: ")
            answer = raw_input()
            client.send(answer)

            answer_checking = client.recv(1)
            if answer_checking == '1':
                print("Correct Answer Player")
            else:
                print("Wrong Answer")
        question_ending = client.recv(1024)
        l = question_ending.split()
        for i in range(len(l)):
            if int(l[i]) == score:
                win = 0
        if win == 0:
            if int(l[int(client_number)]) == score:
                print("You won the match")
                msg = client.recv(1024)
                print(msg)
                time.sleep(0.04)
                client.close()
                return
            else:
                print("You lose")
                client.close()
                return
        else:
            print("Player Score")
            for i in range(len(l)):
                print(str(i) + "  " +  "{0}".format(l[i]))
    winning_message = client.recv(1024)
    time.sleep(1)
    print(winning_message)
    client.close()

game()
