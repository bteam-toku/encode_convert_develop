from .base_restore_backup import BaseRestoreBackup

class RestoreOrgFile(BaseRestoreBackup):
    """元ファイル復元クラス
    """

    #
    # constructor/destructor
    #
    def __init__(self) -> None:
        """コンストラクタ

        Args:
            extensions (list): バックアップファイル拡張子リスト
        """
        super().__init__(extensions=['.org'])

    def __del__(self) -> None:
        """デストラクタ
        """
        super().__del__()
    