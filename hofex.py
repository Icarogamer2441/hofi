import sys
import hofivm as vm

funcs = {}
mem = []
maxmem = 10500
uexit = [False]

for i, item in enumerate(sys.argv[::-1]):
    if i == len(sys.argv) - 1:
        pass
    else:
        mem.append(item)

mem.append(len(sys.argv[1:]))

regs = {"prt": 0, "nad": 0, "nbd": 0, "ncd": 0, "mad": 0, "mbd": 0, "mcd": 0}
pvars = {}

def isint(value):
    try:
        int(value)
        return 1
    except:
        return 0

def isfloat(value):
    try:
        float(value)
        return 1
    except:
        return 0

def Exec(bytecode, rettype="int"):
    lvars = {}
    pos = 0
    fname = ""
    while pos < len(bytecode):
        op = bytecode[pos]
        pos += 1

        if op == vm.OP_PUSH:
            nlen = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + nlen].decode("utf-8")
            pos += nlen
            if len(fname):
                funcs[fname][1].append(vm.OP_PUSH)
                funcs[fname][1].append(nlen)
                funcs[fname][1].extend(name.encode("utf-8"))
            else:
                if isint(name):
                    mem.append(int(name))
                elif isfloat(name):
                    mem.append(float(name))
                elif name in regs.keys():
                    mem.append(regs[name])
                elif name in lvars.keys():
                    mem.append(lvars[name][1])
                elif name in pvars.keys():
                    mem.append(pvars[name][1])
                elif name.startswith("\"") and name.endswith("\""):
                    mem.append(name.replace("\"", "").replace("\\'", '"').replace("\\n", "\n").replace("\\t", "\t"))
                elif name.startswith("'") and name.endswith("'"):
                    mem.append(name.replace("'", "").replace('\\"', "'").replace("\\n", "\n").replace("\\t", "\t"))
                else:
                    print("Error: unknown registeror variable name -> {}".format(name))
                    exit(1)
        elif op == vm.OP_POP:
            nlen = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + nlen].decode("utf-8")
            pos += nlen
            if len(fname):
                funcs[fname][1].append(vm.OP_POP)
                funcs[fname][1].append(nlen)
                funcs[fname][1].extend(name.encode("utf-8"))
            else:
                if name in regs.keys():
                    regs[name] = mem.pop()
                elif name in lvars.keys():
                    lvars[name][1] = mem.pop()
                elif name in pvars.keys():
                    pvars[name][1] = mem.pop()
                else:
                    print("Error: unknown register or variable name -> {}".format(name))
                    exit(1)
        elif op == vm.OP_PRINT:
            if len(fname):
                funcs[fname][1].append(vm.OP_PRINT)
            else:
                print(regs["prt"], end="")
        elif op == vm.OP_RET:
            nlen = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + nlen].decode("utf-8")
            pos += nlen
            if len(fname):
                funcs[fname][1].append(vm.OP_RET)
                funcs[fname][1].append(nlen)
                funcs[fname][1].extend(name.encode("utf-8"))
            else:
                if rettype != "void":
                    if isint(name):
                        if rettype == "int":
                            mem.append(int(name))
                        else:
                            print("\nError: can't return int in type -> {}".format(rettype))
                            exit(1)
                    elif isfloat(name):
                        if rettype == "float":
                            mem.append(float(name))
                        else:
                            print("\nError: can't return float in type -> {}".format(rettype))
                            exit(1)
                    elif name in regs.keys():
                        if isinstance(regs[name], int):
                            if rettype == "int":
                                mem.append(regs[name])
                            else:
                                print("\nError: can't return int in type -> {}".format(rettype))
                                exit(1)
                        elif isinstance(regs[name], float):
                            if rettype == "float":
                                mem.append(regs[name])
                            else:
                                print("\nError: can't return float in type -> {}".format(rettype))
                                exit(1)
                        elif isinstance(regs[name], str):
                            if rettype == "string":
                                meme.append(regs[name])
                            else:
                                print("\nError: can't return string in type -> {}".format(rettype))
                                exit(1)
                    elif name in lvars.keys():
                        if isinstance(lvars[name][1], int):
                            if rettype == "int":
                                mem.append(lvars[name][1])
                            else:
                                print("\nError: can't return int in type -> {}".format(rettype))
                                exit(1)
                        elif isinstance(lvars[name][1], float):
                            if rettype == "float":
                                mem.append(lvars[name][1])
                            else:
                                print("\nError: can't return float in type -> {}".format(rettype))
                                exit(1)
                        elif isinstance(lvars[name][1], str):
                            if rettype == "string":
                                meme.append(lvars[name][1])
                            else:
                                print("\nError: can't return string in type -> {}".format(rettype))
                                exit(1)
                    elif name in pvars.keys():
                        if isinstance(pvars[name][1], int):
                            if rettype == "int":
                                mem.append(pvars[name][1])
                            else:
                                print("\nError: can't return int in type -> {}".format(rettype))
                                exit(1)
                        elif isinstance(pvars[name][1], float):
                            if rettype == "float":
                                mem.append(pvars[name][1])
                            else:
                                print("\nError: can't return float in type -> {}".format(rettype))
                                exit(1)
                        elif isinstance(pvars[name][1], str):
                            if rettype == "string":
                                meme.append(pvars[name][1])
                            else:
                                print("\nError: can't return string in type -> {}".format(rettype))
                                exit(1)
                    elif name.startswith("\"") and name.endswith("\""):
                        if rettype == "string":
                            mem.append(name.replace("\"", "").replace("\\'", '"').replace("\\n", "\n").replace("\\t", "\t"))
                        else:
                            print("\nError: can't return string in type -> {}".format(rettype))
                            exit(1)
                    elif name.startswith("'") and name.endswith("'"):
                        if rettype == "string":
                            mem.append(name.replace("'", "").replace('\\"', "'").replace("\\n", "\n").replace("\\t", "\t"))
                        else:
                            print("\nError: can't return string in type -> {}".format(rettype))
                            exit(1)
                    else:
                        print("\nError: unknown register or variable name -> {}".format(name))
                        exit(1)
                else:
                    print("Error: can't return things with void function type!")
                    exit(1)
        elif op == vm.OP_FUNC:
            nlen = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + nlen].decode("utf-8")
            pos += nlen
            typ = bytecode[pos]
            pos += 1
            fname = name
            funcs[fname] = [vm.functypes[typ], bytearray()]
        elif op == vm.OP_ADD:
            nlen1 = bytecode[pos]
            pos += 1
            name1 = bytecode[pos:pos + nlen1].decode("utf-8")
            pos += nlen1
            nlen2 = bytecode[pos]
            pos += 1
            name2 = bytecode[pos:pos + nlen2].decode("utf-8")
            pos += nlen2
            if len(fname):
                funcs[fname][1].append(vm.OP_ADD)
                funcs[fname][1].append(nlen1)
                funcs[fname][1].extend(name1.encode("utf-8"))
                funcs[fname][1].append(nlen2)
                funcs[fname][1].extend(name2.encode("utf-8"))
            else:
                if name2 in regs.keys():
                    name2 = regs[name2]
                elif name2 in lvars.keys():
                    name2 = lvars[name2][1]
                elif name2 in pvars.keys():
                    name2 = pvars[name2][1]
                else:
                    print("Error: unknown register or variable name -> {}".format(name1))
                    exit(1)

                if name1 in regs.keys():
                    regs[name1] += name2
                elif name1 in lvars.keys():
                    lvars[name1] += name2
                elif name1 in pvars.keys():
                    pvars[name1] += name2
                else:
                    print("Error: unknown register or variable name -> {}".format(name1))
                    exit(1)
        elif op == vm.OP_CALL:
            nlen = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + nlen].decode("utf-8")
            pos += nlen
            if len(fname):
                funcs[fname][1].append(vm.OP_CALL)
                funcs[fname][1].append(nlen)
                funcs[fname][1].extend(name.encode("utf-8"))
            else:
                if name in funcs.keys():
                    Exec(funcs[name][1], funcs[name][0])
                else:
                    print("Error: unknown function -> {}".format(name))
                    exit(1)
        elif op == vm.OP_INTVAR:
            nlen1 = bytecode[pos]
            pos += 1
            name1 = bytecode[pos:pos + nlen1].decode("utf-8")
            pos += nlen1
            nlen2 = bytecode[pos]
            pos += 1
            name2 = bytecode[pos:pos + nlen2].decode("utf-8")
            pos += nlen2
            if len(fname):
                funcs[fname][1].append(vm.OP_INTVAR)
                funcs[fname][1].append(nlen1)
                funcs[fname][1].extend(name1.encode("utf-8"))
                funcs[fname][1].append(nlen2)
                funcs[fname][1].extend(name2.encode("utf-8"))
            else:
                if name2 in regs.keys():
                    name2 = regs[name2]
                elif name2 in lvars.keys():
                    name2 = lvars[name2][1]
                elif name2 in pvars.keys():
                    name2 = pvars[name2][1]
                else:
                    print("Error: unknown register or variable name -> {}".format(name2))
                    exit(1)
                
                lvars[name1] = ["int", name2]
        elif op == vm.OP_FLOATVAR:
            nlen1 = bytecode[pos]
            pos += 1
            name1 = bytecode[pos:pos + nlen1].decode("utf-8")
            pos += nlen1
            nlen2 = bytecode[pos]
            pos += 1
            name2 = bytecode[pos:pos + nlen2].decode("utf-8")
            pos += nlen2
            if len(fname):
                funcs[fname][1].append(vm.OP_FLOATVAR)
                funcs[fname][1].append(nlen1)
                funcs[fname][1].extend(name1.encode("utf-8"))
                funcs[fname][1].append(nlen2)
                funcs[fname][1].extend(name2.encode("utf-8"))
            else:
                if name2 in regs.keys():
                    name2 = regs[name2]
                elif name2 in lvars.keys():
                    name2 = lvars[name2][1]
                elif name2 in pvars.keys():
                    name2 = pvars[name2][1]
                else:
                    print("Error: unknown register or variable name -> {}".format(name1))
                    exit(1)
                    
                lvars[name1] = ["float", name2]
        elif op == vm.OP_STRVAR:
            nlen1 = bytecode[pos]
            pos += 1
            name1 = bytecode[pos:pos + nlen1].decode("utf-8")
            pos += nlen1
            nlen2 = bytecode[pos]
            pos += 1
            name2 = bytecode[pos:pos + nlen2].decode("utf-8")
            pos += nlen2
            if len(fname):
                funcs[fname][1].append(vm.OP_STRVAR)
                funcs[fname][1].append(nlen1)
                funcs[fname][1].extend(name1.encode("utf-8"))
                funcs[fname][1].append(nlen2)
                funcs[fname][1].extend(name2.encode("utf-8"))
            else:
                if name2 in regs.keys():
                    name2 = regs[name2]
                elif name2 in lvars.keys():
                    name2 = lvars[name2][1]
                elif name2 in pvars.keys():
                    name2 = pvars[name2][1]
                else:
                    print("Error: unknown register or variable name -> {}".format(name1))
                    exit(1)
                    
                lvars[name1] = ["string", name2]
        elif op == vm.OP_EXIT:
            if len(fname):
                funcs[fname][1].append(vm.OP_EXIT)
            else:
                uexit[0] = True
                exit(regs["mcd"])

        for name, value in lvars.items():
            if value[0] == "int":
                if isinstance(value[1], int):
                    pass
                else:
                    print("Error: use int values to int variables!")
                    exit(1)
            elif value[0] == "float":
                if isinstance(value[1], float):
                    pass
                else:
                    print("Error: use float values to float variables!")
                    exit(1)
            elif value[0] == "string":
                if isinstance(value[1], str):
                    pass
                else:
                    print("Error: use string to string variables!")
                    exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.hf>")
        sys.exit(1)
    else:
        if sys.argv[1].endswith(".hf"):
            with open(sys.argv[1], "rb") as inp:
                Exec(inp.read())

            Exec(funcs["main"][1], funcs["main"][0])
            if not uexit[0]:
                print("Segmentation fault")
                print("use exit in your code!")
                for i in range(0, 5):
                    print("NOW!!!")
                exit(255)
        else:
            print("Error: use '.hf' file extension")
            sys.exit(1)
