from flask import Flask, render_template
import subprocess

app = Flask(__name__)
app._static_folder = '../static'

@app.route('/')
def setup():
    return render_template('index.html', title='Setup')


@app.route('/setupdone')
def setup_done():
    return render_template('setupdone.html', title='Add or Remove')


@app.route('/startcluster', methods=['GET', 'POST'])
def initial_setup():
    subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/start-cluster.sh")
    return render_template('setupdone.html', title='Add or Remove')


@app.route('/addworker', methods=['GET', 'POST'])
def add_worker():
    subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/add-to-cluster.sh")
    return render_template('setupdone.html', title='Add or Remove')


@app.route('/removeworker', methods=['GET', 'POST'])
def delete_worker():
    subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/remove-from-cluster.sh")
    return render_template('setupdone.html', title='Add or Remove')


@app.route('/removeeverything', methods=['GET', 'POST'])
def delete_all():
    subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/remove-all.sh")
    return render_template('setupdone.html', title='Add or Remove')


@app.route('/gettoken', methods=['GET', 'POST'])
def get_token():
    file = open('ansible-playbook-output.txt', 'r')
    file_lines = file.readlines()
    floatingipStr = "Added floating ip:"
    spark_adress = ""
    token = ""

    for x in range(len(file_lines)):
        if floatingipStr in file_lines[x]:
            floatingip = file_lines[x].split(' ')[3]
            spark_adress = "http://" + floatingip + ":60060"
            break

    tokenStr = "token.stdout_lines"
    for x in range(len(file_lines)):
        if tokenStr in file_lines[x]:
            token = file_lines[x + 4].split('\\')[3]
            token = '/?token=' + token[1:len(token)]
            break

    auto_login = spark_adress + token
    print(auto_login)
    return render_template('setupdone.html', title='Add or Remove', token=token, adress=spark_adress, notebook=auto_login)


if __name__ == '__main__':
    app.run(debug=True)
