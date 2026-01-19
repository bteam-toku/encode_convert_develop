from encode_convert.interfaces import AbstractRestoreBackup
import os

class BaseRestoreBackup(AbstractRestoreBackup):
    """バックアップ復元基底クラス
    """
    # protected attributes
    _backup_extensions : str = None  # バックアップファイル拡張子
    _restored_file_list : list = []  # 復元ファイルリスト

    #
    # constructor/destructor
    #
    def __init__(self, backup_extensions: str) -> None:
        """コンストラクタ

        Args:
            backup_extensions (str): バックアップファイル拡張子
        """
        self._backup_extensions = backup_extensions

    def __del__(self) -> None:
        """デストラクタ
        """
        pass
    
    #
    # public methods
    #
    def restore(self, file_path: str) -> bool:
        """バックアップからの復元処理

        Args:
            file_path (str): 復元対象ファイルパス
        Returns:
            bool: 復元結果(True:成功、False:失敗)
        """
        # バックアップ拡張子が設定されていない、ファイルが存在しない、または拡張子が一致しない場合は復元しない
        if  not self._backup_extensions or \
            not os.path.isfile(file_path) or not os.path.exists(file_path) or \
            not file_path.endswith(self._backup_extensions):
            return False

        # バックアップ復元処理
        try:
            # 拡張子が一致する場合、ファイル名から拡張子を削除
            original_file_path = file_path[:-len(self._backup_extensions)]
            # 元のファイルが存在する場合は削除してからバックアップをリネーム
            if os.path.exists(original_file_path):
                os.remove(original_file_path)
            os.rename(file_path, original_file_path)
            return True
        except Exception as e:
            print(f"バックアップ復元中にエラーが発生しました: {file_path} - {e}")
            return False

    def restore_in_folder(self, folder_path: str) -> list:
        """一括バックアップ復元処理

        Args:
            folder_path (str): 復元対象ディレクトリパス
        Returns:
            list: 復元ファイルリスト
        """
        # 初期化
        self._restored_file_list = []

        # バックアップ拡張子が設定されていない、またはディレクトリが存在しない場合は復元しない
        if  not self._backup_extensions or \
            not os.path.isdir(folder_path) or not os.path.exists(folder_path):
            return self._restored_file_list
        
        # ディレクトリ内のバックアップファイルを再帰的に検索して復元処理を実行
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 拡張子を確認して復元処理を実行
                if file.endswith(self._backup_extensions):
                    file_path = os.path.join(root, file)
                    # 復元処理を実行して、成功した場合は結果リストに追加
                    if self.restore(file_path):
                        self._restored_file_list.append(file_path)

        # 返却値として復元結果リストを返す
        return self._restored_file_list
    
    def get_restored_result(self) -> list:
        """復元ファイルリスト取得

        Returns:
            list: 復元ファイルリスト
        """
        return self._restored_file_list
