from flask import Flask, redirect, url_for, abort, make_response, json, jsonify, request
import click

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>hello world</h1>'

@app.route('/greet/<name>')
@app.route('/greet')
def greet(name):
    return f'<h1>Hello World {name}</h1>'

# @app.route('/hello/<name>')
# def hello(name):
#     return f'<h1>Hello flask {name}</h1>'

@app.route('/hello')
def hello():
    return f'<h1>hello redirect, set me</h1>'

# 调用 url_for('say_hello', name="programmer")

# 自定义创建命令
@app.cli.command('say-hello')
def hello():
    click.echo('hello cmd')

# 需要使用template

@app.route('/hi')
def hi():
    name = request.args.get('name', 'Flask')
    return f'<h1>Hello {name}</h1>'

@app.route('/hello', methods=['GET', 'POST'])
def say_hi():
    return '<h1>Flask GET POST</h1>'

# 类型转换器
@app.route('/goback/<int:year>')
def go_back(year):
    return f'<p>welcome to {2024 - year}</p>'

# @app.route('/colors/<any(blue, white, red):color>')
# def three_colors(color):
#     return f'<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'

colors = ['blue', 'white', 'red']
@app.route('/colors/<any(%s):color>' % str(colors)[1:-1])
def three_(color):
    return f'<h1>{color}</h1>'

# 生成状态码
@app.route('/hi2')
def hi2():
    return '<h1>hello, flask!</h1>', 201
# 重定向
@app.route('/hi3')
def hi3():
    return redirect('http://www.example.com')

# 重新定向回hello
@app.route('/redirect')
def hi4():
    return redirect(url_for('say_what'))

@app.route('/say_what')
def say_what():
    return f'<h1>say what</h1>'

# 针对异常, 手动返回错误响应
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418) # 传入参数代码
    else:
        return 'a drop of tea'
    
# abort前面不要return
@app.route('/404')
def not_found():
    abort(404)
    
@app.route('/418')
def tea():
    abort(418)

@app.route('/foo')
def foo():
    response = make_response('hello world')
    response.mimetype = 'text/plain'
    return response

@app.route('/note')
def note():
    data = {
        'name' : '1',
        'gender' : '0'
    }
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response

@app.route('/jsontify')
def jsn():
    data = {
        'name':'sun',
        'gender':'male'
    }
    return jsonify(data)

# 附加状态码
# @app.route('/500')
# def foo():
#     data = { 'name':'sum', 'gender':'male' }
#     return jsonify(data), 500

@app.route('/tet/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('last')))
    response.set_cookie('name', name)
    return response

@app.route('/me')
def me():
    return '<h1>say i am me</h1>'

@app.route('/')
@app.route('/last')
def last():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'human')
    return f'<h1>Hello, {name}</h1>'