$ErrorActionPreference = "Stop"

Write-Host "ACC Portal setup" -ForegroundColor Cyan
Write-Host ""

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found. Install Python 3.11+ from https://www.python.org/downloads/ and try again."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

$Python = ".venv\Scripts\python.exe"

Write-Host "Installing dependencies..." -ForegroundColor Yellow
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host "Generating .env..." -ForegroundColor Yellow
    $secret = & $Python -c "import secrets; print(secrets.token_urlsafe(48))"
    @"
SECRET_KEY=$secret
DATABASE_URL=sqlite:///acc_portal.db
SESSION_COOKIE_SECURE=0
"@ | Set-Content -Encoding UTF8 .env
}

Write-Host "Creating database tables..." -ForegroundColor Yellow
& $Python -m flask --app run.py init-db

Write-Host "Adding sample scholarships..." -ForegroundColor Yellow
& $Python seed_scholarships.py

Write-Host "" 
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Next: create the administrator account with:" -ForegroundColor Cyan
Write-Host "  .venv\Scripts\python.exe -m flask --app run.py create-admin"
Write-Host "Then start the portal with:" -ForegroundColor Cyan
Write-Host "  .venv\Scripts\python.exe run.py"
Write-Host "Open http://127.0.0.1:5000"
