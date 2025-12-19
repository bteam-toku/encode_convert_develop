.\env.ps1

# encode_convert実行
if ($args[0] -eq "e") {
    if($args.Count -lt 3) {
        Write-Host "Usage: .\encode_convert_dev.ps1 e <path> <encode>"
        exit
    }
    py -m encode_convert $args[1] $args[2]
}
# restore_original実行
elseif ($args[0] -eq "r") {
    if($args.Count -lt 2) {
        Write-Host "Usage: .\encode_convert_dev.ps1 r <path>"
        exit
    }
    py -m restore_orgfile $args[1]
}
# その他
else {
    Write-Host "Usage: .\encode_convert_dev.ps1 <e|r> <path> [<encode>]"
    Write-Host "  e: encode_convert実行"
    Write-Host "  r: restore_original実行"
}