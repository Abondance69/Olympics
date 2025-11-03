# =======================================
# BUILD POUR PRODUCTION
# =======================================

Write-Host "🏗️  Build de l'application pour production..." -ForegroundColor Cyan

# Build Frontend
Write-Host "`n📦 Build du Frontend..." -ForegroundColor Yellow
Set-Location frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installation des dépendances frontend..." -ForegroundColor Yellow
    npm install
}

npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend build réussi!" -ForegroundColor Green
    Write-Host "📁 Fichiers disponibles dans: frontend\build\" -ForegroundColor Cyan
} else {
    Write-Host "❌ Erreur lors du build frontend" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..

# Vérifier le backend
Write-Host "`n🔍 Vérification du Backend..." -ForegroundColor Yellow
Set-Location backend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installation des dépendances backend..." -ForegroundColor Yellow
    npm install
}

Write-Host "✅ Backend prêt pour le déploiement!" -ForegroundColor Green

Set-Location ..

Write-Host "`n🎉 Build complet terminé!" -ForegroundColor Green
Write-Host "`nPrêt pour le déploiement:" -ForegroundColor Cyan
Write-Host "  - Frontend: frontend\build\" -ForegroundColor White
Write-Host "  - Backend: backend\" -ForegroundColor White
Write-Host "`nConsultez DEPLOYMENT.md pour les instructions de déploiement" -ForegroundColor Yellow
