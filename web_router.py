from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__, 
           template_folder='docs',
           static_url_path='',
           static_folder='.')

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # 用于flash消息
db = SQLAlchemy(app)

# 定义消息模型
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 创建数据库表
with app.app_context():
    db.create_all()

# 发送邮件的函数
def send_email_notification(message):
    # 邮件服务器配置
    smtp_host = 'smtp.qq.com'  # 使用QQ邮箱为例
    smtp_port = 587
    smtp_user = '你的邮箱@qq.com'
    smtp_pass = '你的邮箱授权码'  # 需要在邮箱设置中获取授权码

    # 创建邮件内容
    msg = MIMEText(f"""
    收到新留言：
    姓名：{message.name}
    邮箱：{message.email}
    内容：{message.content}
    时间：{message.created_at}
    """, 'plain', 'utf-8')
    
    msg['Subject'] = Header('新留言通知', 'utf-8')
    msg['From'] = smtp_user
    msg['To'] = smtp_user

    try:
        # 发送邮件
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [smtp_user], msg.as_string())
        return True
    except Exception as e:
        print(f"发送邮件失败：{e}")
        return False

@app.route('/weiwei/')
def index():
    return render_template('index.html')

# 处理表单提交
@app.route('/submit_message', methods=['POST'])
def submit_message():
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        email = request.form.get('email')
        content = request.form.get('content')

        # 创建新消息
        new_message = Message(
            name=name,
            email=email,
            content=content
        )

        try:
            # 保存到数据库
            db.session.add(new_message)
            db.session.commit()

            # 发送邮件通知
            send_email_notification(new_message)

            return {'status': 'success', 'message': '消息已发送！'}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
