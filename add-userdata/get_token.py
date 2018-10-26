
file = open(“ansible-playbook-output.txt”, “r”)
file_lines = file.readlines():
tokenStr = "token.stdout_lines"
for x in range(len(file_lines)):
    if tokenStr in file_lines[x]:
        print file_lines[x+1]
        break
