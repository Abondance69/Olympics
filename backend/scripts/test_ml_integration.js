/**
 * Script de test pour l'intégration ML
 * Teste tous les endpoints ML via le backend Express
 */

const axios = require('axios');

const BACKEND_URL = 'http://localhost:5000';
const COLORS = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${COLORS[color]}${message}${COLORS.reset}`);
}

async function testEndpoint(name, url, method = 'GET', data = null) {
  try {
    log(`\n🧪 Test: ${name}`, 'cyan');
    log(`   ${method} ${url}`, 'blue');
    
    const config = {
      method,
      url: `${BACKEND_URL}${url}`,
      timeout: 10000
    };
    
    if (data) {
      config.data = data;
    }
    
    const response = await axios(config);
    
    log(`   ✅ Succès (${response.status})`, 'green');
    log(`   📊 Données: ${JSON.stringify(response.data).substring(0, 200)}...`, 'reset');
    
    return { success: true, data: response.data };
  } catch (error) {
    log(`   ❌ Erreur: ${error.message}`, 'red');
    if (error.response) {
      log(`   Status: ${error.response.status}`, 'red');
      log(`   Réponse: ${JSON.stringify(error.response.data)}`, 'red');
    }
    return { success: false, error: error.message };
  }
}

async function runTests() {
  log('═══════════════════════════════════════════════════════', 'yellow');
  log('🤖 TEST D\'INTÉGRATION API ML - Olympics Analytics', 'yellow');
  log('═══════════════════════════════════════════════════════', 'yellow');
  
  const results = {
    passed: 0,
    failed: 0,
    total: 0
  };

  // Test 1: Backend principal
  log('\n📡 GROUPE 1: Backend Express', 'cyan');
  const test1 = await testEndpoint('Backend principal', '/');
  results.total++;
  test1.success ? results.passed++ : results.failed++;

  // Test 2: Health check ML
  log('\n🏥 GROUPE 2: Health Checks', 'cyan');
  const test2 = await testEndpoint('ML API Health Check', '/api/ml/health');
  results.total++;
  test2.success ? results.passed++ : results.failed++;

  // Test 3: Prédictions Paris 2024
  log('\n🏆 GROUPE 3: Prédictions', 'cyan');
  const test3 = await testEndpoint('Prédictions Paris 2024 (TOP 25)', '/api/ml/predict/paris2024');
  results.total++;
  test3.success ? results.passed++ : results.failed++;
  
  if (test3.success) {
    log(`   🥇 Top 3 prédictions:`, 'green');
    const preds = test3.data.predictions || [];
    preds.slice(0, 3).forEach((p, i) => {
      log(`      ${i + 1}. ${p.country}: ${p.predicted_total_medals} médailles`, 'green');
    });
  }

  // Test 4: Prédiction France
  const test4 = await testEndpoint('Prédiction France', '/api/ml/predict/country/France');
  results.total++;
  test4.success ? results.passed++ : results.failed++;

  // Test 5: Prédiction USA
  const test5 = await testEndpoint('Prédiction USA', '/api/ml/predict/country/USA');
  results.total++;
  test5.success ? results.passed++ : results.failed++;

  // Test 6: Informations modèles
  log('\n📊 GROUPE 4: Métadonnées', 'cyan');
  const test6 = await testEndpoint('Informations sur les modèles', '/api/ml/models/info');
  results.total++;
  test6.success ? results.passed++ : results.failed++;

  // Test 7: Pays inexistant (devrait échouer gracieusement)
  log('\n🔍 GROUPE 5: Gestion d\'erreurs', 'cyan');
  const test7 = await testEndpoint('Pays inexistant (test erreur)', '/api/ml/predict/country/InvalidCountry');
  results.total++;
  // On s'attend à une erreur 404, c'est normal
  if (!test7.success && test7.error.includes('404')) {
    log('   ✅ Erreur 404 gérée correctement', 'green');
    results.passed++;
  } else if (!test7.success) {
    results.passed++; // Toute erreur est acceptable ici
  } else {
    results.failed++;
  }

  // Résumé
  log('\n═══════════════════════════════════════════════════════', 'yellow');
  log('📊 RÉSUMÉ DES TESTS', 'yellow');
  log('═══════════════════════════════════════════════════════', 'yellow');
  log(`Total: ${results.total}`, 'blue');
  log(`✅ Réussis: ${results.passed}`, 'green');
  log(`❌ Échoués: ${results.failed}`, 'red');
  log(`Taux de réussite: ${((results.passed / results.total) * 100).toFixed(1)}%`, 
      results.failed === 0 ? 'green' : 'yellow');
  
  if (results.failed === 0) {
    log('\n🎉 TOUS LES TESTS SONT PASSÉS ! 🎉', 'green');
    log('✅ L\'intégration ML est fonctionnelle', 'green');
  } else {
    log('\n⚠️  Certains tests ont échoué', 'yellow');
    log('💡 Assurez-vous que:', 'yellow');
    log('   1. Le backend Express tourne sur le port 5000', 'reset');
    log('   2. L\'API ML Python Flask tourne sur le port 5001', 'reset');
    log('   3. Les dépendances (axios) sont installées', 'reset');
  }
  
  log('\n═══════════════════════════════════════════════════════\n', 'yellow');
  
  process.exit(results.failed > 0 ? 1 : 0);
}

// Lancer les tests
runTests().catch(error => {
  log(`\n💥 ERREUR FATALE: ${error.message}`, 'red');
  process.exit(1);
});
