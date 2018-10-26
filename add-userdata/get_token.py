file = open('ansible-playbook-output.txt', 'r')
file_lines = file.readlines()
tokenStr = "token.stdout_lines"
for x in range(len(file_lines)):
    if tokenStr in file_lines[x]:
        token = file_lines[x+1].split('\\')[3]
        print token[1:len(token)]
	break

