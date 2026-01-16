from encode_convert.config import Config
from encode_convert.factories import Factory
from encode_convert.interfaces import AbstractConverter
import argparse
import pandas as pd
import os

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='エンコード変換ツール')
    subparser = parser.add_subparsers(dest='mode', required=True, help='モード選択')
    # convertモードを追加
    convert_parser = subparser.add_parser('convert', help='エンコード変換モード')
    convert_parser.add_argument('target_path', type=str, help='変換対象のパス')
    convert_parser.add_argument('to_encoding', type=str, help='変換先エンコード名')
    convert_parser.add_argument('--output_path', type=str, default='', help='出力フォルダ:（設定ファイルのoutput_path）')
    # restoreモードを追加
    restore_parser = subparser.add_parser('restore', help='バックアップからの復元モード')
    restore_parser.add_argument('target_path', type=str, help='変換対象のパス')
    restore_parser.add_argument('--output_path', type=str, default='', help='出力フォルダ:（設定ファイルのoutput_path）')
    args = parser.parse_args()
    # 引数の取得
    mode = args.mode
    target_path = args.target_path
    to_encoding = getattr(args, 'to_encoding', None)
    output_path = args.output_path

    # エンコード変換実行
    config=Config()
    converter : AbstractConverter = Factory.create(config=config)
    output_path = args.output_path if args.output_path else config.output_path()

    match mode:
        # エンコード変換モード
        case 'convert':
            # エンコード名の正規化
            if os.path.isfile(target_path):
                # ファイル単体のエンコード変換
                converter.convert(target_path, to_encoding)
            elif os.path.isdir(target_path):
                # フォルダ内のエンコード変換
                result_list = converter.convert_in_folder(target_path, to_encoding)
                # 結果をCSVに保存
                df = pd.DataFrame(result_list, columns=['変換したファイル'])
                df.to_csv(os.path.join(output_path, 'converted_list.csv'), index=False, encoding='utf-8-sig')
            else:
                print('不正なパスです。target_path:', target_path)
                return

        # バックアップからの復元モード    
        case 'restore':
            if os.path.isfile(target_path):
                # ファイル単体のバックアップからの復元
                converter.restore(target_path)
            elif os.path.isdir(target_path):
                # バックアップからの復元
                result_list = converter.restore_in_folder(target_path)
                # 結果をCSVに保存
                df = pd.DataFrame(result_list, columns=['復元したファイル'])
                df.to_csv(os.path.join(output_path, 'restored_list.csv'), index=False, encoding='utf-8-sig')
            else:
                print('不正なパスです。target_path:', target_path)
                return
            
        # その他は不正なモードとしてエラーメッセージを表示
        case _:
            print('モードが正しくありません。 (Usage : convert|restore)')
            return

if __name__ == "__main__":
    main()