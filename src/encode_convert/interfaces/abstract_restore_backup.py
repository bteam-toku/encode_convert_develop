from abc import ABC, abstractmethod
import os

class AbstractRestoreBackup(ABC):
    """バックアップ復元抽象クラス
    """
    #
    # constructor/destructor
    #
    def __init__(self, backup_extensions: str) -> None:
        """コンストラクタ

        Args:
            backup_extensions (str): バックアップファイル拡張子
        """
        pass

    def __del__(self) -> None:
        """デストラクタ
        """
        pass
    
    #
    # public methods
    #
    @abstractmethod
    def restore(self, file_path: str) -> bool:
        """バックアップからの復元処理

        Args:
            file_path (str): 復元対象ファイルパス
        Returns:
            bool: 復元結果(True:成功、False:失敗)
        """
        pass

    @abstractmethod
    def restore_in_folder(self, folder_path: str) -> list:
        """一括バックアップ復元処理

        Args:
            folder_path (str): 復元対象ディレクトリパス
        Returns:
            list: 復元ファイルリスト
        """
        pass
    
    @abstractmethod
    def get_restored_result(self) -> list:
        """復元ファイルリスト取得

        Returns:
            list: 復元ファイルリスト
        """
        pass
