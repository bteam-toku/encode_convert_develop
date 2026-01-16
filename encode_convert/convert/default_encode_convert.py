from .base_encode_convert import BaseEncodeConvert

class DefaultEncodeConvert(BaseEncodeConvert):
    """エンコード変換クラス
    """
    def correct_encoding_name(self, encoding_name: str) -> str:
        """エンコード名の補正処理

        Args:
            encoding_name (str): エンコード名
        Returns:
            str: 補正後のエンコード名
        """
        # 入力が空の場合はデフォルトとしてutf-8を返す
        if not encoding_name:
            return 'utf-8'
        
        # 入力エンコード名の正規化
        normalized_name = encoding_name.lower().replace('-', '').replace('_', '').replace(' ', '').replace('/', '')

        # 補正マッピング
        correct_name = encoding_name
        match (normalized_name):
            case 'utf8' | 'utf':
                correct_name = 'utf-8'
            case 'utf8sig' | 'utf8bom' | 'utfwithbom':
                correct_name = 'utf-8-sig'
            case 'utf16':
                correct_name = 'utf-16'
            case 'shiftjis' | 'sjis' | 'cp932':
                correct_name = 'shift_jis'
            case _:
                # normalized_nameに ['sig', 'bom'] が含まれている場合の補正
                if 'sig' in normalized_name or 'bom' in normalized_name:
                    if 'utf8' in normalized_name:
                        correct_name = 'utf-8-sig'
                    elif 'utf16' in normalized_name:
                        correct_name = 'utf-16-sig'
        # 補正後のエンコード名を返す
        return correct_name
