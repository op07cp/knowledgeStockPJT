# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_web_pages(url, pattern, max_depth=2):
  """
  Crawls a given URL recursively to extract unique links to web pages
  matching a specific pattern.

  This function starts at a given URL and explores linked pages up to a
  specified depth, collecting only the URLs that match the provided pattern
  and lead to web pages (HTML documents). It avoids revisiting the same URLs
  to prevent infinite loops.

  Args:
    url: The URL to start crawling.
    pattern: A string representing the pattern to match in the URLs (e.g., "/blog/").
    max_depth: The maximum depth to crawl.

  Returns:
    A list of unique URLs matching the pattern and leading to web pages.
  """
  visited_urls = set()
  urls = []

  def crawl(url, depth):
    """
    Performs the recursive crawling.

    Args:
      url: The URL to crawl.
      depth: The current depth of the crawl.
    """
    if depth > max_depth:
      return

    if url in visited_urls:
      return
    visited_urls.add(url)

    try:
      response = requests.get(url, timeout=10)
      response.raise_for_status()
      time.sleep(3)

      # Check if the response is an HTML document
      if 'text/html' not in response.headers['content-type']:
        return

    except requests.exceptions.RequestException as e:
      print(f"Error fetching {url}: {e}")
      return

    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the current URL matches the pattern
    if pattern in urlparse(url).path:
      urls.append(url)
      print(f"Found URL: {url}")

    for link in soup.find_all("a", href=True):
      absolute_url = urljoin(url, link["href"])

      # Check if the link leads to a web page (not an image, PDF, etc.)
      parsed_link = urlparse(absolute_url)
      if not parsed_link.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.rar')):
        crawl(absolute_url, depth + 1)

  crawl(url, 1)
  return urls


# Streamlitアプリのタイトルを設定
st.title("URLリスト作成 📝")
st.markdown('---')
st.markdown("""
URLのページに記載されているリンクを辿ってURLのリストを作成します。
指定したキーワードが含まれるURLのみをリスト化します。サブディレクトリなどを指定してください。
深度は、リンク先のリンクの深さを示します。リンク先のリンク先のリンクまで収集する場合は3。
""")
st.markdown('---')

# Streamlitの入力フォーム
start_url = st.text_input('URLを入力してください')
url_pattern = st.text_input('キーワードを入力してください')
max_depth = st.number_input('最大深度を入力してください', min_value=1, max_value=3, value=2)

# 検索ボタン
if st.button("Search"):
  # クロール処理
  with st.spinner('Crawling... This may take minutes'):
    urls = crawl_web_pages(start_url, url_pattern, max_depth)

  # 結果表示
  st.subheader('results:')
  if urls:
    for url in urls:
      st.write(url)
    txt_data = "\n".join(urls)
    st.download_button(
      label="Download",
      data=txt_data,
      file_name="urls.txt",
      mime="text/plain",
      )
  else:
    st.write('一致するURLは見つかりませんでした。')



    
