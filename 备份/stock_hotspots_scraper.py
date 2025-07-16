#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国股市热点信息获取程序
每日股市热点和重要信息抓取
"""

import requests
from datetime import datetime, timedelta
import json
import time
import os
from typing import Dict, List, Optional
import re

class StockHotspotsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.today = datetime.now().strftime('%Y-%m-%d')
        
    def get_sina_finance_news(self) -> List[Dict]:
        """获取新浪财经热点新闻"""
        try:
            url = "https://feed.mix.sina.com.cn/api/roll/get"
            params = {
                'pageid': '153',
                'lid': '2509',
                'k': '',
                'num': '20',
                'page': '1'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            news_list = []
            if data.get('result', {}).get('data'):
                for item in data['result']['data']:
                    news_list.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'time': item.get('ctime', ''),
                        'source': '新浪财经'
                    })
            
            return news_list
        except Exception as e:
            print(f"获取新浪财经新闻失败: {e}")
            return []
    
    def get_eastmoney_hot_stocks(self) -> List[Dict]:
        """获取东方财富热门股票"""
        try:
            url = "http://push2.eastmoney.com/api/qt/clist/get"
            params = {
                'pn': '1',
                'pz': '20',
                'po': '1',
                'np': '1',
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': '2',
                'invt': '2',
                'fid': 'f3',
                'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23',
                'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            hot_stocks = []
            if data.get('data', {}).get('diff'):
                for item in data['data']['diff']:
                    hot_stocks.append({
                        'code': item.get('f12', ''),
                        'name': item.get('f14', ''),
                        'price': item.get('f2', 0),
                        'change_percent': item.get('f3', 0),
                        'change_amount': item.get('f4', 0),
                        'volume': item.get('f5', 0),
                        'turnover': item.get('f6', 0)
                    })
            
            return hot_stocks
        except Exception as e:
            print(f"获取热门股票失败: {e}")
            return []
    
    def get_market_indices(self) -> Dict:
        """获取主要指数信息"""
        try:
            # 上证指数、深证成指、创业板指
            indices = {
                '000001': '上证指数',
                '399001': '深证成指',
                '399006': '创业板指'
            }
            
            result = {}
            for code, name in indices.items():
                url = f"http://push2.eastmoney.com/api/qt/stock/get"
                params = {
                    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                    'invt': '2',
                    'fltt': '2',
                    'fields': 'f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52',
                    'secid': f"1.{code}" if code.startswith('399') else f"0.{code}"
                }
                
                response = self.session.get(url, params=params, timeout=10)
                data = response.json()
                
                if data.get('data'):
                    item = data['data']
                    result[name] = {
                        'price': item.get('f43', 0),
                        'change_percent': item.get('f170', 0),
                        'change_amount': item.get('f169', 0),
                        'volume': item.get('f47', 0),
                        'turnover': item.get('f48', 0)
                    }
                
                time.sleep(0.1)  # 避免请求过快
            
            return result
        except Exception as e:
            print(f"获取指数信息失败: {e}")
            return {}
    
    def format_report(self, news_list: List[Dict], hot_stocks: List[Dict], indices: Dict) -> str:
        """格式化报告"""
        report = f"""
========================================
中国股市热点信息日报
日期: {self.today}
========================================

📊 主要指数表现
----------------------------------------
"""
        
        for name, data in indices.items():
            change_symbol = "📈" if data['change_percent'] > 0 else "📉" if data['change_percent'] < 0 else "📊"
            report += f"{change_symbol} {name}: {data['price']:.2f} ({data['change_percent']:+.2f}%)\n"
        
        report += f"""
🔥 热门股票 (前10)
----------------------------------------
"""
        
        for i, stock in enumerate(hot_stocks[:10], 1):
            change_symbol = "🔴" if stock['change_percent'] > 0 else "🟢" if stock['change_percent'] < 0 else "⚪"
            report += f"{i:2d}. {change_symbol} {stock['name']} ({stock['code']}): {stock['price']:.2f} ({stock['change_percent']:+.2f}%)\n"
        
        report += f"""
📰 财经热点新闻 (前10)
----------------------------------------
"""
        
        for i, news in enumerate(news_list[:10], 1):
            report += f"{i:2d}. {news['title']}\n"
            report += f"    来源: {news['source']} | 时间: {news['time']}\n"
            report += f"    链接: {news['url']}\n\n"
        
        report += f"""
