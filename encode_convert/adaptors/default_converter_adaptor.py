from encode_convert.interfaces import AbstractConverter
from encode_convert.interfaces import AbstractEncodeConvert
from encode_convert.interfaces import AbstractRestoreBackup

class DefaultConverterAdaptor(AbstractConverter):
    """エンコード変換アダプタークラス
    """
    # protected attributes
    _converter: AbstractEncodeConvert
    _restorer: AbstractRestoreBackup

    #
    # constructor/destructor
    #
    def __init__(self, converter: AbstractEncodeConvert, restorer: AbstractRestoreBackup) -> None:
        """コンストラクタ
        """
        super().__init__()
        self._converter = converter
        self._restorer = restorer

    def __del__(self) -> None:
        """デストラクタ
        """
        super().__del__()

    #
    # public methods
    #
    def convert(self, file_path: str, to_encoding: str) -> bool:
        """エンコード変換処理

        Args:
            file_path (str): ファイルパス
            to_encoding (str): 変換先エンコード名
        Returns:
            bool: 変換結果(True:成功、False:失敗または変換なし)
        """
        return self._converter.convert(file_path, self._converter.correct_encoding_name(to_encoding))
    
    def convert_in_folder(self, folder_path: str, to_encoding: str) -> list:
        """エンコード変換一括処理

        Args:
            folder_path (str): フォルダパス
            to_encoding (str): 変換先エンコード名
        """
        return self._converter.convert_in_folder(folder_path, self._converter.correct_encoding_name(to_encoding))

    def restore(self, file_path: str) -> bool:
        """バックアップからの復元処理

        Args:
            file_path (str): ファイルパス
        Returns:
            bool: 復元結果(True:成功、False:失敗)
        """
        return self._restorer.restore(file_path)
    
    def restore_in_folder(self, folder_path: str) -> list:
        """バックアップからの一括復元処理

        Args:
            folder_path (str): フォルダパス
        """
        return self._restorer.restore_in_folder(folder_path)