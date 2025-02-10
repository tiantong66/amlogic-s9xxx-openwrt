import os
import requests
from datetime import datetime

# 从环境变量读取密钥
appid = os.environ.get('WECHAT_APPID')
secret = os.environ.get('WECHAT_SECRET')
tianapi_key = os.environ.get('TIANAPI_KEY')

def fetch_tianapi_news():
    # 天行API示例（通用新闻接口）
    url = "http://api.tianapi.com/generalnews/index"
    params = {
        "key": tianapi_key,
        "num": 10,  # 获取10条新闻
        # 可选参数：指定新闻分类（如"keji"为科技，"guoji"为国际）
        # "col": "guoji" 
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["code"] == 200:
        articles = data["newslist"]
        return articles
    else:
        print("天行API请求失败：", data["msg"])
        return []

def format_news(articles):
    today = datetime.now().strftime("%Y-%m-%d")
    formatted_content = f"📅 每日新闻精选 ({today})\n\n"
    for idx, article in enumerate(articles[:5]):  # 取前5条
        title = article.get("title", "无标题")
        url = article.get("url", "")
        source = article.get("source", "未知来源")
        formatted_content += f"{idx+1}. {title}\n来源：{source}\n链接：{url}\n\n"
    return formatted_content.strip()

def get_wechat_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    response = requests.get(token_url)
    return response.json().get("access_token", "")

def publish_to_wechat(content):
    token = get_wechat_token()
    if not token:
        return {"error": "获取微信Token失败"}
    
    # 发布文本消息（如需图文需调用素材接口）
    post_url = f"https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token={token}"
    payload = {
        "filter": {"is_to_all": True},
        "msgtype": "text",
        "text": {"content": content}
    }
    response = requests.post(post_url, json=payload)
    return response.json()

if __name__ == "__main__":
    articles = fetch_tianapi_news()
    if articles:
        content = format_news(articles)
        result = publish_to_wechat(content)
        print("微信发布结果：", result)
    else:
        print("未获取到新闻数据")
