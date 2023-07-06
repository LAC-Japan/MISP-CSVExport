# MISP CSVExport

MISP project: <http://www.misp-project.org/>

## 概要
この Python スクリプトはMISP (マルウェア情報共有プラットフォーム) からデータを検索し、結果を CSV ファイルにエクスポートします。 
検索パラメータは、スクリプトの実行時に引数として指定できます。

- 引数で指定されたパラメータに基づいて MISP からデータを検索します。
- 検索結果をCSVファイルにエクスポートします。

## ライセンス

このソフトウェアは BSD ライセンスに基づいてリリースされています。LICENSE.txt を参照してください。

## 動作確認済み環境

* Python 3.10
* PyMISP 2.4.172

## インストール
1. リポジトリのクローンを作成します。
```
git clone https://github.com/LAC-Japan/MISP-CSVExport
```
2. pip を使用して、必要な Python ライブラリをインストールします。
```
pip3 install pymisp
```
3. config.sampleを元にconfig.iniを作成します。
4. config.iniに MISP URL、MISP AUTHKEYを設定します。 
クライアント証明書による認証がMISPに設定されている場合、CERT FILE PATHとKEY FILE PATHも指定します。
5. 必要な引数を指定してスクリプトを実行します。

## 使用方法

```
python3 misp-csvexport.py --from <日付文字列> --to <日付文字列> -c category -t type -v value -T tag1 tag2
```
引数
- `--from YYYYMMDD(HHMMSS)` : このタイムスタンプ(UTC)以降のデータを検索します。
- `--to YYYYMMDD(HHMMSS)` : このタイムスタンプ(UTC)までのデータを検索します。
- `-c, --category category` : このカテゴリのデータを検索します。
- `-t, --type-attribute type` : このタイプのデータを検索します。
- `-v, --value value` : この値を持つデータを検索します。
- `-T, --event-tags tag1 tag2` : 指定したタグの内いずれかをイベントタグに持つデータを検索します。
- `--all` : MISP上で取得可能なすべてのデータをエクスポートします。
- `--out` : 出力するファイル名を指定します。指定しない場合はresult.csvというファイル名で出力されます。
- `--full-dump-event` : 検索にヒットしたアトリビュートに紐づくイベントの全データを出力します。指定しない場合は条件にマッチしたアトリビュートのみが出力されます。
