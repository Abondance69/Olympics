# =======================================
# SCRIPTS UTILES - OLYMPICS WEBAPP
# =======================================

# Installation complète
Write-Host "📦 Installation des dépendances..." -ForegroundColor Cyan

# Backend
Write-Host "`n🔧 Installation Backend..." -ForegroundColor Yellow
Set-Location backend
npm install

# Frontend
Write-Host "`n🎨 Installation Frontend..." -ForegroundColor Yellow
Set-Location ..\frontend
npm install

Set-Location ..
Write-Host "`n✅ Installation terminée!" -ForegroundColor Green
