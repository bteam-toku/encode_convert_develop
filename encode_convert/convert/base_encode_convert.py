from abc import abstractmethod
import chardet
import codecs
import os
import shutil

class BaseEncodeConvert:
    """エンコード変換基底クラス
    """
    # protected attributes
    _convert_extensions : list = []  # 変換対象拡張子リスト
    _backup_extensions : str = None  # バックアップファイル拡張子
    _converted_file_list : list = []  # 変換ファイルリスト

    #
    # constructor/destructor
    #
    def __init__(self, convert_extensions: list, backup_extensions: str) -> None:
        """コンストラクタ
        """
        self._convert_extensions = convert_extensions
        self._backup_extensions = backup_extensions

    def __del__(self) -> None:
        """デストラクタ
        """
        pass

    #
    # public methods
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
        # ファイルが存在しない、または拡張子が一致しない、変換先エンコード名が無効な場合は変換しない
        if  not os.path.isfile(file_path) or not os.path.exists(file_path) or \
            not any(file_path.endswith(ext) for ext in self._convert_extensions) or \
            not self._is_valid_encoding(to_encoding):
            return False

        # 指定ファイルのエンコード名取得
        from_encoding = self._get_encoding_name(file_path)
        if not self._is_valid_encoding(from_encoding):
            return False

        # エンコード変換処理
        if from_encoding is None or from_encoding.lower() != to_encoding.lower():
            # バックアップ作成
            if self._backup_extensions:
                shutil.copy2(file_path, file_path + self._backup_extensions)
            # エンコード変換実行
            result = self._convert_encoding(file_path, from_encoding, to_encoding)
        else:
            result = False
        # 変換結果を返却
        return result
    
    @abstractmethod
    def convert_in_folder(self, folder_path: str, to_encoding: str) -> list:
        """エンコード変換一括処理

        Args:
            folder_path (str): フォルダパス
            to_encoding (str): 変換先エンコード名

        Returns:
            list: 変換ファイルリスト
        """
        # 初期化
        self._converted_file_list = []
        
        # 変換先エンコード名の妥当性確認
        if  not os.path.isdir(folder_path) or not os.path.exists(folder_path) or \
            not self._is_valid_encoding(to_encoding):
            return self._converted_file_list
        
        # フォルダパス毎に処理実行
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 拡張子が変換対象リストに含まれている場合のみ処理実行
                if any(file.endswith(ext) for ext in self._convert_extensions):
                    file_path = os.path.join(root, file)
                    # エンコード変換実行し、成功した場合は結果リストに追加
                    if self.convert(file_path, to_encoding):
                        self._converted_file_list.append(file_path)

        # 返却値として変換結果リストを返す
        return self._converted_file_list
    
    @abstractmethod
    def get_converted_result(self) -> list:
        """変換結果取得

        Returns:
            list: 変換結果リスト
        """
        return self._converted_file_list
    
    #
    # protected methods
    #
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
        try:
            with open(file_path, 'r', encoding=from_encoding, errors='ignore') as f:
                content = f.read()
            with open(file_path, 'w', encoding=to_encoding, errors='ignore') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error during encoding conversion: {file_path} ({from_encoding} -> {to_encoding} - {e})")
            return False

    @abstractmethod
    def _get_encoding_name(self, file_path: str) -> str:
        """エンコード名取得

        本メソッドではchardetを使用してエンコードを検出し、エンコード名の検出に失敗した場合は'unknown'を返す.

        Args:
            file_path (str): ファイルパス
        Returns:
            str: エンコード名
        """
        try:
            # chardetを使用してエンコード名を検出
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding_name = result['encoding'] if result['encoding'] else 'unknown'
        except:
            # エンコード名取得失敗
            encoding_name = 'unknown'
        # 返却値としてエンコード名を返す
        return encoding_name


    @abstractmethod
    def _is_valid_encoding(self, encoding_name: str) -> bool:
        """有効なエンコード名か判定

        本メソッドではcodecs.lookupを使用してエンコード名の妥当性を確認する。

        Args:
            encoding_name (str): エンコード名

        Returns:
            bool: 判定結果(True:有効、False:無効)
        """
        try:
            # エンコード名の妥当性確認。無効であればLookupError例外が発生する。
            codecs.lookup(encoding_name)
            return True
        except LookupError:
            return False




