# config.py - 配置文件
import os # 在文件顶部添加这一行
"""
股市热点信息抓取配置
"""

# 基本设置
SETTINGS = {
    # 获取新闻数量
    'news_count': 20,
    
    # 获取热门股票数量
    'hot_stocks_count': 20,
    
    # 请求超时时间（秒）
    'timeout': 10,
    
    # 请求间隔时间（秒）
    'request_interval': 0.1,
    
    # 输出文件格式
    'output_format': 'txt',  # 可选: txt, json, html
    
    # 是否发送邮件通知
    'send_email': True,
    
    # 邮件设置（如果启用邮件通知）
    'email_settings': {
        'smtp_server': 'smtp.qq.com',      # QQ邮箱SMTP服务器
        'smtp_port': 465,                   # 主要端口，如果失败会自动尝试其他端口
        'email': '523480842@qq.com',          # 您的QQ邮箱
        'password': os.environ.get('EMAIL_PASSWORD'), # 从名为 EMAIL_PASSWORD 的环境变量中获取密码
        'to_email': '523480842@qq.com'     # 接收邮箱
    }
}

# 监控的股票代码（可选，用于特定股票监控）
WATCH_STOCKS = [
    '000001',  # 平安银行
    '000002',  # 万科A
    '000858',  # 五粮液
    '600036',  # 招商银行
    '600519',  # 贵州茅台
    '600887',  # 伊利股份
]

# 关键词过滤（用于筛选相关新闻）
KEYWORDS = [
    '股市', 'A股', '上证', '深证', '创业板',
    '涨停', '跌停', '牛市', '熊市', '行情',
    '政策', '央行', '降准', '加息', 'GDP',
    '贸易', '科技股', '消费股', '金融股'
]

# 定时任务设置说明
SCHEDULE_HELP = """
如何设置定时任务：

1. Windows系统：
   - 打开"任务计划程序"
   - 创建基本任务
   - 设置触发器为"每天"
   - 设置时间（建议股市开盘前或收盘后）
   - 操作选择"启动程序"
   - 程序路径填写python.exe的路径
   - 参数填写脚本的完整路径

2. Linux/Mac系统：
   - 使用crontab -e命令编辑定时任务
   - 添加以下行（每天9点运行）：
     0 9 * * * /usr/bin/python3 /path/to/your/script.py
   - 保存并退出

3. 推荐运行时间：
   - 早上8:30-9:00（开盘前）
   - 晚上6:00-7:00（收盘后）
"""

# 使用说明
USAGE_HELP = """
使用说明：

1. 安装依赖：
   pip install requests

2. 运行程序：
   python stock_hotspots_scraper.py

3. 程序会生成以下文件：
   - stock_hotspots_YYYY-MM-DD.txt（每日报告）

4. 自定义设置：
   - 修改config.py中的参数
   - 添加关注的股票代码
   - 配置邮件通知（可选）

5. 注意事项：
   - 程序使用公开API，请勿过度频繁请求
   - 股市数据有延迟，仅供参考
   - 建议在非交易时间运行程序
"""