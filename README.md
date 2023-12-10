# jpg2jpg-bugfix-metadata

## リリースノート
2023/12/10 初版リリース。

## 説明
png2jpg改でAutomatic1111生成画像を変換した場合にプロンプト冒頭に"parameters: "が混入していた問題が発生していました。  
本ツールを使用することで変換済みの画像を一括で修正することができます。  
プロンプト冒頭に誤って入っていた"parameters: "のテキストが削除されます。
なお、png2jpg改のバグは2023/12/10に修正済みです。png2jpg改はpng2jpg-for-a1111-and-NAIに名称変更してGithubで公開しています。

## 前提
Python環境

## 準備
以下のライブラリを使用するため、入っていない場合はインストールします。
* PIL  
pip install pillow

* piexif  
pip install piexif

## 使い方
1. inputsフォルダに変換したいJPEG画像（png2jpg改でJPEG変換した画像）を入れます。※JPEG画像の拡張子は".jpg"である必要があります。
2. jpg2jpg-fix-metadata.batをダブルクリックします。
3. outputsフォルダに問題のプロンプトを修正したJPEG画像が保存されます。

## 設定変更等
処理完了後にコマンドラインを閉じないようにしたい場合はjpg2jpg-fix-metadata.bat内の@REM pauseのコメントアウトを外してください。
