from flask import Flask, redirect, url_for, abort, make_response, json, jsonify, request, session, g
import os
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

# @app.route('/foo')
# def foo():
#     response = make_response('hello world')
#     response.mimetype = 'text/plain'
#     return response

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

# # session的cookie安全
# # 1.session的随机密钥
# @app.route('/secret')
# def secret():
#     ## 更安全的做法是写进.env文件之中
#     app.secret_key = os.getenv('SECRET_KEY', 's3123212')
#     return redirect(url_for('login'))

# # 2.模拟用户认证
# @app.route('/login')
# def login():
#     session['logged_in'] = True ## 写入session
#     return redirect(url_for('test_login')) ## 必须保证.env文件写入了密钥

# @app.route('/test_login')
# def test_login():
#     name = request.args.get('name')
#     if name is None:
#         name = request.cookies.get('name', 'sunny')
#         response = f'<h1>hello {name}</h1>'
#         if 'logged_in' in session:
#             response += '[Authenticated]'
#         else:
#             response += '[Not Authenticated]'
#         return response

# @app.route('/admin')
# def admin():
#     if 'logged_in' not in session:
#         abort(403)
#     return 'welcome to admin page'

# # 用户登出
# @app.route('/logout')
# def logout():
#     if 'logged_in' in session:
#         session.pop('logged_in')
#     return redirect(url_for('test_login'))

# # 程序上下文
# @app.before_request
# def get_name():
#     g.name = request.args.get('name')

# '''激活上下文'''
# from app import app
# from flask import current_app
# # with 语句激活上下文
# with app.app_context():
#     current_app.name

# # 显式使用push方法激活上下文, 执行完相关操作后pop退出
# app_ctx = app.app_context()
# app_ctx.push()
# print(current_app.name)
# app_ctx.pop()

# # 请求上下文可以通过test_request_context()方法临时创建
# with app.test_request_context('/hello'):
#     request.method
#     # 这里同样可以使用push和pop方法显式激活或者销毁请求上下文
    
# # 上下文钩子 --- 简单了解： 例如在请求处理结束后，需要数据库关闭链接
# @app.teardown_appcontext()
# def teardown_db(exception):
#     db.close()

# http进阶实践
# 重定向回上一个页面
# @app.route('/foo')
# def foo():
#     return f'<h1>Foo gpage</h1><a href={url_for('do_something')}>Do something</a>'
# @app.route('/bar')
# def bar():
#     return f'<h1>Bar page</h1><a href={url_for('do_something')}>Do something</a>'
# @app.route('/do_something')
# def do_something():
#     # do something
#     return redirect(url_for('test_login'))

@app.route('/test_login')
def test_login():
    return f'<h1>test_login</h1>'

# 获取上一个页面的url (1)http referrer (2)查询参数
# return redirect(request.referrer)
# 添加备用选项
# return redirect(request.referrer or url_for('hello))

# 手动加入包含当前页面的url查询参数
@app.route('/foo')
def foo():
    return f'<h1>Foo page</h1><a href={url_for('do_something', next=request.full_path)}>Do something</a>'
@app.route('/bar')
def bar():
    return f'<h1>Bar page</h1><a href={url_for('do_something', next=request.full_path)}>Do something</a>'


@app.route('/do_something_and_redirect')
def do_something():
    # do something
    return redirect_back()

# 确保next的url是应用程序内的验证过的url
from urllib.parse import urlparse, urljoin
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# 重定向到默认的hello视图, 安全版
def redirect_back(default='test_login', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
