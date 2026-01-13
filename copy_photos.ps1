# Script copy anh tu dien thoai Xiaomi 12X sang E:\anh
# Moi lan copy 100 anh cho den khi het

$batchSize = 100
$destFolder = "E:\anh"

# Tao thu muc dich neu chua ton tai
if (!(Test-Path $destFolder)) {
    New-Item -ItemType Directory -Path $destFolder -Force
    Write-Host "Da tao thu muc: $destFolder" -ForegroundColor Green
}

# Khoi tao Shell COM object de truy cap thiet bi MTP
$shell = New-Object -ComObject Shell.Application

# Tim thu muc "This PC"
$thisPC = $shell.NameSpace(17)  # 17 = My Computer / This PC

# Tim dien thoai Xiaomi 12X
$phone = $null
foreach ($item in $thisPC.Items()) {
    if ($item.Name -like "*Xiaomi*") {
        $phone = $item
        Write-Host "Da tim thay dien thoai: $($item.Name)" -ForegroundColor Green
        break
    }
}

if ($phone -eq $null) {
    Write-Host "Khong tim thay dien thoai Xiaomi. Vui long kiem tra ket noi USB!" -ForegroundColor Red
    Write-Host "Cac thiet bi co san:" -ForegroundColor Yellow
    foreach ($item in $thisPC.Items()) {
        Write-Host "  - $($item.Name)"
    }
    Read-Host "Nhan Enter de thoat"
    exit
}

# Truy cap Bo nho trong - lay item dau tien trong dien thoai
$phoneFolder = $phone.GetFolder
if ($phoneFolder -eq $null) {
    Write-Host "Khong the truy cap dien thoai!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}

$internalStorage = $null
Write-Host "`nDang tim bo nho trong..." -ForegroundColor Yellow
foreach ($item in $phoneFolder.Items()) {
    Write-Host "  Tim thay: $($item.Name)" -ForegroundColor Gray
    $internalStorage = $item  # Lay item dau tien
    break
}

if ($internalStorage -eq $null) {
    Write-Host "Khong tim thay bo nho trong!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}
Write-Host "Su dung bo nho: $($internalStorage.Name)" -ForegroundColor Green

# Truy cap DCIM
$storageFolder = $internalStorage.GetFolder
if ($storageFolder -eq $null) {
    Write-Host "Khong the truy cap bo nho trong!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}

$dcimFolder = $null
Write-Host "`nDang tim thu muc DCIM..." -ForegroundColor Yellow
foreach ($item in $storageFolder.Items()) {
    if ($item.Name -eq "DCIM") {
        $dcimFolder = $item
        Write-Host "Da tim thay thu muc DCIM" -ForegroundColor Green
        break
    }
}

if ($dcimFolder -eq $null) {
    Write-Host "Khong tim thay thu muc DCIM!" -ForegroundColor Red
    Write-Host "Cac thu muc co san:" -ForegroundColor Yellow
    foreach ($item in $storageFolder.Items()) {
        Write-Host "  - $($item.Name)"
    }
    Read-Host "Nhan Enter de thoat"
    exit
}

# Truy cap Camera
$dcimNamespace = $dcimFolder.GetFolder
if ($dcimNamespace -eq $null) {
    Write-Host "Khong the truy cap DCIM!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}

$cameraFolder = $null
Write-Host "`nDang tim thu muc Camera..." -ForegroundColor Yellow
foreach ($item in $dcimNamespace.Items()) {
    if ($item.Name -eq "Camera") {
        $cameraFolder = $item
        Write-Host "Da tim thay thu muc Camera" -ForegroundColor Green
        break
    }
}

if ($cameraFolder -eq $null) {
    Write-Host "Khong tim thay thu muc Camera!" -ForegroundColor Red
    Write-Host "Cac thu muc co san:" -ForegroundColor Yellow
    foreach ($item in $dcimNamespace.Items()) {
        Write-Host "  - $($item.Name)"
    }
    Read-Host "Nhan Enter de thoat"
    exit
}

# Lay danh sach tat ca cac file anh/video
$cameraNamespace = $cameraFolder.GetFolder
if ($cameraNamespace -eq $null) {
    Write-Host "Khong the truy cap thu muc Camera!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}

$allItems = @()
Write-Host "`nDang lay danh sach file..." -ForegroundColor Yellow
foreach ($item in $cameraNamespace.Items()) {
    $allItems += $item
}

$totalFiles = $allItems.Count
Write-Host "Tong so file can copy: $totalFiles" -ForegroundColor Cyan

if ($totalFiles -eq 0) {
    Write-Host "Khong co file nao de copy!" -ForegroundColor Yellow
    Read-Host "Nhan Enter de thoat"
    exit
}

# Lay danh sach file da copy (de bo qua)
$existingFiles = @{}
if (Test-Path $destFolder) {
    Get-ChildItem $destFolder -File | ForEach-Object {
        $existingFiles[$_.Name] = $true
    }
    Write-Host "Da co $($existingFiles.Count) file trong thu muc dich" -ForegroundColor Gray
}

# Copy theo batch
$destNamespace = $shell.NameSpace($destFolder)
$copied = 0
$skipped = 0
$batchNumber = 1
$currentBatch = 0

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Bat dau copy..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

foreach ($item in $allItems) {
    $fileName = $item.Name
    
    # Kiem tra file da ton tai chua
    if ($existingFiles.ContainsKey($fileName)) {
        $skipped++
        continue
    }
    
    try {
        # Copy file
        # 0x10 = Khong hien dialog xac nhan ghi de
        $destNamespace.CopyHere($item, 0x10)
        
        $copied++
        $currentBatch++
        
        Write-Host "[$copied] Da copy: $fileName" -ForegroundColor White
        
        # Sau moi batch, tam dung de tranh qua tai
        if ($currentBatch -ge $batchSize) {
            Write-Host "`n>>> Da hoan thanh batch $batchNumber ($batchSize file)" -ForegroundColor Green
            Write-Host ">>> Doi 3 giay truoc khi tiep tuc...`n" -ForegroundColor Yellow
            Start-Sleep -Seconds 3
            $batchNumber++
            $currentBatch = 0
        }
    }
    catch {
        Write-Host "Loi khi copy $fileName : $_" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "HOAN THANH!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tong so file: $totalFiles" -ForegroundColor White
Write-Host "Da copy: $copied file" -ForegroundColor Green
Write-Host "Da bo qua (da ton tai): $skipped file" -ForegroundColor Yellow
Write-Host "Thu muc dich: $destFolder" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

Read-Host "Nhan Enter de thoat"
