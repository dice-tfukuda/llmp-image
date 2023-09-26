#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import fitz
import re
import pandas as pd


# In[4]:


def extract_figure_info_from_folder(input_folder, pattern):
    """
    フォルダ内の複数のPDFファイルから図番号とその座標を抽出し、データフレームに格納する関数。

    Args:
        pdf_folder (str): PDFファイルが格納されているフォルダのパス。
        pattern (str): 図番号の正規表現パターン。

    Returns:
        pd.DataFrame: 抽出された情報を格納したデータフレーム。
    """
    # データフレームのためのリストを初期化
    data = []

    # フォルダ内のPDFファイルのリストを取得
    pdf_files = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_document = fitz.open(pdf_file)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pdf_text = page.get_text()
            
            matches = re.finditer(pattern, pdf_text)

            for match in matches:
                match_text = match.group()
                # 図番号の座標を取得
                bbox = match.span()
                x0, y0, x1, y1 = bbox[0], bbox[1], bbox[0] + len(match_text), bbox[1] - len(match_text)
                data.append({
                    'PDFファイル': os.path.basename(pdf_file),
                    'ページ番号': page_number + 1,  # ページ番号をページのインデックスから計算
                    '図番号': match_text,
                    'x0': x0,
                    'y0': y0,
                    'x1': x1,
                    'y1': y1
                })

        pdf_document.close()

    # データフレームに情報を格納
    df = pd.DataFrame(data)

    return df


# In[5]:


# 使用例:
if __name__ == "__main__":
    input_folder = '../sample-pdf'  # PDFファイルが格納されているフォルダのパス
    pattern = r"【図 [0-9]+\-[0-9]+】"  # 図番号の正規表現パターン
    result_df = extract_figure_info_from_folder(pdf_folder, pattern)

# データフレームをCSVファイルとして保存
    result_df.to_csv('figure_info.csv', index=False)


# In[ ]:




