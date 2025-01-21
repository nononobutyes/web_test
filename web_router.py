from flask import Flask, render_template, request, jsonify
import yagmail
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__, 
           template_folder='docs',
           static_url_path='',
           static_folder='.')

# 从环境变量获取邮件配置
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

@app.route('/weiwei/')
def index():
    return render_template('index.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    try:
        # 检查环境变量是否存在
        if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
            return jsonify({
                'status': 'error',
                'message': '邮件服务配置不完整，请检查环境变量'
            })

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
