from flask import Flask, render_template, request, redirect
from waitress import serve
import controllers as ctl
import createfiles as crtf

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
    path = request.form['rootdir']
    ctl.setroot(path)
    return redirect('/')


@app.route('/setsettings', methods=['POST'])
def setsettings():
    xmlTemplate = request.form.get('XMLtemplate') or None
    xmlVariables = request.form.get('XMLvariables') or None
    wordTemplate = request.form.get('Wordtemplate') or None
    wordVariables = request.form.get('Wordvariables') or None
    subdir = request.form.get('subdir') or None
    localizations = request.form.getlist('localizations[]')
    ctl.setsettings(subdir, xmlTemplate, xmlVariables,
                    wordTemplate, wordVariables, localizations)
    return redirect('/')


@app.route('/createfiles', methods=['POST'])
def createfiles():
    subdir = request.headers.get('subdir')
    crtf.createfiles(subdir)
    return redirect('/')


if __name__ == "__main__":
    serve(app, host="localhost", port="9400")
