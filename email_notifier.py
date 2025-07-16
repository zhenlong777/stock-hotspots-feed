# email_notifier.py - 邮件通知功能
"""
股市热点信息邮件通知模块
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import ssl
from datetime import datetime

class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_stock_report(self, report_content, to_email):
        """发送股市报告邮件"""
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = Header(f"股市热点助手 <{self.email}>", 'utf-8')
            msg['To'] = Header(to_email, 'utf-8')
            msg['Subject'] = Header(f"📊 股市热点日报 - {datetime.now().strftime('%Y-%m-%d')}", 'utf-8')
            
            # 邮件正文
            body = f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #f4f4f4; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin-bottom: 30px; }}
        .stock-item {{ background-color: #f9f9f9; padding: 10px; margin: 5px 0; border-radius: 5px; }}
        .positive {{ color: #d32f2f; }}
        .negative {{ color: #388e3c; }}
        .news-item {{ border-left: 3px solid #2196f3; padding-left: 10px; margin: 10px 0; }}
        .footer {{ background-color: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 中国股市热点日报</h1>
        <p>{datetime.now().strftime('%Y年%m月%d日')}</p>
    </div>
    
    <div class="content">
        <pre style="white-space: pre-wrap; font-family: monospace;">{report_content}</pre>
    </div>
    
    <div class="footer">
        <p>本报告由股市热点助手自动生成，数据仅供参考</p>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 连接SMTP服务器并发送邮件
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, to_email, msg.as_string())
            
            print(f"✅ 邮件已发送到: {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            return False

# 增强版主程序，集成邮件功能
if __name__ == "__main__":
    # 示例：如何在主程序中使用邮件通知
    from config import SETTINGS
    
    # 如果启用了邮件通知
    if SETTINGS['send_email']:
        email_config = SETTINGS['email_settings']
        notifier = EmailNotifier(
            email_config['smtp_server'],
            email_config['smtp_port'],
            email_config['email'],
            email_config['password']
        )
        
        # 这里应该是从主程序获取的报告内容
        report_content = "这里是股市报告内容..."
        
        # 发送邮件
        notifier.send_stock_report(report_content, email_config['to_email'])