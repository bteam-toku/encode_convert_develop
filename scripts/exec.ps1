# 一つ上の親ディレクトリをカレントフォルダリに設定（環境に合わせて変更してください）
Set-Location -Path (Join-Path $PSScriptRoot "..")

# encode_convert実行
if ($args[0] -eq "convert") {
    if ($args.Count -lt 3) {
        Write-Host "Usage: .\encode_convert_dev.ps1 convert <path> <encode>"
        exit
    }
    $hostInputPath = (resolve-path $args[1]).Path
    $fullCurrentPath = Get-Location
    docker run -it --rm `
        -v "${hostInputPath}:/app/input" `
        -v "${fullCurrentPath}:/data" `
        ghcr.io/bteam-toku/encode_convert convert /app/input $args[2]
}
# restore_original実行
elseif ($args[0] -eq "restore") {
    if ($args.Count -lt 2) {
        Write-Host "Usage: .\encode_convert_dev.ps1 restore <path>"
        exit
    }
    $hostInputPath = (resolve-path $args[1]).Path
    $fullCurrentPath = Get-Location
    docker run -it --rm `
        -v "${hostInputPath}:/app/input" `
        -v "${fullCurrentPath}:/data" `
        ghcr.io/bteam-toku/encode_convert restore /app/input
}
# その他
else {
    Write-Host "Usage: .\encode_convert_dev.ps1 <convert|restore> <path> [<encode>]"
}