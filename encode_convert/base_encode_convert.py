from abc import abstractmethod
import os
import shutil

class BaseEncodeConvert:
    """エンコード変換基底クラス
    """
    _conversion_result = [] # 変換結果を格納するリスト


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
    # protected methods
    #
    @abstractmethod
    def _get_encoding_name(self, file_path: str) -> str:
        """エンコード名取得

        Args:
            file_path (str): ファイルパス

        Returns:
            str: エンコード名
        """
        pass

    @abstractmethod
    def _is_valid_encoding(self, encoding_name: str) -> bool:
        """有効なエンコード名か判定

        Args:
            encoding_name (str): エンコード名

        Returns:
            bool: 判定結果(True:有効、False:無効)
        """
        pass

    @abstractmethod
    def _convert_encoding(self, file_path: str, from_encoding: str, to_encoding: str) -> bool:
        """エンコード変換処理

        Args:
            file_path (str): ファイルパス
            from_encoding (str): 変換元エンコード名
            to_encoding (str): 変換先エンコード名

        Returns:
            bool: 変換結果(True:成功、False:失敗)
        """
        pass


    #
    # public methods
    #
    def convert(self, file_path: str, to_encoding: str, backup: bool=True) -> bool:
        """エンコード変換処理

        Args:
            file_path (str): ファイルパス
            to_encoding (str): 変換先エンコード名
            backup (bool): バックアップ作成フラグ(True:作成、False:作成しない)
        Returns:
            bool: 変換結果(True:成功、False:失敗または変換なし)
        """
        # file_pathの存在確認
        if not os.path.isfile(file_path):
            return False
        # 変換先エンコード名の妥当性確認
        if not self._is_valid_encoding(to_encoding):
            return False

        # 指定ファイルのエンコード名取得
        from_encoding = self._get_encoding_name(file_path)
        if not self._is_valid_encoding(from_encoding):
            return False

        # エンコード変換処理
        if from_encoding is None or from_encoding.lower() != to_encoding.lower():
            # バックアップ作成
            if backup:
                shutil.copy2(file_path, file_path + '.org')
            # エンコード変換実行
            result = self._convert_encoding(file_path, from_encoding, to_encoding)
        else:
            result = False
        # 変換結果を返却
        return result
    
    def batch_convert(self, root_path: list, to_encoding: str, extensions:list, backup:bool=True) -> None:
        """エンコード変換一括処理

        Args:
            root_path (list): ルートパスリスト
            to_encoding (str): 変換先エンコード名
            extensions (list): 対象拡張子リスト（例：['.txt', '.csv']）
            backup (bool): バックアップ作成フラグ(True:作成、False:作成しない)

        Returns:
            None
        """
        # 変換結果リスト初期化
        self._conversion_result.clear()
        
        # 変換先エンコード名の妥当性確認
        if not self._is_valid_encoding(to_encoding):
            return
        
        # ルートパス毎に処理実行
        for root, dirs, files in os.walk(root_path):
            for file in files:
                # 拡張子確認
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    # エンコード変換実行
                    if self.convert(file_path, to_encoding, backup):
                        self._conversion_result.append(file_path)
    
    def get_conversion_result(self) -> list:
        """変換結果取得

        Returns:
            list: 変換結果リスト
        """
        return self._conversion_result
