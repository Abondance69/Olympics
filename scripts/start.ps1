# =======================================
# DÉMARRAGE COMPLET DE L'APPLICATION
# =======================================

Write-Host "🚀 Démarrage de l'application Olympics Analytics..." -ForegroundColor Cyan

# Vérifier si les dépendances sont installées
if (-not (Test-Path "backend\node_modules")) {
    Write-Host "❌ Backend node_modules non trouvé. Exécutez d'abord: .\scripts\install.ps1" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "❌ Frontend node_modules non trouvé. Exécutez d'abord: .\scripts\install.ps1" -ForegroundColor Red
    exit 1
}

# Fonction pour démarrer le backend
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD\backend
    npm start
}

Write-Host "✅ Backend démarré (Job ID: $($backendJob.Id))" -ForegroundColor Green
Write-Host "📡 API disponible sur: http://localhost:5000" -ForegroundColor Cyan

# Attendre 3 secondes pour que le backend démarre
Start-Sleep -Seconds 3

# Fonction pour démarrer le frontend
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD\frontend
    npm start
}

Write-Host "✅ Frontend démarré (Job ID: $($frontendJob.Id))" -ForegroundColor Green
Write-Host "🌐 Application disponible sur: http://localhost:3000" -ForegroundColor Cyan

Write-Host "`n📊 Les deux serveurs sont en cours d'exécution!" -ForegroundColor Green
Write-Host "Pour arrêter les serveurs, fermez cette fenêtre ou appuyez sur Ctrl+C" -ForegroundColor Yellow

# Attendre que l'utilisateur arrête
Write-Host "`nAppuyez sur une touche pour arrêter les serveurs..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Arrêter les jobs
Stop-Job $backendJob
Stop-Job $frontendJob
Remove-Job $backendJob
Remove-Job $frontendJob

Write-Host "`n🛑 Serveurs arrêtés" -ForegroundColor Red
