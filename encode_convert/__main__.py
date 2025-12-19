from .encode_convert import EncodeConvert
import argparse
import pandas as pd

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='エンコード変換ツール')
    parser.add_argument('directory', type=str, help='変換対象のディレクトリパス')
    parser.add_argument('to_encoding', type=str, help='変換先のエンコード名')
    parser.add_argument('--extensions', type=str, nargs='*', default=['.c', '.cpp', '.h'], help='対象とするファイル拡張子のリスト（デフォルト: .c, .cpp, .h）')
    parser.add_argument('--no-backup', action='store_true', help='バックアップを作成しない場合に指定')
    parser.add_argument('--output', type=str, default='.//', help='出力フォルダ:（デフォルト: カレントディレクトリ）')
    args = parser.parse_args()
    # 引数の取得
    directory = args.directory
    to_encoding = args.to_encoding
    extensions = args.extensions
    if args.no_backup:
        is_backup = False
    else:
        is_backup = True
    output_path = args.output
    # エンコード名を補正
    if to_encoding.lower() == 'utf8' or to_encoding.lower() == 'utf_8':
        to_encoding = 'utf-8'
    if to_encoding.lower() == 'utf16' or to_encoding.lower() == 'utf_16':
        to_encoding = 'utf-16'
    if to_encoding.lower() == 'shift-jis' or to_encoding.lower() == 'sjis':
        to_encoding = 'shift_jis'
    # エンコード変換実行
    encoder = EncodeConvert()
    encoder.batch_convert(directory, to_encoding, extensions, is_backup)

    # 変換結果を取得してcsv出力
    result_list = encoder.get_conversion_result()
    df = pd.DataFrame(result_list, columns=['変換したファイル'])
    file_path = output_path + '/conversion_list.csv'
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()