# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup

def search_keyword_in_div(url, keyword):
  """
  This function searches for a specific keyword in the text content of all div tags on a given URL.
  It then prints the class name and the first 100 characters of the text content of the div tags that contain the keyword.

  Args:
    url: The URL of the webpage to search.
    keyword: The keyword to search for.
  """
  results = []
  try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    div_tags = soup.find_all("div")
    for div_tag in div_tags:
      text = div_tag.get_text(strip=True)  # Get the text content of the div tag and strip whitespace
      if keyword in text:
        class_name = div_tag.get("class")  # Get the class attribute
        if class_name:
          class_name = " ".join(class_name)  # Convert list of class names to a string
        else:
          class_name = "None"  # If no class attribute is found, display "None"
        results.append((class_name, text[:100]))

  except requests.exceptions.RequestException as e:
    st.write(f"Error fetching URL: {e}")
  except Exception as e:
    st.write(f"An error occurred: {e}")

  return results


# Streamlitアプリのタイトルを設定
st.title("Class Nameを見つける 🔎")

st.markdown('---')
st.markdown('This app shows which tag in the HTML code the keyword you are looking for on your website belongs to. Enter the URL and keywords in the blanks below and press "search".')
st.markdown('---')

# URLとキーワードの入力
url = st.text_input("URLを入力してください")
keyword = st.text_input("キーワードを入力してください")

# 検索ボタン
if st.button("Search"):
    if url and keyword:
        # キーワード検索を実行
        results = search_keyword_in_div(url, keyword)

        # 結果を表示
        if results:
            for class_name, text in results:
                st.write(f"class: {class_name}")
                st.write(f"text: {text}...\n")
        else:
            st.warning("キーワードが見つかりませんでした。")
    else:
        st.warning("URLとキーワードを入力してください。")