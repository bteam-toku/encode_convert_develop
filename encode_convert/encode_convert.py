from .base_encode_convert import BaseEncodeConvert        
import chardet
import codecs

class EncodeConvert(BaseEncodeConvert):
    """エンコード変換クラス
    """

    #
    # constructor/destructor
    #
    def __init__(self) -> None:
        """コンストラクタ
        """
        super().__init__()

    def __del__(self) -> None:
        """デストラクタ
        """
        super().__del__()

    #
    # protected methods
    def _get_encoding_name(self, file_path: str) -> str:
        """エンコード名取得

        Args:
            file_path (str): ファイルパス

        Returns:
            str: エンコード名
        """
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding_name = result['encoding'] if result['encoding'] else 'unknown'
        return encoding_name
    
    def _is_valid_encoding(self, encoding_name: str) -> bool:
        """有効なエンコード名か判定

        Args:
            encoding_name (str): エンコード名

        Returns:
            bool: 判定結果(True:有効、False:無効)
        """
        try:
            codecs.lookup(encoding_name)
            return True
        except LookupError:
            return False
    
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
