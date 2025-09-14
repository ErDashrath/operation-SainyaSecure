@echo off
echo 🚀 Operation SainyaSecure - Project Folder Rename Helper
echo ============================================================

set "currentPath=C:\Users\Dashrath\Desktop\Academic\Hackathons\tryyy001"
set "newPath=C:\Users\Dashrath\Desktop\Academic\Hackathons\operation-SainyaSecure"

echo Current folder: %currentPath%
echo New folder:     %newPath%
echo.

if exist "%currentPath%" (
    echo ✅ Current project folder found!
    
    if exist "%newPath%" (
        echo ❌ Target folder already exists. Please remove it first.
        pause
        exit /b 1
    )
    
    echo 🔄 Renaming folder...
    ren "%currentPath%" "operation-SainyaSecure"
    
    if exist "%newPath%" (
        echo ✅ Folder successfully renamed!
        echo.
        echo 📂 New project location: %newPath%
        echo 🎯 You can now navigate to the new folder with:
        echo    cd "%newPath%"
        echo.
        echo 🚀 To continue working on Operation SainyaSecure:
        echo    1. cd "%newPath%"
        echo    2. python manage.py runserver
        echo.
        echo 🎉 Welcome to Operation SainyaSecure!
    ) else (
        echo ❌ Error renaming folder. Please try manually.
        echo 💡 Make sure no files are open and no terminals are in the directory.
    )
) else (
    echo ❌ Current project folder not found at: %currentPath%
    echo 💡 Please check the path.
)

echo.
pause