# 自動抓新聞發布到 Threads 腳本

此腳本能夠自動從 NewsAPI 獲取最新的財經新聞，並直接發布到 Threads 平台。使用 Threads SDK 實現了無縫集成，讓您輕鬆將新聞內容分享給您的關注者。

## 功能特點

- 自動從 NewsAPI 獲取最新財經新聞
- 精選相關度最高的文章
- 自動格式化新聞內容，包含標題、描述、來源和連結
- 使用官方 Threads SDK 發布內容
- 完整的錯誤處理和日誌輸出

## 安裝前提

1. Python 3.6+
2. 有效的 NewsAPI 密鑰（腳本已內置一個可用的API密鑰，但建議替換為自己的密鑰）
3. Meta 開發者帳號和 Threads API 訪問權限
4. Threads 帳號已連接至 Meta 開發者應用

## Threads API 申請步驟

1. **創建 Meta 開發者帳號**
   - 前往 [Meta 開發者平台](https://developers.facebook.com/)
   - 註冊或登錄您的 Meta 帳號

2. **創建 Threads API 應用**
   - 在開發者控制台右上角點擊 "Create App"
   - 選擇 "Access the Threads API" 作為應用類型
   - 填寫應用名稱和其他必要信息
   - 完成應用創建流程

3. **開啟 API 權限**
   - 在應用控制台中，確保已經開啟所有 Threads API 權限
   - 預設情況下，僅會開啟一個 API，需手動開啟其他所需 API

4. **添加 Instagram 測試帳號**
   - 在應用設置中，將您的 Instagram 帳號添加為測試帳號
   - 輸入帳號時不需要添加 "@" 符號

5. **接受應用連接邀請**
   - 添加測試帳號後，您會收到一個邀請通知
   - 接受此邀請，允許 Threads 與您的應用程式連動

6. **產生訪問令牌 (Access Token)**
   - 在 Graph 測試頁面點擊 "Generate Token"
   - 完成授權流程，同意必要的權限請求

7. **獲取必要的憑證**
   - 用戶 ID: 使用 `/me` API 獲取您的 ID
   - Access Token: 步驟 6 中生成的令牌
   - App Secret: 在應用控制台的"設定">"基本"中獲取

## 安裝步驟

1. 確保已安裝所需的套件：

```
pip install threads-sdk newsapi-python requests
```

或使用項目中的requirements.txt：

```
pip install -r requirements.txt
```

2. 創建 `api_key_config.py` 文件，並設置您的 API 憑證：

   方法一：直接創建並編輯
   ```python
   # Threads API 憑證
   THREADS_TOKEN = "您的_THREADS_ACCESS_TOKEN"  # 替換為您的 Threads API 存取權杖
   THREADS_USER_ID = "您的_THREADS_USER_ID"     # 替換為您的 Threads 用戶 ID
   THREADS_APP_ID = "您的_THREADS_APP_ID"       # 替換為您的 Threads 應用 ID
   THREADS_APP_SECRET = "您的_THREADS_APP_SECRET" # 替換為您的 Threads 應用密鑰

   # NewsAPI 憑證
   NEWS_API_KEY = "您的_NEWS_API_KEY" # 替換為您的 NewsAPI 密鑰
   ```
   
   方法二：使用提供的模板
   ```
   # 複製模板文件
   cp api_key_config_template.py api_key_config.py
   
   # 然後編輯 api_key_config.py 文件，填入您的API密鑰
   ```

3. (可選) 修改 `news_to_threads.py` 中的 NewsAPI 查詢參數，以獲取您感興趣的新聞類型

## 使用方法

運行腳本：

```
python news_to_threads.py
```

運行時，腳本會檢查 api_key_config.py 中的 APP_SECRET 設置。如果未設置（保持為 "您的應用密鑰"），則會提示您輸入 APP_SECRET（從 Meta 開發者控制台獲取）。輸入後，腳本將：
1. 連接到 NewsAPI 獲取最新財經新聞
2. 選取相關度最高的一篇文章
3. 將新聞內容格式化並顯示
4. 創建 Threads 貼文容器
5. 發布新聞至您的 Threads 帳號

## 修改新聞關鍵字

如果您想要獲取不同類型的新聞，可以修改 `news_to_threads.py` 文件中的搜索關鍵字：

1. 打開 `news_to_threads.py` 文件
2. 找到第66行左右的搜索參數：
   ```python
   finance_news = newsapi.get_everything(
       q='台積電 OR 台股',  # 搜索關鍵字在這裡
       language='zh',
       from_param=week_ago,
       to=today,
       sort_by='relevancy',
       page_size=1  # 只獲取一篇新聞
   )
   ```
3. 修改 `q=` 參數中的關鍵字，例如：
   - 科技新聞：`q='蘋果 OR 谷歌 OR 微軟'`
   - 全球財經：`q='股市 OR 經濟 OR 美股'`
   - 加密貨幣：`q='比特幣 OR 以太坊 OR 區塊鏈'`

關鍵字之間可以使用以下操作符：
- `OR`: 搜索包含任一關鍵字的新聞
- `AND`: 搜索同時包含多個關鍵字的新聞
- `-`: 排除包含特定關鍵字的新聞，例如 `台積電 -台股`

保存文件後，下次運行腳本時將獲取您指定的新聞類型。

## 修改獲取新聞數量

默認情況下，腳本會獲取並發布2篇新聞。如果您想修改獲取和發布的新聞數量：

1. 打開 `news_to_threads.py` 文件
2. 找到主程序部分（約在文件末尾）：
   ```python
   if __name__ == "__main__":
       print("開始獲取新聞並發布到 Threads...")
       
       news_count = 2  # 要發布的新聞數量
       success_count = get_news_and_post_to_threads(news_count)
       
       # ... 後續代碼 ...
   ```
3. 修改 `news_count` 的值為您希望獲取和發布的新聞數量

注意事項：
- 發布過多新聞可能會受到Threads API頻率限制
- 為避免這個問題，腳本在發布每篇新聞之間會等待3秒
- 對於大量新聞發布，建議適當增加每篇間隔時間

## 密鑰安全處理

為了確保API密鑰和敏感信息的安全，建議採取以下措施：

1. **環境變量**: 使用環境變量存儲密鑰，而不是直接寫在代碼中
   ```python
   import os
   API_KEY = os.environ.get("NEWS_API_KEY")
   ```

2. **加密配置文件**: 將配置文件加密存儲，運行時解密
   
3. **使用密鑰管理服務**: 如AWS Secrets Manager或Hashicorp Vault等專業密鑰管理服務

4. **添加.gitignore**: 將包含敏感信息的文件添加到.gitignore，避免提交到版本控制系統

## 注意事項

- Threads API 的 ACCESS_TOKEN 有效期為 24 小時，需要定期更新
- 如需長期使用，請考慮實現長期 ACCESS_TOKEN 的獲取機制
- 請遵守 NewsAPI 和 Threads API 的使用條款和限制
- 本腳本中已內置一個 NewsAPI 密鑰，但建議替換為您自己的密鑰以避免超出配額限制

## 定時自動發布

如需定時自動發布，可以使用系統排程工具：

### Windows (使用工作排程器)
1. 開啟工作排程器的方法：
   - 方法一：按下「Windows鍵 + R」，輸入「taskschd.msc」，點擊「確定」
   - 方法二：在開始菜單搜尋「工作排程器」
2. 在工作排程器中，點擊右側「操作」面板中的「創建基本任務」
3. 設置任務名稱（如「Threads新聞發布」）並點擊「下一步」
4. 選擇觸發器（例如每天特定時間）並點擊「下一步」
5. 設置時間和頻率後點擊「下一步」
6. 選擇「啟動程序」操作並點擊「下一步」
7. 在「程序或腳本」欄位中，瀏覽並選擇Python解釋器的路徑（如「C:\Python310\python.exe」）
8. 在「添加引數」欄位中填入腳本路徑（如「E:\myPython\newsapi_threads\news_to_threads.py」）
9. 點擊「下一步」，然後點擊「完成」

### Linux/macOS (使用 cron)
編輯 crontab 文件：
```
crontab -e
```

添加排程任務（例如每天上午 9 點運行）：
```
0 9 * * * /usr/bin/python /path/to/news_to_threads.py
```

## 自定義與擴展

此腳本可以進一步擴展:
- 增加更多新聞類別
- 添加圖片支持
- 將 APP_SECRET 保存到配置文件
- 添加電子郵件通知
- 實現多帳號支持

## 疑難排解

1. **無法獲取新聞**
   - 檢查 NewsAPI 密鑰是否有效
   - 確認網絡連接
   - 嘗試調整搜索參數，如擴大日期範圍或更改關鍵詞

2. **無法發布到 Threads**
   - 檢查 ACCESS_TOKEN 是否過期（有效期僅 24 小時）
   - 確認 APP_SECRET 輸入正確
   - 檢查 Threads 帳號是否已正確連接到應用
   - 查看 Meta 開發者控制台中的錯誤日誌

3. **安裝依賴失敗**
   - 嘗試逐個安裝依賴：`pip install requests`、`pip install newsapi-python`、`pip install threads-sdk`
   - 檢查 Python 版本是否兼容（需要 Python 3.6+）
   - 如遇網絡問題，可嘗試使用國內鏡像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 參考資源

- [Threads SDK 說明文檔](https://nijialin.com/2024/08/17/python-threads-sdk-introduction/)
- [NewsAPI 官方文檔](https://newsapi.org/docs)
- [Meta 開發者平台](https://developers.facebook.com/) 
