import sets
import sys
import re

def loadmap(mapfilename):
    address_dict = {}
    di = {}
    f = open(mapfilename, "r");
    content = f.readlines()
    started = False
    for line in content:
        if len(line) < 4:
            continue
        line = line.strip()
        temp = line[0:255].partition(' ')[0]
        if temp=="UNUSED":
            continue
        if temp==".text":
            started = True;
            continue
        if temp==".init":
            started = True
            continue
        if temp=="Starting":
            continue
        if temp=="extab":
            continue
        if temp==".ctors":
            break #uh?
        if temp==".dtors":
            break
        if temp==".rodata":
            continue
        if temp==".data":
            continue
        if temp==".sbss":
            continue
        if temp==".sdata":
            continue
        if temp==".sdata2":
            continue
        if temp=="address":
            continue
        if temp=="-----------------------":
            continue
        if temp==".sbss2":
            break
        if temp[1] == ']':
            continue
        if (not started):
            continue
        
        address = vaddress = size = unknown = None
        m = re.match(r"(?P<address>[0-9a-f]{8}) (?P<size>[0-9a-f]{8}) (?P<vaddress>[0-9a-f]{8}) {1,2}(?P<unknown>[0-8]*) (?P<name>.*)", line)

        if m:
            name = m.group("name").split()[0]
            obj = m.group("name").split()[-1]
            if ((name != ".text" and name != ".init") and len(name) > 3):
                address_dict[m.group("vaddress")] = {"address" : m.group("address"), "size": m.group("size"), 
                                                     "vaddress" : m.group("vaddress"), "name" : name, "obj" : obj}
                try:
                    di[obj]
                except Exception as e:
                    di[obj] = []
                di[obj].append(name)
    
    return address_dict, di

def print_di(di):
    for k in di:
        print k
        for f in di[k]:
            print "\t%s" % f

def print_ad(ad):
    for k in ad:
        print ad[k]
			
ad, di = loadmap("main.map")

for k in ad:
    MakeNameEx(LocByName(GetFunctionName(int("0x%s"%k,16))), ad[k]["name"], SN_PUBLIC)
    print GetFunctionName(int("0x%s"%k,16)), k, ad[k]["name"]
    