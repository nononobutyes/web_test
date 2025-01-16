from flask import Flask, render_template # 应用flask框架

app = Flask(__name__)

@app.route('/weiwei/') # 定义根路由，当访问根路径时，返回index函数
def index():
    return render_template('web_test.html') # 返回web_test.html页面

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) # 运行app，debug=True表示启用调试模式.
