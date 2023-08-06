def make(file):
        with open(file,"r") as headers_file:
            for line in headers_file.readlines():
                split1 = line.split("\n")[0]
                split2 = split1.split(": ")
                key = split2[0]
                value = split2[1]
                result = "'" + key + "'" + ":" + "'" + value + "'" + ","
                return result

def write(word):
    print(word,end="")

def writeline(word):
    print(word,end="\n")

def coder():    
    return {'telegram':'@Plugin','name':'Yazan Alqasem'}