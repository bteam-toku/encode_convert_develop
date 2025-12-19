# encode_convert実行
if ($args[0] -eq "e") {
    if($args.Count -lt 3) {
        Write-Host "Usage: .\encode_convert_dev.ps1 e <path> <encode>"
        exit
    }
    $hostInputPath = (resolve-path $args[1]).Path
    $hostOutputPath = $PWD.Path
    docker run -it --rm `
    -v "${hostInputPath}:/input" `
    -v "${hostOutputPath}:/output" `
    encode_convert encode_convert /input $args[2] --output /output
}
# restore_original実行
elseif ($args[0] -eq "r") {
    if($args.Count -lt 2) {
        Write-Host "Usage: .\encode_convert_dev.ps1 r <path>"
        exit
    }
    $hostInputPath = (resolve-path $args[1]).Path
    $hostOutputPath = $PWD.Path
    docker run -it --rm `
    -v "${hostInputPath}:/input" `
    -v "${hostOutputPath}:/output" `
    encode_convert restore_orgfile /input --output /output
}
# その他
else {
    Write-Host "Usage: .\encode_convert_dev.ps1 <e|r> <path> [<encode>]"
    Write-Host "  e: encode_convert実行"
    Write-Host "  r: restore_original実行"
}