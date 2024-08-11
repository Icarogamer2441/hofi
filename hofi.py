import hofivm as vm

test = vm.Vm()

test.func("test", 4)
test.pop("nad")
test.pop("nbd")
test.add("nad", "nbd")
test.ret("nad")

test.func("main", 1)
test.push("'1 + 1 = '")
test.pop("prt")
test.prt()
test.push("1")
test.push("1")
test.call("test")
test.pop("prt")
test.prt()
test.push('"\\n"')
test.pop("prt")
test.prt()

test.comp("out.hf")
