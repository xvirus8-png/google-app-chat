Write-Host "Starting server for Big Pickle Chat..." -ForegroundColor Green
Write-Host "افتح المتصفح على: http://localhost:8080/big-pickle-chat.html" -ForegroundColor Yellow
Write-Host "اضغط Ctrl+C للإيقاف" -ForegroundColor Gray
Write-Host ""
python -m http.server 8080 --directory "C:\Users\medo2\Desktop\GOOGLE APP"
