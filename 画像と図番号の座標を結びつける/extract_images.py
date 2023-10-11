#!/usr/bin/env python
# coding: utf-8

# In[3]:


# コード更新用ファイル　
# 下記コードを実行するとextract_image.pyファイルが更新される
get_ipython().system('jupyter nbconvert --to python extract_images.ipynb')


# In[6]:


import os
import fitz
import pandas as pd


# In[1]:


def extract_images(input_folder, csv_filename, output_root_folder):
    """
    指定したフォルダ内の複数のPDFファイルから画像を保存し、画像と座標をデータフレームに保存する関数。

    Args:
        input_folder (str): PDFファイルが格納されているフォルダへのパス。
        csv_filename (str): 出力CSVファイルのパス。
        output_root_folder (str): 画像を保存するルートフォルダへのパス。
    """
    # データフレームのためのリストを初期化
    data = []
    
    os.makedirs(output_root_folder, exist_ok=True)

    pdf_files = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_document = fitz.open(pdf_file)
        pdf_filename = os.path.basename(pdf_file)
        
        # PDF毎に画像保存用フォルダの作成
        pdf_name_without_extension = os.path.splitext(pdf_filename)[0]
        output_folder = os.path.join(output_root_folder, pdf_name_without_extension)
        os.makedirs(output_folder, exist_ok=True)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            image_infos = page.get_image_info(xrefs=True)  # 画像の情報を取得

            for img_index, img_info in enumerate(image_infos):
                # 位置情報の取得
                x0, y0, x1, y1 = img_info['bbox']

                # 画像を抽出して保存
                xref = img_info['xref']
                base_image = pdf_document.extract_image(xref)
                if base_image:
                    image_data = base_image['image']
                else:
                    pass # 画像が正しく取得できなかった場合のエラーハンドリングまたはスキップ処理を行うことができます。

                image_filename = f"{pdf_name_without_extension}_page{page_number + 1}_img{img_index}.png"
                image_path = os.path.join(output_folder, image_filename)

                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data)

                # データフレームに情報を追加
                data.append({
                    'PDFファイル': pdf_filename,
                    'ページ番号': page_number + 1,
                    '画像ファイル': image_filename,
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


# In[10]:


if __name__ == "__main__":
    input_folder = '../sample-pdf'
    csv_filename = 'image_info.csv'
    output_root_folder = "output-images"
    df = extract_images(input_folder, csv_filename, output_root_folder)


# In[ ]:




