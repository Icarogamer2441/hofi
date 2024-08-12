OP_PUSH = 1
OP_POP = 2
OP_PRINT = 3
OP_FUNC = 4
OP_RET = 5
OP_ADD = 6
OP_CALL = 7
OP_INTVAR = 8
OP_FLOATVAR = 9
OP_STRVAR = 10
OP_EXIT = 11
OP_FUNCEND = 12
OP_SUB = 13
OP_MUL = 14
OP_DIV = 15

functypes = {1: "int", 2: "float", 3: "string", 4: "void"}

class Vm:
    def __init__(self):
        self.bytecode = bytearray()

    def push(self, value):
        self.bytecode.append(OP_PUSH)
        self.bytecode.append(len(str(value)))
        self.bytecode.extend(str(value).encode("utf-8"))

    def pop(self, rvname):
        self.bytecode.append(OP_POP)
        self.bytecode.append(len(str(rvname)))
        self.bytecode.extend(str(rvname).encode("utf-8"))

    def prt(self):
        self.bytecode.append(OP_PRINT)

    def func(self, name, rettype):
        self.bytecode.append(OP_FUNC)
        self.bytecode.append(len(str(name)))
        self.bytecode.extend(str(name).encode("utf-8"))
        if rettype in functypes.keys():
            self.bytecode.append(rettype)
            print(f"Created function -> '{name}', with type -> '{functypes[rettype]}'")
        else:
            print(f"Error: unknown type -> '{rettype}'. types -> {functypes}")

    def ret(self, value):
        self.bytecode.append(OP_RET)
        self.bytecode.append(len(str(value)))
        self.bytecode.extend(str(value).encode("utf-8"))

    def add(self, rv1, rv2):
        self.bytecode.append(OP_ADD)
        self.bytecode.append(len(str(rv1)))
        self.bytecode.extend(str(rv1).encode("utf-8"))
        self.bytecode.append(len(str(rv2)))
        self.bytecode.extend(str(rv2).encode("utf-8"))

    def call(self, fname):
        self.bytecode.append(OP_CALL)
        self.bytecode.append(len(str(fname)))
        self.bytecode.extend(str(fname).encode("utf-8"))

    def ivar(self, name, value):
        self.bytecode.append(OP_INTVAR)
        self.bytecode.append(len(str(name)))
        self.bytecode.extend(str(name).encode("utf-8"))
        self.bytecode.append(len(str(value)))
        self.bytecode.extend(str(value).encode("utf-8"))

    def fvar(self, name, value):
        self.bytecode.append(OP_FLOATVAR)
        self.bytecode.append(len(str(name)))
        self.bytecode.extend(str(name).encode("utf-8"))
        self.bytecode.append(len(str(value)))
        self.bytecode.extend(str(value).encode("utf-8"))

    def svar(self, name, value):
        self.bytecode.append(OP_STRVAR)
        self.bytecode.append(len(str(name)))
        self.bytecode.extend(str(name).encode("utf-8"))
        self.bytecode.append(len(str(value)))
        self.bytecode.extend(str(value).encode("utf-8"))

    def exitt(self):
        self.bytecode.append(OP_EXIT)

    def funcend(self):
        self.bytecode.append(OP_FUNCEND)

    def sub(self, rv1, rv2):
        self.bytecode.append(OP_SUB)
        self.bytecode.append(len(str(rv1)))
        self.bytecode.extend(str(rv1).encode("utf-8"))
        self.bytecode.append(len(str(rv2)))
        self.bytecode.extend(str(rv2).encode("utf-8"))

    def mul(self, rv1, rv2):
        self.bytecode.append(OP_MUL)
        self.bytecode.append(len(str(rv1)))
        self.bytecode.extend(str(rv1).encode("utf-8"))
        self.bytecode.append(len(str(rv2)))
        self.bytecode.extend(str(rv2).encode("utf-8"))

    def div(self, rv1, rv2):
        self.bytecode.append(OP_DIV)
        self.bytecode.append(len(str(rv1)))
        self.bytecode.extend(str(rv1).encode("utf-8"))
        self.bytecode.append(len(str(rv2)))
        self.bytecode.extend(str(rv2).encode("utf-8"))

    def comp(self, outname):
        with open(outname, "wb") as out:
            out.write(self.bytecode)
