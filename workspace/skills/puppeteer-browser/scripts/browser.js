#!/usr/bin/env node
/**
 * Puppeteer 浏览器自动化脚本
 * 用于绕过 Cloudflare 等 JS Challenge 防护
 */

const puppeteer = require('puppeteer');

async function launchBrowser(url, options = {}) {
  const {
    headless = true,
    stealth = true,
    timeout = 30000
  } = options;

  const browser = await puppeteer.launch({
    headless,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--disable-infobars'
    ]
  });

  const page = await browser.newPage();

  // 设置真实浏览器 UA
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

  // 绕过自动化检测
  if (stealth) {
    await page.evaluateOnNewDocument(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
      window.navigator.chrome = true;
    });
  }

  try {
    console.log(`[*] 访问: ${url}`);
    await page.goto(url, { 
      waitUntil: 'networkidle2',
      timeout
    });

    // 等待页面稳定
    await new Promise(r => setTimeout(r, 3000));

    return page;
  } catch (e) {
    console.error('[!] 错误:', e.message);
    await browser.close();
    throw e;
  }
}

async function screenshot(url, output = 'screenshot.png') {
  const page = await launchBrowser(url);
  await page.screenshot({ path: output, fullPage: true });
  console.log(`[+] 截图保存: ${output}`);
  await page.browser().close();
}

async function getContent(url) {
  const page = await launchBrowser(url);
  const content = await page.content();
  await page.browser().close();
  return content;
}

// 命令行参数处理
const args = process.argv.slice(2);
const command = args[0];
const url = args[1];
const output = args[2];

switch (command) {
  case 'screenshot':
    if (!url) {
      console.error('用法: node browser.js screenshot <url> [output]');
      process.exit(1);
    }
    screenshot(url, output || 'screenshot.png');
    break;

  case 'content':
    if (!url) {
      console.error('用法: node browser.js content <url>');
      process.exit(1);
    }
    getContent(url).then(content => {
      console.log(content);
    });
    break;

  default:
    console.log(`
Puppeteer 浏览器自动化

用法:
  node browser.js screenshot <url> [output]  截图
  node browser.js content <url>             获取页面内容

示例:
  node browser.js screenshot https://www.mehs.us/
  node browser.js content https://www.mehs.us/
    `);
}
