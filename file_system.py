"""
- This is a mimic of a shell terminal
Commands include: 
                             ls == lists all directories/files in the current directory
                  cd [new path] == change directory. ex: cd ../home >> move to parent folder then go to the "home" folder
                           quit == ends execution
               mkdir [dir name] == makes a directory. ex: mkdir new_files >> makes new directory calles new_files
 mkfile [file name] "[content]" == makes a file.
               read [file name] == reads a file's content
  write [file name] "[content]" == write to file
rewrite [file name] "[content]" == replace file content with new content
"""
class Node():
    def __init__(self, path):
        # ex: root/desktop
        self.path = path
    def name(self):
        # ex: in "root/desktop" 'desktop' is the name
        return self.path.split('/')[-1]
    def parent(self):
        p  = self.path.split('/')
        if len(p) >= 2:
            return p[-2]
        else:
            return "~"
    def path_split(self):
        return self.path.split('/')
    def parent_path(self):
        par  = self.path.split('/')[0:-1]
        p = ""
        for i in par:
            p += i + '/'
        return p[0:-1]

class Dir(Node):
    def __init__(self, path):
        super().__init__(path)
    def is_dir(self):
        return True

class File(Node):
    def __init__(self, path, content):
        super().__init__(path)
        self.content = content
    def is_dir(self):
        return False

def stitch_path(p): # takes list and returns path
    res = ""
    for i in p:
        res += i + '/'
    return res[0:-1]

def quote_split(ctx):
    part = ""
    parts = []
    in_str = False
    for char in ctx:
        if in_str:
            if char != "\"":
                part += char
            else:
                part += char
                parts.append(part)
                part = ""
                in_str = False
        else:
            if char != " ":
                part += char
                if char == '"':
                    in_str = True
                elif char == ctx[-1]:
                    parts.append(part)
                    part = ""
            elif char == " ":
                parts.append(part)
                part = ""
    res = []
    for i in parts:
        if i == "":
            continue
        else: 
            res.append(i)
    return res

system = [
    Dir("root"),
    Dir("root/home"),
    Dir("root/config"),
    File("root/config/conf.toml", "no content here"),
    File("root/home/notes.txt", "hello world!"),
    File("root/home/secrets.txt", "don't tell noone!!"),
]
cur_path = "root/home"
online = True

def loop():
    global cur_path
    global online
    cmd = input(cur_path + "$ ")
    cmdl = cmd.split(' ')
    ln = len(cmdl)
    if ln == 1 and cmd == "ls":
        res = ""
        for node in system:
            if node.parent_path() == cur_path:
                res += node.name() + ' '
        print(res + "\n")
    elif ln == 2 and cmdl[0] == "cd":
        if cmdl[1][0] == "/":
            print("~ please don't start directories with '/'")
            return
        split_path = cmdl[1].split("/") # ex: ../home/files >> [ '..', 'home', 'files' ]
        new_path = cur_path
        for i in split_path:
            if i == '..':
                if cur_path == "root":
                    print("~ You're in root, you can't go any higher")
                    return
                new_path = stitch_path( new_path.split('/')[0:-1] )
            else:
                new_path += '/' + i
        for i in system:
            if new_path == i.path:
                if i.is_dir() == True:
                    cur_path = new_path
                else:
                    print("~ You can't cd into a file!")
    elif ln == 1 and cmdl[0] == "quit":
        online = False
    elif ln == 2 and cmdl[0] == "mkdir":
        new_dir = cmdl[1]
        if '.' in new_dir or ' ' in new_dir:
            print("~ directory names must not contain periods or spaces")
            return
        system.append(Dir(str( cur_path + '/' + new_dir )))
    elif ln >= 2 and cmdl[0] == "mkfile":
        file_content = ""
        if ln > 2:
            file_content = quote_split(cmd)[2]
        file_name = cmdl[1]
        system.append(File(str( cur_path + '/' + file_name ), file_content[1:-1]))
    elif ln == 2 and cmdl[0] == "read":
        for node in system:
            if node.is_dir():
                continue
            if node.path == str(cur_path + '/' + cmdl[1]):
                if node.content == "":
                    print("~ file is empty")
                else:
                    print(node.content + "\n")
                return
        else:
            print("~ couldn't find file!")
            
        

print("\nstarting...\n")
while online:
    loop()
else:
    print("~ goodbye!")