from abc import ABC, abstractmethod
import pandas as pd

class AbstractConverter(ABC):
    """エンコード変換インターフェース
    """
    #
    # constructor/destructor
    #
    def __init__(self) -> None:
        """コンストラクタ
        """
        pass

    def __del__(self) -> None:
        """デストラクタ
        """
        pass

    #
    # abstract public methods
    #
    @abstractmethod
    def convert(self, file_path: str, to_encoding: str) -> bool:
        """エンコード変換処理

        Args:
            file_path (str): ファイルパス
            to_encoding (str): 変換先エンコード名
        Returns:
            bool: 変換結果(True:成功、False:失敗または変換なし)
        """
        pass

    @abstractmethod
    def convert_in_folder(self, folder_path: str, to_encoding: str) -> list:
        """エンコード変換一括処理

        Args:
            folder_path (str): フォルダパス
            to_encoding (str): 変換先エンコード名
        Returns:
            list: 変換ファイルリスト
        """
        pass

    @abstractmethod
    def restore(self, file_path: str) -> bool:
        """バックアップからの復元処理

        Args:
            file_path (str): ファイルパス
        Returns:
            bool: 復元結果(True:成功、False:失敗)
        """
        pass

    @abstractmethod
    def restore_in_folder(self, folder_path: str) -> list:
        """バックアップからの一括復元処理

        Args:
            folder_path (str): フォルダパス
        Returns:
            list: 復元ファイルリスト
        """
        pass
