#!/usr/bin/env python
# coding: utf-8

# In[5]:


# コード更新用ファイル　
# 下記コードを実行するとextract_figure.pyファイルが更新される
get_ipython().system('jupyter nbconvert --to python extract_figure.ipynb')


# In[2]:


import os
import fitz
import re
import pandas as pd


# In[3]:


def extract_figure(pdf_folder, pattern, csv_filename):
    """
    フォルダ内の複数のPDFファイルから図番号とその座標を抽出し、データフレームに格納する関数。

    Args:
        pdf_folder (str): PDFファイルが格納されているフォルダのパス。
        pattern (str): 図番号の正規表現パターン。
        csv_filename (str): 出力csvファイルのパス

    """
    # データフレームのためのリストを初期化
    data = []

    # フォルダ内のPDFファイルのリストを取得
    pdf_files = [os.path.join(pdf_folder, filename) for filename in os.listdir(pdf_folder) if filename.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_document = fitz.open(pdf_file)
        
        # PDFの縦の長さを取得
        pdf_height = pdf_document[0].rect.height

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pdf_text = page.get_text()
            blocks = page.get_text("blocks")

            for block in blocks:
                text = block[4]  # テキスト部分を取得
                match = re.search(pattern, text)
                if match:
                        x0, y0, x1, y1 = block[:4]  # ブロックの座標を取得

                        # マッチした部分の開始・終了位置を取得
                        start_pos = match.start()
                        end_pos = match.end()

                        # 開始・終了位置の座標を調整
                        x0 = x0 + start_pos  # これは簡易的な方法であり、実際には適切な位置を計算する必要がある
                        x1 = x0 + end_pos    # 同上
                        
                        # y座標にページ数×PDFの縦の長さを加算
                        y0 += page_number * pdf_height
                        y1 += page_number * pdf_height

                        print(f"Matched text: {match.group()} at coordinates: ({x0}, {y0}), ({x1}, {y1})")

                        data.append({
                            'PDFファイル': os.path.basename(pdf_file),
                            'ページ番号': page_number + 1,
                            '図番号': match.group(),
                            'x0': x0,
                            'y0': y0,
                            'x1': x1,
                            'y1': y1
                        })

        pdf_document.close()

    # データフレームに情報を格納
    df = pd.DataFrame(data)
    
    # データフレームをCSVファイルとして保存
    df.to_csv(csv_filename, index=False)

    return df


# In[4]:


# 使用例:
if __name__ == "__main__":
    pdf_folder = '../sample-pdf'  # PDFファイルが格納されているフォルダのパス
    pattern = r"【図 [0-9]+\-[0-9]+】"  # 図番号の正規表現パターン
    figure_csv_filename = 'figure_info.csv'
    result_df = extract_figure(pdf_folder, pattern, figure_csv_filename)


# In[ ]:




