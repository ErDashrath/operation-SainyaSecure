# Operation SainyaSecure - Folder Rename Script
# This script helps rename the project folder and update working directory

Write-Host "🚀 Operation SainyaSecure - Project Folder Rename Helper" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

$currentPath = "C:\Users\Dashrath\Desktop\Academic\Hackathons\tryyy001"
$newPath = "C:\Users\Dashrath\Desktop\Academic\Hackathons\operation-SainyaSecure"

Write-Host "Current folder: $currentPath" -ForegroundColor Yellow
Write-Host "New folder:     $newPath" -ForegroundColor Green

if (Test-Path $currentPath) {
    Write-Host "`n✅ Current project folder found!" -ForegroundColor Green
    
    if (Test-Path $newPath) {
        Write-Host "❌ Target folder already exists. Please remove it first or choose a different name." -ForegroundColor Red
        exit 1
    }
    
    try {
        Write-Host "`n🔄 Renaming folder..." -ForegroundColor Cyan
        Rename-Item -Path $currentPath -NewName "operation-SainyaSecure"
        Write-Host "✅ Folder successfully renamed!" -ForegroundColor Green
        
        Write-Host "`n📂 New project location: $newPath" -ForegroundColor Cyan
        Write-Host "🎯 You can now navigate to the new folder with:" -ForegroundColor Yellow
        Write-Host "   cd `"$newPath`"" -ForegroundColor White
        
        Write-Host "`n🚀 To continue working on Operation SainyaSecure:" -ForegroundColor Cyan
        Write-Host "   1. cd `"$newPath`"" -ForegroundColor White
        Write-Host "   2. python manage.py runserver" -ForegroundColor White
        
    } catch {
        Write-Host "❌ Error renaming folder: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "💡 Please make sure:" -ForegroundColor Yellow
        Write-Host "   - No files are open in the project" -ForegroundColor White
        Write-Host "   - No terminals are currently in the project directory" -ForegroundColor White
        Write-Host "   - VS Code is not open with the project" -ForegroundColor White
    }
} else {
    Write-Host "❌ Current project folder not found at: $currentPath" -ForegroundColor Red
    Write-Host "💡 Please check the path or run this script from the correct location." -ForegroundColor Yellow
}

Write-Host "`n🎉 Welcome to Operation SainyaSecure!" -ForegroundColor Green