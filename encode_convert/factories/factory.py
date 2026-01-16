from encode_convert.interfaces import AbstractConverter
from encode_convert.config import Config
from typing import Optional
import importlib

class Factory:
    _instance : Optional[object] = None
    _cached_type : Optional[type] = None
    _config : Config = None

    #
    # コンストラクタ / デストラクタ
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
    # public methods
    #
    @classmethod
    def create(cls, adaptor_type_name: Optional[str] = None, config: Optional[Config] = None) -> AbstractConverter:
        """エンコード変換アダプターの生成

        Args:
            adaptor_type_name (Optional[str], optional): アダプターの型名. デフォルトはNone.
            config (Optional[Config], optional): 設定情報. デフォルトはNone.
        Returns:
            AbstractConverter: AbstractConverterオブジェクト
        """
        # 同じ型のアダプターがキャッシュされている場合はそれを返す（シングルトン）
        if cls._instance is not None and cls._cached_type == adaptor_type_name:
            return cls._instance
        
        # 設定情報が提供されていない場合は新たに生成する
        cls._config = config if config is not None else Config()

        if adaptor_type_name is None:
            # デフォルトで必要なモジュールをインポート
            from encode_convert.adaptors import DefaultConverterAdaptor
            from encode_convert.convert import DefaultEncodeConvert
            from encode_convert.restore import DefaultRestoreBackup
            # adaptor_type_nameが指定されていない場合はデフォルトのアダプターを使用
            converter = DefaultEncodeConvert(cls._config.convert_extension(), cls._config.backup_extension())
            restorer = DefaultRestoreBackup(cls._config.backup_extension())
            cls._instance = DefaultConverterAdaptor(converter, restorer)
            cls._cached_type = adaptor_type_name
        else:
            # 指定された型名からアダプタークラスを動的にインポートして生成
            module_path, class_name = adaptor_type_name.rsplit('.', 1)
            module = importlib.import_module(module_path)
            adaptor_class = getattr(module, class_name)
            cls._instance = adaptor_class()
            cls._cached_type = adaptor_type_name

        # 生成したアダプターを返す
        return cls._instance
