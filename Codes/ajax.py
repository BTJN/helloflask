from flask import Flask, jsonify

app = Flask(__name__)

# ajax技术可以在不用重载页面的情况下就可以与服务器交换数据
@app.route('/')
@app.route('/ajax')
def ajax():
    return f'Ajax pages'

# 返回局部数据
# @app.route('/comments/<int:post_id>')
# def get_comments(post_id):
#     return render_tamplate('comments.html')

# @app.route('/profile/<int:user_id>')
# def get_profile(user_id):
#     return jsonify(username=username, bio=bio)

# 异步加载长文章
from jinja2.utils import generate_lorem_ipsum
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#load').click(function() {
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data) { 
                    $('.body').append(data); 
                }
            })
        })
    })</script>
    '''%post_body
    
@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

from flask import request

# 注入攻击示例
# @app.route('/students')
# def bobby_table():
#     pwd =  request.args.get('pwd')
#     cur = db.execute(f"Select * From students Where pwd={pwd}")
#     ret = cur.fetchall()
#     return ret

# xss 跨站攻击, 被执行查询参数javascript脚本
@app.route('/hello')
def hello():
    name = request.args.get('name')
    return f'<h1>hello {name}!</h1>'
