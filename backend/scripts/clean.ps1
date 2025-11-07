# =======================================
# NETTOYAGE DES FICHIERS TEMPORAIRES
# =======================================

Write-Host "🧹 Nettoyage des fichiers temporaires..." -ForegroundColor Cyan

# Nettoyer Backend
Write-Host "`n🔧 Nettoyage Backend..." -ForegroundColor Yellow
if (Test-Path "backend\node_modules") {
    Remove-Item -Recurse -Force "backend\node_modules"
    Write-Host "  ✅ node_modules supprimé" -ForegroundColor Green
}
if (Test-Path "backend\package-lock.json") {
    Remove-Item -Force "backend\package-lock.json"
    Write-Host "  ✅ package-lock.json supprimé" -ForegroundColor Green
}

# Nettoyer Frontend
Write-Host "`n🎨 Nettoyage Frontend..." -ForegroundColor Yellow
if (Test-Path "frontend\node_modules") {
    Remove-Item -Recurse -Force "frontend\node_modules"
    Write-Host "  ✅ node_modules supprimé" -ForegroundColor Green
}
if (Test-Path "frontend\build") {
    Remove-Item -Recurse -Force "frontend\build"
    Write-Host "  ✅ build supprimé" -ForegroundColor Green
}
if (Test-Path "frontend\package-lock.json") {
    Remove-Item -Force "frontend\package-lock.json"
    Write-Host "  ✅ package-lock.json supprimé" -ForegroundColor Green
}

Write-Host "`n✨ Nettoyage terminé!" -ForegroundColor Green
Write-Host "Pour réinstaller, exécutez: .\scripts\install.ps1" -ForegroundColor Yellow
