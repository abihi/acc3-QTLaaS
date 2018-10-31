from flask import Flask, redirect, url_for, request, render_template
import subprocess
#from dir import file

app = Flask(__name__)


@app.route('/')
def setup():
    return render_template('index.html',title='Setup')


@app.route('/setupdone',  methods=['GET','POST'])
def setup_done():
    return render_template('setupdone.html', title='Add or Remove')

@app.route('/startcluster')
def initial_setup():
    subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/start-cluster.sh")
    return render_template('setupdone.html', title='Add or Remove')

@app.route('/addworker')
def add_worker():
    subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/add-to-cluster.sh")
    return render_template('setupdone.html', title='Add or Remove')

@app.route('/removeworker')
def delete_worker():
    subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/remove-from-cluster.sh")
    return render_template('setupdone.html', title='Add or Remove')

@app.route('/gettoken')
def get_token():
    file = open('ansible-playbook-output.txt', 'r')
    file_lines = file.readlines()
    floatingipStr = "Added floating ip:"
    for x in range(len(file_lines)):
        if floatingipStr in file_lines[x]:
	   floatingip = file_lines[x].split(' ')[3]
           print "Spark address: " "http://"+ floatingip + ":60060"
           break
    tokenStr = "token.stdout_lines"
    for x in range(len(file_lines)):
        if tokenStr in file_lines[x]:
	   token = file_lines[x+4].split('\\')[3]
           print "Login token: " + token[1:len(token)]
           break
    return render_template('setupdone.html', title='Add or Remove')

if __name__ == '__main__':
    app.run(debug=True)
