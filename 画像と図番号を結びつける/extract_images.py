#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import fitz
import pandas as pd


# In[2]:


def extract_images_and_save_to_dataframe(input_folder, output_root_folder):
    """
    指定したフォルダ内の複数のPDFファイルから画像と座標を抽出し、データフレームに保存する関数。

    Args:
        input_folder (str): PDFファイルが格納されているフォルダへのパス。
        output_root_folder (str): 画像とデータフレームを保存するルートフォルダへのパス。
    """
    # データフレームのためのリストを初期化
    data = []

    os.makedirs(output_root_folder, exist_ok=True)

    pdf_files = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_filename = os.path.basename(pdf_file)
        pdf_name_without_extension = os.path.splitext(pdf_filename)[0]
        output_folder = os.path.join(output_root_folder, pdf_name_without_extension)
        os.makedirs(output_folder, exist_ok=True)

        print(f'Processing {pdf_file}')

        pdf_document = fitz.open(pdf_file)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_data = base_image['image']
                image_format = base_image['ext']

                image_filename = f'page{page_number+1}_img{img_index}.{image_format}'
                image_path = os.path.join(output_folder, image_filename)
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data)

                # 位置情報の取得
                x0, y0, x1, y1 = img[2], img[3], img[4], img[5]

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
    csv_filename = 'image_info.csv'
    csv_path = os.path.join(output_root_folder, csv_filename)
    df.to_csv(csv_path, index=False)



# In[3]:


# 使用例:
if __name__ == "__main__":
    input_folder = '../sample-pdf'
    output_root_folder = 'output-images'
    extract_images_and_save_to_dataframe(input_folder, output_root_folder)


# In[ ]:




