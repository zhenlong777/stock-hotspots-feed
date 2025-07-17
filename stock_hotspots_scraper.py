import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 在脚本开头添加超时配置
def create_session_with_timeout():
    """创建带有超时和重试机制的会话"""
    session = requests.Session()
    
    # 配置重试策略
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# 修改所有网络请求，添加超时
def fetch_with_timeout(url, timeout=30):
    """带超时的网络请求"""
    try:
        session = create_session_with_timeout()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"正在请求: {url}")
        response = session.get(url, headers=headers, timeout=timeout)
        print(f"请求成功，状态码: {response.status_code}")
        return response
        
    except requests.exceptions.Timeout:
        print(f"请求超时: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {url}, 错误: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None

# 在主函数中添加总体超时控制
def main():
    """主函数带总体超时控制"""
    import signal
    
    def timeout_handler(signum, frame):
        print("脚本运行超时，强制退出")
        raise TimeoutError("脚本运行超时")
    
    # 设置总体超时为4分钟
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(240)  # 4分钟超时
    
    try:
        # 您的原始代码逻辑
        print("开始抓取股市热点...")
        
        # 示例：抓取新浪财经数据
        sina_url = "https://finance.sina.com.cn/roll/index.d.html"
        response = fetch_with_timeout(sina_url, timeout=30)
        
        if response:
            print("新浪财经数据获取成功")
            # 处理数据...
        else:
            print("新浪财经数据获取失败，跳过")
        
        # 示例：抓取东方财富数据
        eastmoney_url = "http://fund.eastmoney.com/data/rankingDisplay.aspx"
        response = fetch_with_timeout(eastmoney_url, timeout=30)
        
        if response:
            print("东方财富数据获取成功")
            # 处理数据...
        else:
            print("东方财富数据获取失败，跳过")
            
        # 生成RSS文件
        print("生成RSS文件...")
        generate_rss_file()
        
        print("脚本执行完成")
        
    except TimeoutError:
        print("脚本执行超时")
        exit(1)
    except Exception as e:
        print(f"脚本执行出错: {e}")
        exit(1)
    finally:
        signal.alarm(0)  # 取消超时设置

if __name__ == "__main__":
    main()