----------------------------------------
报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================
"""
        
        return report
    
    def save_report(self, report: str):
        """保存报告到文件"""
        filename = f"stock_hotspots_{self.today}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {filename}")
    
    def run(self):
        """运行主程序"""
        print("正在获取中国股市热点信息...")
        
        # 获取各种数据
        print("📰 获取财经新闻...")
        news_list = self.get_sina_finance_news()
        
        print("🔥 获取热门股票...")
        hot_stocks = self.get_eastmoney_hot_stocks()
        
        print("📊 获取指数信息...")
        indices = self.get_market_indices()
        
        # 生成报告
        report = self.format_report(news_list, hot_stocks, indices)
        
        # 打印到控制台
        print(report)
        
        # 保存到文件
        self.save_report(report)
        
        # 发送邮件通知（如果启用）
        self.send_email_notification(report)
        
        print("✅ 股市热点信息获取完成！")
    
    def send_email_notification(self, report):
        """发送邮件通知"""
        try:
            # 导入配置（需要在同目录下有config.py文件）
            from config import SETTINGS
            
            if not SETTINGS.get('send_email', False):
                print("📧 邮件通知未启用")
                return
                
            email_config = SETTINGS['email_settings']
            
            # 检查邮件配置
            if not all([
                email_config.get('email'),
                email_config.get('password'),
                email_config.get('to_email')
            ]):
                print("❌ 邮件配置不完整，请检查config.py")
                return
            
            print("📧 正在发送邮件通知...")
            
            # 发送邮件
            success = self.send_email(report, email_config)
            
            if success:
                print(f"✅ 邮件已成功发送到: {email_config['to_email']}")
            else:
                print("❌ 邮件发送失败")
                
        except ImportError:
            print("❌ 未找到config.py文件，请确保配置文件存在")
        except Exception as e:
            print(f"❌ 邮件发送过程中出错: {e}")
    
    def send_email(self, report_content, email_config):
        """发送邮件的具体实现"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.header import Header
            import ssl
            
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = Header(f"股市热点助手 <{email_config['email']}>", 'utf-8')
            msg['To'] = Header(email_config['to_email'], 'utf-8')
            msg['Subject'] = Header(f"📊 股市热点日报 - {self.today}", 'utf-8')
            
            # 邮件正文
            body = f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #f4f4f4; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .footer {{ background-color: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 中国股市热点日报</h1>
        <p>{self.today}</p>
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
            
            # 尝试多种连接方式
            smtp_configs = [
                # 方式1: SMTP_SSL + 465端口
                {'method': 'SMTP_SSL', 'port': 465, 'use_tls': False},
                # 方式2: SMTP + STARTTLS + 587端口
                {'method': 'SMTP', 'port': 587, 'use_tls': True},
                # 方式3: SMTP + STARTTLS + 25端口
                {'method': 'SMTP', 'port': 25, 'use_tls': True}
            ]
            
            for config in smtp_configs:
                try:
                    print(f"📧 尝试连接方式: {config['method']} 端口:{config['port']}")
                    
                    if config['method'] == 'SMTP_SSL':
                        # 使用SSL连接
                        context = ssl.create_default_context()
                        # 降低SSL安全级别以兼容QQ邮箱
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        
                        server = smtplib.SMTP_SSL(email_config['smtp_server'], config['port'], context=context)
                    else:
                        # 使用普通SMTP连接
                        server = smtplib.SMTP(email_config['smtp_server'], config['port'])
                        server.ehlo()
                        
                        if config['use_tls']:
                            context = ssl.create_default_context()
                            context.check_hostname = False
                            context.verify_mode = ssl.CERT_NONE
                            server.starttls(context=context)
                            server.ehlo()
                    
                    print("📧 正在登录邮箱...")
                    server.login(email_config['email'], email_config['password'])
                    
                    print("📧 正在发送邮件...")
                    server.sendmail(email_config['email'], email_config['to_email'], msg.as_string())
                    
                    server.quit()
                    print(f"✅ 邮件发送成功！使用方式: {config['method']} 端口:{config['port']}")
                    return True
                    
                except Exception as e:
                    print(f"❌ 方式 {config['method']}:{config['port']} 失败: {e}")
                    try:
                        server.quit()
                    except:
                        pass
                    continue
            
            print("❌ 所有连接方式都失败了")
            return False
            
        except Exception as e:
            print(f"❌ 邮件发送过程中出错: {e}")
            return False

def main():
    """主函数"""
    scraper = StockHotspotsScraper()
    scraper.run()

if __name__ == "__main__":
    main()