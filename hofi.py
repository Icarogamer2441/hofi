import hofivm as vm
import sys

out = vm.Vm()

funcs = ["exit"]

out.func("exit", 4)
out.pop("mcd")
out.exitt()
out.funcend()

t_int = "INTEGER"
t_string = "STRING"
t_float = "FLOATING"
t_plus = "PLUS"
t_minus = "MINUS"
t_times = "TIMES"
t_div = "DIVIDE"
t_id = "IDENTIFIER"
t_lparen = "LPAREN"
t_rparen = "RPAREN"
t_lbkt = "LBRACKET"
t_rbkt = "RBRACKET"
t_colon = "COLON"
t_semicolon = "SEMICOLON"
t_set = "SET"
t_dctset = "DICTSET"
t_equal = "EQUAL"
t_not = "NOT"
t_nequal = "NOTEQUAL"
t_comma = "COMMA"

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def tokenize(code):
    tokens = []
    pos = 0
    fnl = ""

    while pos < len(code):
        token = code[pos]
        pos += 1

        if token.isdigit():
            while (token.isdigit() or token == ".") and pos <= len(code):
                fnl += token

                if pos < len(code):
                    token = code[pos]
                pos += 1
            if fnl.isdigit():
                tokens.append((t_int, int(fnl)))
            elif is_float(fnl):
                tokens.append((t_float, float(fnl)))
            else:
                print(f"Error: Unknown type -> '{fnl}'")
            fnl = ""
            pos -= 1
        elif token == "+":
            tokens.append((t_plus, token))
        elif token == "-":
            if pos < len(code):
                token = code[pos]
                pos += 1
                if token == ">":
                    tokens.append((t_dctset, "->"))
                else:
                    tokens.append((t_minus, "-"))
                    pos -= 1
            else:
                tokens.append((t_minus, token))
        elif token == "\"":
            fnl += token
            token = code[pos]
            pos += 1
            while token != "\"" and pos <= len(code):
                fnl += token

                if pos < len(code):
                    token = code[pos]
                else:
                    print("Error: unclosed string!")
                    exit(1)
                pos += 1
            fnl += token
            tokens.append((t_string, fnl))
            fnl = ""
        elif token == "'":
            fnl += token
            token = code[pos]
            pos += 1
            while token != "'" and pos <= len(code):
                fnl += token

                if pos < len(code):
                    token = code[pos]
                else:
                    print("Error: unclosed string!")
                    exit(1)
                pos += 1
            fnl += token
            tokens.append((t_string, fnl))
            fnl = ""
        elif token == " " or token == "\t" or token == "\n":
            continue
        elif token == "(":
            tokens.append((t_lparen, token))
        elif token == ")":
            tokens.append((t_rparen, token))
        elif token == "{":
            tokens.append((t_lbkt, token))
        elif token == "}":
            tokens.append((t_rbkt, token))
        elif token == ":":
            tokens.append((t_colon, token))
        elif token == ";":
            tokens.append((t_semicolon, token))
        elif token == "=":
            if pos < len(code):
                token = code[pos]
                pos += 1
                if token == "=":
                    tokens.append((t_equal, "=="))
                else:
                    tokens.append((t_set, "="))
                    pos -= 1
            else:
                tokens.append((t_set, token))
        elif token == "*":
            tokens.append((t_times, token))
        elif token == "/":
            tokens.append((t_div, token))
        elif token == "!":
            if pos < len(code):
                token = code[pos]
                pos += 1
                if token == "=":
                    tokens.append((t_nequal, "!="))
                else:
                    tokens.append((t_not, "!"))
                    pos -= 1
            else:
                tokens.append((t_not, token))
        elif token == ",":
            tokens.append((t_comma, token))
        else:
            while token != "\"" and token != "+" and token != "-" and pos <= len(code) and token != " " and token != "\t" and token != "\n" and token != "(" and token != ")" and token != "{" and token != "}" and token != ":" and token != ";" and token != "=" and token != "/" and token != "*" and token != "!" and token != ",":
                fnl += token

                if pos < len(code):
                    token = code[pos]
                pos += 1
            tokens.append((t_id, fnl))
            pos -= 1
            fnl = ""
    return tokens

