# 一つ上の親ディレクトリをカレントフォルダリに設定（環境に合わせて変更してください）
Set-Location -Path (Join-Path $PSScriptRoot "..")
# venvの有効化
.\scripts\env.ps1

# encode_convert実行
if ($args[0] -eq "convert") {
    if ($args.Count -lt 3) {
        Write-Host "Usage: .\encode_convert_dev.ps1 convert <path> <encode>"
        exit
    }
    py -m encode_convert $args[0] $args[1] $args[2]
}
# restore_original実行
elseif ($args[0] -eq "restore") {
    if ($args.Count -lt 2) {
        Write-Host "Usage: .\encode_convert_dev.ps1 restore <path>"
        exit
    }
    py -m encode_convert $args[0] $args[1]
}
# その他
else {
    Write-Host "Usage: .\encode_convert_dev.ps1 <convert|restore> <path> [<encode>]"
}