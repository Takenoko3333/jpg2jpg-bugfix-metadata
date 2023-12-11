# Copyright © 2023 Takenoko
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import glob
import os
import piexif
import piexif.helper
from PIL import Image, ExifTags
from datetime import datetime
from pywintypes import Time

# Windowsの場合
on_windows = os.name == 'nt'
if on_windows:
    import win32file
    import win32con

# 画像形式
IMG_INPUT_FORMAT = 'JPEG'
IMG_OUTPUT_FORMAT = 'JPEG'
# 画像拡張子
IMG_INPUT_FILENAME_EXT = 'jpg'
IMG_OUTPUT_FILENAME_EXT = 'jpg'
# ディレクトリ
INPUT_DIR = 'inputs/'
OUTPUT_DIR = 'outputs/'

# 画像を配列に格納
files = glob.glob(INPUT_DIR + '*.' + IMG_INPUT_FILENAME_EXT)

# 全画像の変換・保存
for file in files:
    file_name = os.path.splitext(os.path.basename(file))[0]
    output_file_name = file_name + '.' + IMG_OUTPUT_FILENAME_EXT
    output_file_path = OUTPUT_DIR + output_file_name
    output_file_abspath = os.path.abspath(OUTPUT_DIR + output_file_name)

    def get_user_comment(exif_data):
        user_comment_tag = None
        for tag, value in exif_data.items():
            if ExifTags.TAGS.get(tag) == 'UserComment':
                user_comment_tag = tag
                break

        if user_comment_tag:
            user_comment = exif_data[user_comment_tag]
            return user_comment

        return None

    def fix_metadata(file, output_file_path):
        # 画像を開く
        image = Image.open(file)

        # Exif情報を取得
        exif_data = image._getexif()

        # UserCommentを取得
        user_comment = get_user_comment(exif_data)

        # UserCommentを修正
        if user_comment is not None:
            # UserCommentのデコードと不要文字削除
            decoded_text = user_comment.decode('utf-8').replace('\x00', '').replace("UNICODE", "")

            # 修正
            fixed_text = decoded_text.replace('parameters: ', '')

            # Exifデータを作成
            exif_dict = {"Exif": {piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(fixed_text or '', encoding='unicode')}}

            # Exifデータをバイトに変換
            exif_bytes = piexif.dump(exif_dict)

            # Exifデータを挿入して新しい画像を保存
            image.save(output_file_path)
            piexif.insert(exif_bytes, output_file_path)

        # 画像を閉じる
        image.close()

    # Exifデータを修正して保存
    fix_metadata(file, output_file_path)

    # 日時情報を取得
    with Image.open(file):
        access_time   = os.path.getatime(file) # アクセス日時
        modify_time   = os.path.getmtime(file) # 更新日時

        if on_windows:
            creation_time = os.path.getctime(file) # 作成日時

    # 日付情報の設定
    # PNGファイルのハンドルを取得（Windowsのみ）
    if on_windows:
        handle = win32file.CreateFile(
            output_file_path,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            0,
            None
        )

        # JPEGファイルに元画像の作成日時、アクセス日時、更新日時を設定
        win32file.SetFileTime(handle, Time(creation_time), Time(access_time), Time(modify_time))

        # ハンドルを閉じる
        handle.Close()

    # 他のプラットフォームではアクセス日時と更新日時を設定
    os.utime(output_file_path, (access_time, modify_time))