def comp3(code, lvarss=[]):
    lvars = lvarss
    tokens = tokenize(code)
    pos = 0
    while pos < len(tokens):
        token = tokens[pos]
        pos += 1
        if token[0] == t_int or token[0] == t_float or token[0] == t_string or (token[0] == t_id and token[1] in lvars):
            out.push(str(token[1]))
        elif token[0] == t_plus:
            token = tokens[pos]
            pos += 1
            if token[0] == t_id and token[1] in funcs:
                fname = token[1]
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    argnum = 1
                    while pos < len(tokens) and argnum > 0:
                        if token[0] == t_lparen:
                            argnum += 1
                            final.append(token[1])
                        elif token[0] == t_rparen:
                            argnum -= 1
                            if argnum > 0:
                                final.append(token[1])
                            else:
                                break
                        elif token[0] == t_comma:
                            if argnum == 1:
                                comp3(" ".join(final), lvars)
                                final = []
                            else:
                                final.append(token[1])
                        else:
                            final.append(str(token[1]))
                        token = tokens[pos]
                        pos += 1
                    if len(final):
                        comp3(" ".join(final), lvars)
                        final = []
                    out.call(fname)
                else:
                    print("Error: use '(' to start function arguments!")
                    exit(1)
            else:
                out.push(str(token[1]))
            out.pop("mbd")
            out.pop("mad")
            out.add("mad", "mbd")
            out.push("mad")
        elif token[0] == t_id and token[1] in funcs:
            fname = token[1]
            token = tokens[pos]
            pos += 1
            if token[0] == t_lparen:
                token = tokens[pos]
                pos += 1
                final = []
                argnum = 1
                while pos < len(tokens) and argnum > 0:
                    if token[0] == t_lparen:
                        argnum += 1
                        final.append(token[1])
                    elif token[0] == t_rparen:
                        argnum -= 1
                        if argnum > 0:
                            final.append(token[1])
                        else:
                            break
                    elif token[0] == t_comma:
                        if argnum == 1:
                            comp3(" ".join(final), lvars)
                            final = []
                        else:
                            final.append(token[1])
                    else:
                        final.append(str(token[1]))
                    token = tokens[pos]
                    pos += 1
                if len(final):
                    comp3(" ".join(final), lvars)
                    final = []
                out.call(fname)
            else:
                print("Error: use '(' to start functions arguments!")
                exit(1)
        elif token[0] == t_minus:
            token = tokens[pos]
            pos += 1
            if token[0] == t_id and token[1] in funcs:
                fname = token[1]
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    argnum = 1
                    while pos < len(tokens) and argnum > 0:
                        if token[0] == t_lparen:
                            argnum += 1
                            final.append(token[1])
                        elif token[0] == t_rparen:
                            argnum -= 1
                            if argnum > 0:
                                final.append(token[1])
                            else:
                                break
                        elif token[0] == t_comma:
                            if argnum == 1:
                                comp3(" ".join(final), lvars)
                                final = []
                            else:
                                final.append(token[1])
                        else:
                            final.append(str(token[1]))
                        token = tokens[pos]
                        pos += 1
                    if len(final):
                        comp3(" ".join(final), lvars)
                        final = []
                    out.call(fname)
                else:
                    print("Error: use '(' to start function arguments!")
                    exit(1)
            else:
                out.push(str(token[1]))
            out.pop("mbd")
            out.pop("mad")
            out.sub("mad", "mbd")
            out.push("mad")
        elif token[0] == t_times:
            token = tokens[pos]
            pos += 1
            if token[0] == t_id and token[1] in funcs:
                fname = token[1]
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    argnum = 1
                    while pos < len(tokens) and argnum > 0:
                        if token[0] == t_lparen:
                            argnum += 1
                            final.append(token[1])
                        elif token[0] == t_rparen:
                            argnum -= 1
                            if argnum > 0:
                                final.append(token[1])
                            else:
                                break
                        elif token[0] == t_comma:
                            if argnum == 1:
                                comp3(" ".join(final), lvars)
                                final = []
                            else:
                                final.append(token[1])
                        else:
                            final.append(str(token[1]))
                        token = tokens[pos]
                        pos += 1
                    if len(final):
                        comp3(" ".join(final), lvars)
                        final = []
                    out.call(fname)
                else:
                    print("Error: use '(' to start function arguments!")
                    exit(1)
            else:
                out.push(str(token[1]))
            out.pop("mbd")
            out.pop("mad")
            out.mul("mad", "mbd")
            out.push("mad")
        elif token[0] == t_div:
            token = tokens[pos]
            pos += 1
            if token[0] == t_id and token[1] in funcs:
                fname = token[1]
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    argnum = 1
                    while pos < len(tokens) and argnum > 0:
                        if token[0] == t_lparen:
                            argnum += 1
                            final.append(token[1])
                        elif token[0] == t_rparen:
                            argnum -= 1
                            if argnum > 0:
                                final.append(token[1])
                            else:
                                break
                        elif token[0] == t_comma:
                            if argnum == 1:
                                comp3(" ".join(final), lvars)
                                final = []
                            else:
                                final.append(token[1])
                        else:
                            final.append(str(token[1]))
                        token = tokens[pos]
                        pos += 1
                    if len(final):
                        comp3(" ".join(final), lvars)
                        final = []
                    out.call(fname)
                else:
                    print("Error: use '(' to start function arguments!")
                    exit(1)
            else:
                out.push(str(token[1]))
            out.pop("mbd")
            out.pop("mad")
            out.div("mad", "mbd")
            out.push("mad")

