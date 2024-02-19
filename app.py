import logging
from flask import Flask, redirect, render_template, request, make_response

app = Flask(__name__)

logger = logging.getLogger(__name__)

@app.route('/index/')
def index():
    return render_template('main.html')

@app.route('/greeting/')
def greeting():
    context={
        'name': request.cookies.get('name'),         
        'mail': request.cookies.get('mail')
    }
    return render_template('greeting.html', **context)

@app.route('/in', methods = ['POST', 'GET'])
def submitIn():
    if request.form.get('name') != '' and request.form.get('mail') != '':
        res = make_response(redirect('/greeting'))
        res.set_cookie('name', request.form.get('name'))
        res.set_cookie('mail', request.form.get('mail'))
        return res
    else:
        return render_template('main.html')

@app.route('/out')
def submitOut():
    res = make_response(redirect('/index'))
    res.set_cookie('name', '', 0)
    res.set_cookie('mail', '', 0)
    return res

@app.errorhandler(404)
def page_not_found(e):
    logger.warning(e)
    context = {
    'title': 'Страница не найдена',
    'url': request.base_url,
    }
    return render_template('404.html', **context), 404

if __name__ == '__main__':
    app.run()