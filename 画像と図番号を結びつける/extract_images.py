#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import fitz
import pandas as pd


# In[6]:


def extract_images(input_folder, csv_filename):
    """
    指定したフォルダ内の複数のPDFファイルから画像と座標を抽出し、データフレームに保存する関数。

    Args:
        input_folder (str): PDFファイルが格納されているフォルダへのパス。
        csv_filename (str): 出力CSVファイルのパス。
    """
    # データフレームのためのリストを初期化
    data = []

    pdf_files = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_document = fitz.open(pdf_file)
        pdf_filename = os.path.basename(pdf_file)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            image_infos = page.get_image_info(xrefs=True)  # 画像の情報を取得

            for img_index, img_info in enumerate(image_infos):
                # 位置情報の取得
                x0, y0, x1, y1 = img_info['bbox']

                # データフレームに情報を追加
                data.append({
                    'PDFファイル': pdf_filename,
                    'ページ番号': page_number + 1,
                    '画像インデックス': img_index,
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


# In[7]:


if __name__ == "__main__":
    input_folder = '../sample-pdf'
    csv_filename = 'image_info.csv'
    df = extract_images(input_folder, csv_filename)


# In[ ]:




