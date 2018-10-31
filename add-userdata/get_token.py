#python ssc-instance-userdata-optimized.py 2>&1 | tee ansible-playbook-output.txt
file = open('ansible-playbook-output.txt', 'r')
file_lines = file.readlines()
tokenStr = "token.stdout_lines"
for x in range(len(file_lines)):
    if tokenStr in file_lines[x]:
        token = file_lines[x+4].split('\\')[3]
        print token[1:len(token)]
	break
floatingipStr = "Added floating ip:"
for x in range(len(file_lines)):
    if floatingipStr in file_lines[x]:
        floatingip = file_lines[x].split(' ')[4]
        print floatingip
        break