def comp2(code, lvarss=[]):
    lvars = lvarss
    tokens = tokenize(code)
    pos = 0
    while pos < len(tokens):
        token = tokens[pos]
        pos += 1

        if token[0] == t_id:
            if token[1] == "show":
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    argnum = 1
                    while pos < len(tokens) and argnum > 0:
                        if token[0] == t_lparen:
                            argnum += 1
                            final.append(token[1])
                        elif token[0] == t_rparen:
                            argnum -= 1
                            if argnum > 0:
                                final.append(token[1])
                            else:
                                break
                        elif token[0] == t_comma:
                            if argnum == 1:
                                comp3(" ".join(final), lvars)
                                final = []
                                out.pop("prt")
                                out.prt()
                            else:
                                final.append(token[1])
                        else:
                            final.append(str(token[1]))
                        
                        token = tokens[pos]
                        pos += 1
                    if len(final):
                        comp3(" ".join(final), lvars)
                        final = []
                        out.pop("prt")
                        out.prt()
                    token = tokens[pos]
                    pos += 1
                    if token[0] == t_semicolon:
                        pass
                    else:
                        print("Error: use semicolon on the end of 'show()'!")
                        exit(1)
            elif token[1] == "return":
                token = tokens[pos]
                pos += 1
                final = []
                while token[0] != t_semicolon and pos < len(tokens):
                    final.append(str(token[1]))

                    token = tokens[pos]
                    pos += 1
                comp3(" ".join(final), lvars)
                final = []
                out.pop("mad")
                out.ret("mad")
            elif token[1] == "int":
                token = tokens[pos]
                pos += 1
                vname = ""
                if token[0] == t_id:
                    vname = token[1]
                else:
                    print("Error: use normal words to set variables values!")
                    exit(1)
                token = tokens[pos]
                pos += 1
                if token[0] == t_set:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    while token[0] != t_semicolon and pos < len(tokens):
                        final.append(str(token[1]))
                        
                        token = tokens[pos]
                        pos += 1
                    comp3(" ".join(final), lvars)
                    final = []
                    out.pop("mad")
                    out.ivar(vname, "mad")
                    lvars.append(vname)
                else:
                    print("Error: use '=' to set variables values!")
                    exit(1)
            elif token[1] == "float":
                token = tokens[pos]
                pos += 1
                vname = ""
                if token[0] == t_id:
                    vname = token[1]
                else:
                    print("Error: use normal words to set variables values!")
                    exit(1)
                token = tokens[pos]
                pos += 1
                if token[0] == t_set:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    while token[0] != t_semicolon and pos < len(tokens):
                        final.append(str(token[1]))
                        
                        token = tokens[pos]
                        pos += 1
                    comp3(" ".join(final), lvars)
                    final = []
                    out.pop("mad")
                    out.fvar(vname, "mad")
                    lvars.append(vname)
                else:
                    print("Error: use '=' to set variables values!")
                    exit(1)
            elif token[1] == "string":
                token = tokens[pos]
                pos += 1
                vname = ""
                if token[0] == t_id:
                    vname = token[1]
                else:
                    print("Error: use normal words to set variables values!")
                    exit(1)
                token = tokens[pos]
                pos += 1
                if token[0] == t_set:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    while token[0] != t_semicolon and pos < len(tokens):
                        final.append(str(token[1]))
                        
                        token = tokens[pos]
                        pos += 1
                    comp3(" ".join(final), lvars)
                    final = []
                    out.pop("mad")
                    out.svar(vname, "mad")
                    lvars.append(vname)
                else:
                    print("Error: use '=' to set variables values!")
                    exit(1)
            elif token[1] in funcs:
                fname = token[1]
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    final = []
                    argnum = 1
                    while pos < len(tokens) and argnum > 0:
                        if token[0] == t_lparen:
                            argnum += 1
                            final.append(token[1])
                        elif token[0] == t_rparen:
                            argnum -= 1
                            if argnum > 0:
                                final.append(token[1])
                            else:
                                break
                        elif token[0] == t_comma:
                            if argnum == 1:
                                comp3(" ".join(final), lvars)
                                final = []
                            else:
                                final.append(token[1])
                        else:
                            final.append(str(token[1]))
                        token = tokens[pos]
                        pos += 1
                    if len(final):
                        comp3(" ".join(final), lvars)
                        final = []
                    token = tokens[pos]
                    pos += 1
                    if token[0] == t_semicolon:
                        out.call(fname)
                    else:
                        print("Error: use semicolon to end function call")
                        exit(1)
                else:
                    print("Error: use '(' to start functions arguments!")
                    exit(1)

