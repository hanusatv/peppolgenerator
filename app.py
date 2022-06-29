from flask import Flask, render_template, request, redirect
from waitress import serve
import controllers as ctl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CasaDelPiss'
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/', methods=['GET'])
def index():
    rootdir = ctl.getroot()
    dirs = ctl.getdir()
    return render_template('index.html', dirs=dirs, rootdir=rootdir)


@app.route('/setroot', methods=['POST'])
def setroot():
    path = request.headers.get('rootdir')
    ctl.setroot(path)
    return redirect('/')


@app.route('/setsettings', methods=['POST'])
def setsettings():
    xmlTemplate = request.form.get('XMLtemplate') or None
    xmlVariables = request.form.get('XMLvariables') or None
    wordTemplate = request.form.get('Wordtemplate') or None
    wordVariables = request.form.get('Wordvariables') or None
    subdir = request.form.get('subdir') or None
    ctl.setsettings(subdir, xmlTemplate, xmlVariables,
                    wordTemplate, wordVariables)
    return redirect('/')


if __name__ == "__main__":
    serve(app, host="localhost", port="9400")
