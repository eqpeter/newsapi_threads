#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
從 NewsAPI 獲取新聞並使用 Threads SDK 發布到 Threads
"""

import json
import os
import requests
from datetime import datetime, timedelta
from threads.api import ThreadsAPI  # threads-sdk包的導入方式
from api_key_config import THREADS_TOKEN, THREADS_USER_ID, THREADS_APP_ID, THREADS_APP_SECRET, NEWS_API_KEY

def truncate_text(text, max_length=400):
    """
    截斷文本，確保不超過指定的最大長度
    如果截斷，會在末尾添加...
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def get_news_and_post_to_threads(num_news=2):
    """
    獲取多篇財經新聞並發布到 Threads
    
    參數:
    num_news (int): 要獲取和發布的新聞數量
    
    返回:
    int: 成功發布的新聞數量
    """
    success_count = 0
    
    try:
        # 使用配置中的APP_SECRET
        if not THREADS_APP_SECRET:
            APP_SECRET = input("請輸入您的 APP_SECRET（從 Meta 開發者控制台獲取）: ")
        else:
            APP_SECRET = THREADS_APP_SECRET
            print(f"使用配置中的APP_SECRET: {APP_SECRET[:5]}...")
        
        # 初始化 Threads API（移除app_id參數）
        threads = ThreadsAPI(
            user_id=THREADS_USER_ID,
            access_token=THREADS_TOKEN,
            app_secret=APP_SECRET
        )
        
        print(f"正在獲取{num_news}篇新聞...")
        
        # 設置搜索參數
        today = datetime.now().strftime('%Y-%m-%d')
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        # 導入 NewsAPI
        try:
            from newsapi.newsapi_client import NewsApiClient
        except ImportError:
            print("正在嘗試安裝正確的NewsAPI庫...")
            import subprocess
            subprocess.check_call(["pip", "install", "newsapi-python"])
            # 重新導入
            from newsapi.newsapi_client import NewsApiClient
        
        # 初始化 NewsAPI 客戶端
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        
        # 獲取財經新聞
        finance_news = newsapi.get_everything(
            q='台積電 OR 台股',
            language='zh',
            from_param=week_ago,
            to=today,
            sort_by='relevancy',
            page_size=num_news  # 獲取指定數量的新聞
        )
        
        articles = finance_news.get('articles', [])
        
        if not articles:
            print("未找到新聞！")
            return 0
        
        print(f"找到 {len(articles)} 篇新聞")
        
        # 處理每篇新聞
        for i, article in enumerate(articles):
            print(f"\n處理第 {i+1} 篇新聞...")
            
            # 截斷標題和描述
            title = truncate_text(article['title'])
            description = truncate_text(article.get('description', '無描述'))
            source = article['source']['name']
            url = article['url']
            
            # 構建貼文內容
            post_content = f"{title}\n\n{description}\n\n來源: {source}\n連結: {url}"
            
            print("\n獲取到的新聞：")
            print("=" * 80)
            print(post_content)
            print("=" * 80)
            
            # 發布到 Threads
            print("\n正在創建貼文容器...")
            media_json = threads.create_media_container(text=post_content)
            print(f"容器創建結果: {media_json}")
            
            if not media_json or "id" not in media_json:
                print("創建貼文容器失敗!")
                continue
                
            container_id = media_json.get("id")
            print(f"容器 ID: {container_id}")
            
            # 發布貼文
            print("正在發布貼文...")
            publish_result = threads.publish_container(container_id)
            print(f"發布結果: {publish_result}")
            
            if publish_result:
                print("貼文發布成功!")
                success_count += 1
            else:
                print("貼文發布失敗!")
            
            # 在兩篇貼文之間稍作停頓，避免頻率限制
            if i < len(articles) - 1:
                print("等待3秒後發布下一篇新聞...")
                import time
                time.sleep(3)
                
    except Exception as e:
        print(f"處理過程中發生錯誤: {str(e)}")
    
    return success_count

if __name__ == "__main__":
    print("開始獲取新聞並發布到 Threads...")
    
    news_count = 2  # 要發布的新聞數量
    success_count = get_news_and_post_to_threads(news_count)
    
    print(f"\n任務完成！成功發布 {success_count}/{news_count} 篇新聞到 Threads。")
    
    if success_count == 0:
        print("所有新聞發布失敗，請檢查錯誤訊息。")
    elif success_count < news_count:
        print(f"部分新聞發布失敗，共有 {news_count - success_count} 篇未能發布。") 