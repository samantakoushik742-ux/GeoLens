# GeoLens - download location photos from Wikimedia Commons
# ------------------------------------------------------------
# Saves every gallery photo into assets\locations\ so the site
# shows them from your own repository.
#
# HOW TO RUN (once):
#   Right-click this file -> "Run with PowerShell"
#   or in a terminal in this folder:
#   powershell -ExecutionPolicy Bypass -File .\download-images.ps1
#
# Then commit the new assets\locations folder and push.

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $here "assets\locations"
New-Item -ItemType Directory -Force -Path $target | Out-Null

# Wikimedia asks scripts to identify themselves.
$headers = @{ "User-Agent" = "GeoLensImageFetcher/1.0 (student project; https://violetbyte.github.io/GeoLens-Disaster-Prediction-System/)" }

$images = @(
    @('flood-kolkata-3.jpg', 'Torrential rain lash Kolkata, many areas waterlogged- Kolkata-West Bengal-September 2021-IMG 20210915 205028.jpg'),
    @('flood-sundarbans-1.jpg', 'Dense Mangrove Forest of the Sundarban Tiger Reserve during High Tide, West Bengal, India 02.jpg'),
    @('flood-sundarbans-2.jpg', 'Tropical Cyclone Amphan approaching the coasts of India and Bangladesh - May 20th, 2020 (49915736373).jpg'),
    @('flood-sundarbans-3.jpg', 'Riverlets of sundarbans.jpg'),
    @('flood-malda-1.jpg', 'Manikchak Ghat.jpg'),
    @('flood-malda-2.jpg', 'Mahananda River.jpg'),
    @('flood-malda-3.jpg', 'Ganga river (2).jpg'),
    @('flood-murshidabad-1.jpg', 'Bhagirathi River Behind Hazarduari Palace Murshidabad.JPG'),
    @('flood-murshidabad-2.jpg', 'Highway on Farakka Barrage, a barrage in Farakka, West Bengal 16.jpg'),
    @('flood-murshidabad-3.jpg', 'Bridge over Bhagirathi river - Murshidabad.jpg'),
    @('flood-howrah-1.jpg', 'Damodar River at Raspur, Howrah 11.jpg'),
    @('flood-howrah-2.jpg', 'Bagnan bridge on Rupnarayan river, Howrah, in West Bengal, India, photographed by Yogabrata Chakraborty, November 9, 2022.jpg'),
    @('flood-howrah-3.jpg', 'Ghat on Hooghly River in Howrah.jpg'),
    @('drought-bankura-2.jpg', 'Koro Hill.jpg'),
    @('drought-bankura-3.jpg', 'Mukutmanipur dam.jpg'),
    @('drought-purulia-1.jpg', 'Ajodhya Purulia 21.jpg'),
    @('drought-purulia-2.jpg', 'Purulia hills.jpg'),
    @('drought-purulia-3.jpg', 'Ajodhya Hill Water reservoir at Purulia.jpg'),
    @('drought-jhargram-1.jpg', 'View from top of a hill...in belpahari,jhargram ,west bengal.jpg'),
    @('drought-jhargram-2.jpg', 'A click from a top of the hill....at belpahari,jhargram.jpg'),
    @('drought-jhargram-3.jpg', 'Jhargram Kanak Durga Mandir.jpg'),
    @('drought-birbhum-1.jpg', 'Khoai at Shantiniketan in Birbhum district 12.jpg'),
    @('drought-birbhum-2.jpg', 'Khoai at Shantiniketan in Birbhum district 04.jpg'),
    @('drought-birbhum-3.jpg', 'River Kopai - Ballavpur - Birbhum 2014-06-29 5627.JPG'),
    @('drought-paschim-medinipur-1.jpg', 'Ravines on the banks of Shilabati.jpg'),
    @('drought-paschim-medinipur-2.jpg', 'Gangani canyon at Garbeta, Paschim Medinipur 01.jpg'),
    @('drought-paschim-medinipur-3.jpg', 'Shilabati river or Shilai river near Gangani at Garbeta 01.jpg'),
    @('vegetation-sundarbans-1.jpg', 'Sundarbans.jpg'),
    @('vegetation-sundarbans-2.jpg', 'Sundarban Mangrove forest 02.jpg'),
    @('vegetation-sundarbans-3.jpg', 'Mangrove Forest.jpg'),
    @('vegetation-dooars-1.jpg', 'Tea garden in dooars.jpg'),
    @('vegetation-dooars-2.jpg', 'Jaldapara National park Forest.jpg'),
    @('vegetation-dooars-3.jpg', 'Road through Lataguri Forest.jpg'),
    @('vegetation-darjeeling-1.jpg', 'Tea plantation Darjeeling.JPG'),
    @('vegetation-darjeeling-2.jpg', '2024-03-14 Forest seen from Senchal Road 1.jpg'),
    @('vegetation-darjeeling-3.jpg', 'Darjeeling, India, Trees in the forest near Darjeeling.jpg'),
    @('vegetation-jalpaiguri-1.jpg', 'Gairkata Tea Estate 06.jpg'),
    @('vegetation-jalpaiguri-2.jpg', 'Chapramari Wildlife Sanctuary.jpg'),
    @('vegetation-jalpaiguri-3.jpg', 'Gajoldoba Barrage on Teesta river in Gajoldoba 04.jpg'),
    @('vegetation-purulia-1.jpg', 'Palash flowers in Purulia district.jpg'),
    @('vegetation-purulia-2.jpg', 'Sal forests in Purulia, West Bengal, India.jpg'),
    @('vegetation-purulia-3.jpg', 'Ajodhya Pahar Pathway at Purulia.jpg')
)

$ok = 0; $failed = @()
foreach ($item in $images) {
    $name = $item[0]; $file = $item[1]
    $out = Join-Path $target $name
    if (Test-Path $out) { Write-Host "skip  $name (already saved)"; $ok++; continue }
    $base = "https://commons.wikimedia.org/wiki/Special:FilePath/" + [Uri]::EscapeDataString($file.Replace(" ", "_"))
    # Try a 1280px copy, then 960px, then the original file. Retry each a few times.
    $urls = @("$base`?width=1280", "$base`?width=960", $base)
    $saved = $false
    foreach ($url in $urls) {
        for ($try = 1; $try -le 3 -and -not $saved; $try++) {
            try {
                Invoke-WebRequest -Uri $url -Headers $headers -OutFile $out -UseBasicParsing -MaximumRedirection 5
                if ((Get-Item $out).Length -gt 5000) { $saved = $true } else { Remove-Item $out }
            } catch {
                if (Test-Path $out) { Remove-Item $out }
                Start-Sleep -Seconds (2 * $try)
            }
        }
        if ($saved) { break }
    }
    if ($saved) {
        Write-Host "saved $name" -ForegroundColor Green
        $ok++
    } else {
        Write-Host "FAIL  $name  <-  $file" -ForegroundColor Red
        $failed += "$name  <-  $file"
    }
    Start-Sleep -Milliseconds 800
}

Write-Host ""
Write-Host "Done: $ok of $($images.Count) photos saved to assets\locations" -ForegroundColor Cyan
if ($failed.Count -gt 0) {
    Write-Host "These could not be downloaded (the site will keep loading them from Wikimedia):" -ForegroundColor Yellow
    $failed | ForEach-Object { Write-Host "  $_" }
}
Read-Host "Press Enter to close"
