---
name: puppeteer-browser
description: Puppeteer/Playwright 浏览器自动化技能 - 模拟浏览器行为，可用于绕过 Cloudflare 等 JS Challenge 防护
homepage: https://github.com/puppeteer/puppeteer
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","npm"],"env":["BROWSER_CONFIG"]},"primaryEnv":"BROWSER_CONFIG"}}
---

# Puppeteer Browser - 浏览器自动化

使用 Puppeteer 进行浏览器自动化，可绕过 Cloudflare 等 JS Challenge 防护。

## 环境要求

### 安装 Node.js
```bash
# 使用 nvm 安装
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 20
nvm use 20
```

### 安装 Puppeteer
```bash
# 全局安装
npm install -g puppeteer

# 或本地安装
npm install puppeteer
```

### 安装 Chrome (可选)
```bash
# Ubuntu/Debian
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable
```

## 快速开始

### 1. 基本浏览器操作

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto('https://www.mehs.us/');
  await page.screenshot({ path: 'screenshot.png' });
  
  await browser.close();
})();
```

### 2. 绕过 Cloudflare

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage'
    ]
  });
  
  const page = await browser.newPage();
  
  // 设置真实浏览器 UA
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
  
  // 绕过自动化检测
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  
  await page.goto('https://www.mehs.us/', { waitUntil: 'networkidle2' });
  
  // 等待 Cloudflare 挑战完成
  await page.waitForSelector('body', { timeout: 30000 });
  
  console.log('页面加载完成');
  await browser.close();
})();
```

### 3. 获取页面内容

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto('https://www.mehs.us/', { waitUntil: 'networkidle2' });
  
  // 获取页面标题
  const title = await page.title();
  console.log('标题:', title);
  
  // 获取页面内容
  const content = await page.content();
  console.log('内容长度:', content.length);
  
  await browser.close();
})();
```

### 4. 表单提交

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://example.com/login');
  
  // 输入用户名密码
  await page.type('#username', 'admin');
  await page.type('#password', 'password');
  
  // 点击登录按钮
  await page.click('#submit');
  
  // 等待跳转
  await page.waitForNavigation();
  
  await browser.close();
})();
```

### 5. 截图

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto('https://www.mehs.us/');
  
  // 截图
  await page.screenshot({ path: 'page.png' });
  
  // 滚动截图
  await page.screenshot({ 
    path: 'full-page.png', 
    fullPage: true 
  });
  
  await browser.close();
})();
```

## 常用命令

| 功能 | 命令 |
|------|------|
| 启动浏览器 | `puppeteer.launch()` |
| 打开页面 | `browser.newPage()` |
| 访问 URL | `page.goto(url)` |
| 截图 | `page.screenshot()` |
| 获取内容 | `page.content()` |
| 点击元素 | `page.click(selector)` |
| 输入文本 | `page.type(selector, text)` |
| 执行 JS | `page.evaluate()` |
| 等待元素 | `page.waitForSelector()` |

## 绕过防护

### Cloudflare 绕过

```javascript
// 完整 Cloudflare 绕过示例
const puppeteer = require('puppeteer');

async function bypassCloudflare(url) {
  const browser = await puppeteer.launch({
    headless: false,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--disable-infobars',
      '--start-maximized'
    ]
  });
  
  const page = await browser.newPage();
  
  // 设置常见浏览器 UA
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
  
  // 移除 webdriver 标志
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.navigator.chrome = true;
    Object.defineProperty(navigator, 'plugins', {
      get: () => [1, 2, 3, 4, 5]
    });
  });
  
  try {
    await page.goto(url, { 
      waitUntil: 'networkidle2',
      timeout: 60000 
    });
    
    // 等待 Cloudflare 挑战
    await new Promise(r => setTimeout(r, 5000));
    
    return await page.content();
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
}

bypassCloudflare('https://www.mehs.us/');
```

## 配置选项

### 环境变量

```bash
# 可选配置
export PUPPETEER_CONFIG="headless=true,timeout=30000"
```

### 常用启动参数

| 参数 | 说明 |
|------|------|
| headless | 无头模式 |
| slowMo | 慢动作 |
| timeout | 超时时间 |
| args | Chrome 参数 |

## 注意事项

1. 仅用于授权测试
2. 遵守网站 robots.txt
3. 不要对目标造成过大负载
4. 尊重网站服务条款
