import os, sys
from grepfunc import grep
from datetime import datetime

class FlagError(Exception): pass
class MissingRequiredArgument(Exception): pass
class ArgumentError(Exception): pass
class NoCommandError(Exception): pass
class InvalidArgument(Exception): pass
    
idir = os.getcwd()
dirs = os.listdir(idir)
initial = datetime.now()

global starttime, starth, startm, starts, cmds
starttime = initial.strftime("%H:%M:%S")
starth = int(initial.strftime("%H"))
startm = int(initial.strftime("%M"))
starts = int(initial.strftime("%S"))
cmds = ["help", "uptime", "time", "cwd", "search", "history", "clear", "exit", "ls"]
cmds.sort()

def help(query=None):
    try: 
        if query == None: print("\n".join(cmds) + "\n\n-Use help <command> to get detailed information-")
        elif query == "help": print("help - no description provided.")
        elif query == "uptime": print("uptime - elapsed time of this program.")
        elif query == "time": print("time - current time.")
        elif query == "cwd": print("cwd - currently working directory.")
        elif query == "search": print("search - file searching.")
        elif query == "history": print("history - command history.")
        elif query == "clear": print("clear - clean up display.")
        elif query == "exit": print("exit - exit program.")
        elif query == "ls": print("ls - list directory contents.")
        else: raise NoCommandError
    except NoCommandError: print("Help: NoCommandError: No such command.")

def ls(arg=None):
    j = os.getcwd()
    k = os.listdir(j)
    l = []
    if arg == None:
        for i in k:
            if i.startswith("."): pass
            else: l.append(i)
        l.sort()
        return print("\n".join(l))
    elif arg == "-a":
        l.extend([".", ".."])
        l.extend(k)
        l.sort()
        return print("\n".join(l))
    elif arg == "-A":
        k.sort()
        return print("\n".join(k))
    elif arg == "-m":
        for i in k:
            if i.startswith("."): pass
            else: l.append(i)
        l.sort()
        return print(", ".join(l))
    else: raise InvalidArgument
        
def ctime():
    global getnow
    getnow = datetime.now()
    t = getnow.strftime("%H:%M:%S")
    return t

def uptime():
    h = int(datetime.now().strftime("%H"))
    m = int(datetime.now().strftime("%M"))
    s = int(datetime.now().strftime("%S"))
    uh = h - starth
    um = m - startm
    us = s - starts
    return uh, um, us
    
def search(arg, flag=None):
    try:
        if flag == None:
            result = grep(dirs, arg)
            count = grep(dirs, arg, c=True)
        elif flag == "w": #exact word
            result = grep(dirs, arg, w=True)
            count = grep(dirs, arg, w=True, c=True)
        elif flag == "i": #ignore case
            result = grep(dirs, arg, i=True)
            count = grep(dirs, arg, i=True, c=True)
        elif flag == "x": #exact line
            result = grep(dirs, arg, x=True)
            count = grep(dirs, arg, x=True, c=True)
        elif flag == "ix" or flag == "xi":
            result = grep(dirs, arg, x=True, i=True)
            count = grep(dirs, arg, x=True, i=True, c=True)
        elif flag == "iw" or flag == "wi":
            result = grep(dirs, arg, w=True, i=True)
            count = grep(dirs, arg, w=True, i=True, c=True)
        elif flag == "wx" or flag == "xw":
            result = grep(dirs, arg, w=True, x=True)
            count = grep(dirs, arg, w=True, x=True, c=True)
        elif len(flag) > 2: raise ArgumentError
        else: raise FlagError
        return result, count
    except ArgumentError: print("Search: ArgumentError: Too many flags.")
    except FlagError: print("Search: FlagError: No such flag(s).")
    
def clear(): os.system("cls") if os.name == "nt" else os.system("clear")

def exit(): sys.exit(0)

def history():
    f = open("history.txt", "r")
    lines = f.readlines()
    e = []
    for i in lines: e.append(i)
    return e
    
def main():
    global a, trim
    a = input(">>> ")
    trim = a.strip()
    if len(trim) < 1: pass
    else:
        f = open("history.txt", "a")
        f.write(f"{trim}\n")
        f.close()
    return trim

while True:
    main()
    n = trim.split()
    if len(trim) < 1: pass
    elif n[0] not in cmds: print(f"Invalid command: {trim}")
    elif trim == "time": print(ctime())
    elif "search" in trim and not trim.startswith("help"):
        try:
            s = trim.split()
            if len(s) < 2: raise MissingRequiredArgument
            elif len(s) < 3:
                tar = s[1]
                result, count = search(tar)
            else:
                tar = s[1]
                flag = s[2]
                result, count = search(tar, flag)
            print(f"{count} results found:\n"+"\n".join(result))
        except TypeError: pass
        except MissingRequiredArgument: print("search: MissingRequiredArgument: Missing 1 or more arguments.")
    elif trim == "clear": clear()
    elif trim == "exit": exit()
    elif trim == "cwd": print(os.getcwd())
    elif trim == "history":
        d = -1
        e = history()
        for g in e:
            d += 1
            print(f"{d}{(6 - len(str(d))) * ' '} {g.strip()}")
    elif trim == "uptime":
        uh, um, us = uptime()
        print(f"{uh}h {um}m {us}s")
    elif "ls" in trim and not trim.startswith("help"):
        try:
            s = trim.split()
            if len(s) > 2: raise ArgumentError
            elif len(s) == 2:
                m = s[1]
                arg = ls(m)
            else: ls()
        except ArgumentError: print("ls: ArgumentError: Too many arguments.")
        except InvalidArgument: print("ls: InvalidArgument: Invalid arguments")
"""
    elif trim == "debug":
        global c
        c = 0
        print(f"{c}-{ctime()}")
        c += 1
        print(f"{c}-{search(sys.argv[0])}")
        c += 1
        print(f"{c}-{idir}")
        c += 1
        print(f"{c}-{dirs}")
        c += 1
        print(f"{c}-{starttime}")
        c += 1
        print(f"{c}-{trim}")
        c += 1
        print(f"{c}-{uptime()}")
        c += 1
        print(f"{c}-{history()}")
        c += 1
        print(f"{c}-{ls()}")
"""
    elif "help" in trim:
        try:
            s = trim.split()
            if len(s) > 2: raise ArgumentError
            elif len(s) == 2:
                arg = s[1]
                query = help(arg)
            else: help()
        except ArgumentError: print("help: ArgumentError: Too many arguments.")
    else: pass
