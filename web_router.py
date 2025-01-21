from flask import Flask, render_template, request, jsonify
import yagmail

app = Flask(__name__, 
           template_folder='docs',
           static_url_path='',
           static_folder='.')

# 邮件配置
SENDER_EMAIL = '2911901868@qq.com'  # 你的QQ邮箱
SENDER_PASSWORD = 'mxpmolomkebpdhcd'  # QQ邮箱的授权码（不是登录密码）
RECEIVER_EMAIL = '2911901868@qq.com'  # 接收消息的邮箱

@app.route('/weiwei/')
def index():
    return render_template('index.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    try:
        name = request.form.get('name')
        content = request.form.get('content')

        # 创建邮件内容
        message = f"""
        收到新留言：
        
        姓名：{name}
        内容：{content}
        """

        # 使用yagmail发送邮件
        yag = yagmail.SMTP(user=SENDER_EMAIL, 
                          password=SENDER_PASSWORD, 
                          host='smtp.qq.com')
        
        yag.send(to=RECEIVER_EMAIL,
                subject='个人网站新留言',
                contents=message)
        
        return jsonify({'status': 'success', 'message': '消息已发送'})

    except Exception as e:
        print(f"发送邮件失败：{str(e)}")  # 添加错误日志
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
