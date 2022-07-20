Write-Output "Starting application on http://localhost:9400. `nTo stop the application, close this window."
Start-Process "http://localhost:9400"
python.exe .\app.py