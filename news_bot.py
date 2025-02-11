import os
import requests

# 从GitHub Secrets读取密钥
appid = os.environ.get('WECHAT_APPID')
secret = os.environ.get('WECHAT_SECRET')
news_api_key = os.environ.get('NEWS_API_KEY')

# 获取新闻（示例使用NewsAPI）
def fetch_news():
    url = f"https://apis.tianapi.com/toutiaohot/index?apiKey={news_api_key}"
    response = requests.get(url)
    return response.json()['articles'][:5]  # 取前5条新闻

# 获取微信Access Token
def get_wechat_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    response = requests.get(token_url)
    return response.json()['access_token']

# 发布到微信（示例发送文本消息）
def publish_to_wechat(content):
    token = get_wechat_token()
    url = f"https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token={token}"
    data = {
        "filter": {"is_to_all": True},
        "msgtype": "text",
        "text": {"content": content}
    }
    response = requests.post(url, json=data)
    return response.json()

if __name__ == "__main__":
    articles = fetch_news()
    formatted_content = "\n".join([f"{i+1}. {article['title']}\n链接：{article['url']}" for i, article in enumerate(articles)])
    result = publish_to_wechat(f"今日新闻速览：\n\n{formatted_content}")
    print("发布结果：", result)
