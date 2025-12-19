from abc import abstractmethod
import os

class BaseRestoreBackup:
    """バックアップ復元基底クラス
    """
    _extensions = []  # バックアップファイル拡張子
    _restore_result = []  # 復元結果を格納するリスト

    #
    # constructor/destructor
    #
    def __init__(self, extensions: list) -> None:
        """コンストラクタ

        Args:
            extensions (list): バックアップファイル拡張子リスト
        """
        self._extensions = extensions

    def __del__(self) -> None:
        """デストラクタ
        """
        pass
    
    #
    # public methods
    #
    def restore(self, backup_path: str) -> bool:
        """バックアップ復元処理

        Args:
            backup_path (str): バックアップ対象ディレクトリパス

        Returns:
            bool: 復元結果(True:成功、False:失敗)
        """
        # ファイルパスの存在確認
        if not os.path.exists(backup_path):
            print(f"指定されたバックアップパスが存在しません: {backup_path}")
            return False
        # ファイル拡張子の確認
        if not any(backup_path.endswith(ext) for ext in self._extensions):
            print(f"指定されたバックアップパスは有効な拡張子ではありません: {backup_path}")
            return False
        # バックアップ復元処理
        try:
            # バックアップファイルの拡張子を削除して元のファイル名を取得
            original_file_path = backup_path
            for ext in self._extensions:
                # 拡張子が一致する場合、ファイル名から拡張子を削除
                if original_file_path.endswith(ext):
                    original_file_path = original_file_path[:-len(ext)]
                    # 元のファイルが存在する場合は削除してからバックアップをリネーム
                    if os.path.exists(original_file_path):
                        os.remove(original_file_path)
                    os.rename(backup_path, original_file_path)
                    return True
        except Exception as e:
            print(f"バックアップ復元中にエラーが発生しました: {backup_path} - {e}")
            return False

    def batch_restore(self, root_path: str) -> None:
        """一括バックアップ復元処理

        Args:
            root_path (str): バックアップ対象ディレクトリパス
        """
        # ファイルパスの存在確認
        if not os.path.exists(root_path):
            print(f"指定されたバックアップルートパスが存在しません: {root_path}")
            return
        # ディレクトリ内のバックアップファイルを再帰的に検索して復元処理を実行
        for root, dirs, files in os.walk(root_path):
            for file in files:
                # 拡張子を確認して復元処理を実行
                if any(file.endswith(ext) for ext in self._extensions):
                    file_path = os.path.join(root, file)
                    if self.restore(file_path):
                        # 復元結果リストに追加
                        self._restore_result.append(file_path)
    
    def get_restore_result(self) -> list:
        """バックアップ復元結果取得

        Returns:
            list: バックアップ復元結果リスト
        """
        return self._restore_result
