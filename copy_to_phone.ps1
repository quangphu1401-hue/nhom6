# Script copy anh tu E:\anh vao dien thoai Xiaomi 13 Ultra
# Moi lan copy 50 anh cho den khi het

$batchSize = 50
$sourceFolder = "E:\anh"

# Kiem tra thu muc nguon
if (!(Test-Path $sourceFolder)) {
    Write-Host "Thu muc nguon khong ton tai: $sourceFolder" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}

# Khoi tao Shell COM object de truy cap thiet bi MTP
$shell = New-Object -ComObject Shell.Application

# Tim thu muc "This PC"
$thisPC = $shell.NameSpace(17)  # 17 = My Computer / This PC

# Tim dien thoai Xiaomi 13 Ultra
$phone = $null
foreach ($item in $thisPC.Items()) {
    if ($item.Name -like "*Xiaomi 13 Ultra*" -or $item.Name -like "*13 Ultra*") {
        $phone = $item
        Write-Host "Da tim thay dien thoai: $($item.Name)" -ForegroundColor Green
        break
    }
}

if ($phone -eq $null) {
    Write-Host "Khong tim thay dien thoai Xiaomi 13 Ultra. Vui long kiem tra ket noi USB!" -ForegroundColor Red
    Write-Host "Cac thiet bi co san:" -ForegroundColor Yellow
    foreach ($item in $thisPC.Items()) {
        Write-Host "  - $($item.Name)"
    }
    Read-Host "Nhan Enter de thoat"
    exit
}

# Truy cap Bo nho trong dung chung
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
    # Tim "Bo nho trong dung chung" hoac tuong tu
    if ($item.Name -match "dung chung|shared|internal") {
        $internalStorage = $item
        break
    }
}

# Neu khong tim thay, lay item dau tien
if ($internalStorage -eq $null) {
    foreach ($item in $phoneFolder.Items()) {
        $internalStorage = $item
        break
    }
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

# Lay namespace cua thu muc Camera (dich)
$cameraNamespace = $cameraFolder.GetFolder
if ($cameraNamespace -eq $null) {
    Write-Host "Khong the truy cap thu muc Camera!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}

# Lay danh sach file da co trong Camera (de bo qua)
$existingFiles = @{}
Write-Host "`nDang kiem tra file da co trong dien thoai..." -ForegroundColor Yellow
foreach ($item in $cameraNamespace.Items()) {
    $existingFiles[$item.Name] = $true
}
Write-Host "Da co $($existingFiles.Count) file trong thu muc Camera" -ForegroundColor Gray

# Lay danh sach file can copy tu E:\anh
$sourceFiles = Get-ChildItem $sourceFolder -File
$totalFiles = $sourceFiles.Count
Write-Host "Tong so file can copy: $totalFiles" -ForegroundColor Cyan

if ($totalFiles -eq 0) {
    Write-Host "Khong co file nao de copy!" -ForegroundColor Yellow
    Read-Host "Nhan Enter de thoat"
    exit
}

# Copy theo batch
$sourceNamespace = $shell.NameSpace($sourceFolder)
$copied = 0
$skipped = 0
$batchNumber = 1
$currentBatch = 0

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Bat dau copy vao dien thoai..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

foreach ($file in $sourceFiles) {
    $fileName = $file.Name
    
    # Kiem tra file da ton tai chua
    if ($existingFiles.ContainsKey($fileName)) {
        $skipped++
        continue
    }
    
    try {
        # Lay item tu source folder
        $sourceItem = $sourceNamespace.ParseName($fileName)
        
        if ($sourceItem -ne $null) {
            # Copy file vao dien thoai
            # 0x10 = Khong hien dialog xac nhan ghi de
            $cameraNamespace.CopyHere($sourceItem, 0x10)
            
            # Them file vao danh sach da copy de tranh copy lai
            $existingFiles[$fileName] = $true
            
            $copied++
            $currentBatch++
            
            Write-Host "[$copied] Da copy: $fileName" -ForegroundColor White
            
            # Sau moi batch, tam dung de tranh qua tai
            if ($currentBatch -ge $batchSize) {
                Write-Host "`n>>> Da hoan thanh batch $batchNumber ($batchSize file)" -ForegroundColor Green
                Write-Host ">>> Doi 30 giay truoc khi tiep tuc...`n" -ForegroundColor Yellow
                Start-Sleep -Seconds 30
                $batchNumber++
                $currentBatch = 0
                
                # Refresh lai danh sach file trong dien thoai sau moi batch
                Write-Host "Dang cap nhat danh sach file trong dien thoai..." -ForegroundColor Gray
                foreach ($item in $cameraNamespace.Items()) {
                    if (-not $existingFiles.ContainsKey($item.Name)) {
                        $existingFiles[$item.Name] = $true
                    }
                }
            }
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
Write-Host "Thu muc dich: Xiaomi 13 Ultra/DCIM/Camera" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

Read-Host "Nhan Enter de thoat"
