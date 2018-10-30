from flask import Flask, redirect, url_for, request, render_template

#from dir import file

app = Flask(__name__)


@app.route('/')
def setup():
    return render_template('index.html',title='Setup')


@app.route('/setupdone',  methods=['GET','POST'])
def setup_done():
    return render_template('setupdone.html', title='Add or Remove')





if __name__ == '__main__':
    app.run(debug=True)
