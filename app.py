# -- app.py
from flask import Flask, render_template, url_for
from flask.ext.bootstrap import Bootstrap
from db_tool import init, insert, delete, update, search, dump, load_news, get_hypenews, translate_text_to_speech

app = Flask(__name__)
bootstrap = Bootstrap(app) # 


@app.route('/')
def index():
    hype_list = get_hypenews('https://hypebeast.com/zh/footwear') 
    return render_template('index.html', hype_list = hype_list)

@app.route('/download')
def download():
    return render_template('download.html')

if __name__ == "__main__":
    app.run(debug = True)
