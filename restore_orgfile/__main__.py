from .restore_orgfile import RestoreOrgFile
import pandas as pd
import argparse

def main():
    """orgfile復元ツールメイン処理
    """
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='orgfile復元ツール')
    parser.add_argument('directory', type=str, help='復元対象のディレクトリパス')
    parser.add_argument('--output', type=str, default='.//', help='出力フォルダ:（デフォルト: カレントディレクトリ）')
    args = parser.parse_args()
    # 引数の取得
    directory = args.directory
    output_path = args.output

    # 元ファイル復元実行
    restorer = RestoreOrgFile()
    restorer.batch_restore(directory)

    # 復元結果を取得してcsv出力
    result_list = restorer.get_restore_result()
    df = pd.DataFrame(result_list, columns=['復元したファイル'])
    file_path = output_path + '/restore_list.csv'
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()