def comp1(code):
    tokens = tokenize(code)
    pos = 0
    while pos < len(tokens):
        token = tokens[pos]
        pos += 1

        if token[0] == t_id:
            if token[1] == "int":
                token = tokens[pos]
                pos += 1
                fname = ""
                if token[0] == t_id:
                    fname = token[1]
                else:
                    print("Error: use normal words to set functions names and not -> {}".format(token))
                    exit(1)
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    out.func(fname, 1)
                    lvars = []
                    while pos < len(tokens) and token[0] != t_rparen:
                        if token[1] == "int":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.ivar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.ivar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "float":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.fvar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.fvar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "string":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.svar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.svar(aname, "mad")
                            lvars.append(aname)
                        else:
                            print("Error: unknown param type -> {}".format(token[1]))
                            exit(1)
                        token = tokens[pos]
                        pos += 1
                    token = tokens[pos]
                    pos += 1
                    if token[0] == t_lbkt:
                        endnum = 1
                        token = tokens[pos]
                        pos += 1
                        finalcode = []
                        while pos < len(tokens) and endnum > 0:
                            if token[0] == t_lbkt:
                                endnum += 1
                                finalcode.append(token[1])
                            elif token[0] == t_rbkt:
                                endnum -= 1
                                if endnum > 0:
                                    finalcode.append(token[1])
                                else:
                                    break
                            else:
                                finalcode.append(str(token[1]))
                            token = tokens[pos]
                            pos += 1
                        funcs.append(fname)
                        comp2(" ".join(finalcode), lvars)
            elif token[1] == "float":
                token = tokens[pos]
                pos += 1
                fname = ""
                if token[0] == t_id:
                    fname = token[1]
                else:
                    print("Error: use normal words to set functions names and not -> {}".format(token))
                    exit(1)
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    out.func(fname, 2)
                    lvars = []
                    while pos < len(tokens) and token[0] != t_rparen:
                        if token[1] == "int":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.ivar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.ivar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "float":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.fvar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.fvar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "string":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.svar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.svar(aname, "mad")
                            lvars.append(aname)
                        else:
                            print("Error: unknown param type -> {}".format(token[1]))
                            exit(1)
                        token = tokens[pos]
                        pos += 1
                    token = tokens[pos]
                    pos += 1
                    if token[0] == t_lbkt:
                        endnum = 1
                        token = tokens[pos]
                        pos += 1
                        finalcode = []
                        while pos < len(tokens) and endnum > 0:
                            if token[0] == t_lbkt:
                                endnum += 1
                                finalcode.append(token[1])
                            elif token[0] == t_rbkt:
                                endnum -= 1
                                if endnum > 0:
                                    finalcode.append(token[1])
                                else:
                                    break
                            else:
                                finalcode.append(str(token[1]))
                            token = tokens[pos]
                            pos += 1
                        funcs.append(fname)
                        comp2(" ".join(finalcode), lvars)
            elif token[1] == "string":
                token = tokens[pos]
                pos += 1
                fname = ""
                if token[0] == t_id:
                    fname = token[1]
                else:
                    print("Error: use normal words to set functions names and not -> {}".format(token))
                    exit(1)
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    out.func(fname, 3)
                    lvars = []
                    while pos < len(tokens) and token[0] != t_rparen:
                        if token[1] == "int":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.ivar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.ivar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "float":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.fvar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.fvar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "string":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.svar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.svar(aname, "mad")
                            lvars.append(aname)
                        else:
                            print("Error: unknown param type -> {}".format(token[1]))
                            exit(1)
                        token = tokens[pos]
                        pos += 1
                    token = tokens[pos]
                    pos += 1
                    if token[0] == t_lbkt:
                        endnum = 1
                        token = tokens[pos]
                        pos += 1
                        finalcode = []
                        while pos < len(tokens) and endnum > 0:
                            if token[0] == t_lbkt:
                                endnum += 1
                                finalcode.append(token[1])
                            elif token[0] == t_rbkt:
                                endnum -= 1
                                if endnum > 0:
                                    finalcode.append(token[1])
                                else:
                                    break
                            else:
                                finalcode.append(str(token[1]))
                            token = tokens[pos]
                            pos += 1
                        funcs.append(fname)
                        comp2(" ".join(finalcode), lvars)
            elif token[1] == "void":
                token = tokens[pos]
                pos += 1
                fname = ""
                if token[0] == t_id:
                    fname = token[1]
                else:
                    print("Error: use normal words to set functions names and not -> {}".format(token))
                    exit(1)
                token = tokens[pos]
                pos += 1
                if token[0] == t_lparen:
                    token = tokens[pos]
                    pos += 1
                    out.func(fname, 4)
                    lvars = []
                    while pos < len(tokens) and token[0] != t_rparen:
                        if token[1] == "int":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.ivar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.ivar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "float":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.fvar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.fvar(aname, "mad")
                            lvars.append(aname)
                        elif token[1] == "string":
                            token = tokens[pos]
                            pos += 1
                            aname = ""
                            if token[0] == t_id:
                                aname = token[1]
                            else:
                                print("Error: use normal words to set functions arguments names! used -> {}".format(token))
                                exit(1)
                            token = tokens[pos]
                            pos += 1
                            if token[0] == t_comma:
                                pass
                            elif token[0] == t_rparen:
                                out.pop("mad")
                                out.svar(aname, "mad")
                                lvars.append(aname)
                                break
                            else:
                                print("Error: use commas to separate every function argument")
                                exit(1)
                            out.pop("mad")
                            out.svar(aname, "mad")
                            lvars.append(aname)
                        else:
                            print("Error: unknown param type -> {}".format(token[1]))
                            exit(1)
                        token = tokens[pos]
                        pos += 1
                    token = tokens[pos]
                    pos += 1
                    if token[0] == t_lbkt:
                        endnum = 1
                        token = tokens[pos]
                        pos += 1
                        finalcode = []
                        while pos < len(tokens) and endnum > 0:
                            if token[0] == t_lbkt:
                                endnum += 1
                                finalcode.append(token[1])
                            elif token[0] == t_rbkt:
                                endnum -= 1
                                if endnum > 0:
                                    finalcode.append(token[1])
                                else:
                                    break
                            else:
                                finalcode.append(str(token[1]))
                            token = tokens[pos]
                            pos += 1
                        funcs.append(fname)
                        comp2(" ".join(finalcode), lvars)
                        out.funcend()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} -o <file.hof> <out>")
        exit(1)
    else:
        if sys.argv[1] == "-o":
            if sys.argv[2].endswith(".hof"):
                with open(sys.argv[2], "r") as inp:
                    code = inp.read()

                comp1(code)
                out.comp(sys.argv[3] + ".hf")
            else:
                print(f"Error: use '.hof' file extension here -> {sys.argv[2]}")
                exit(1)
        else:
            print(f"Error: use '-o' here -> {sys.argv[1]}")
            exit(1)
