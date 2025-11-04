const mysql = require('mysql2/promise');
const { Pool } = require('pg');

let db;

if (process.env.DB_TYPE === 'postgres') {
  // Configuration PostgreSQL
  db = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 5432,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
  });

  console.log('✅ PostgreSQL pool créé');
} else {
  // Configuration MySQL/MariaDB par défaut
  db = mysql.createPool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
  });

  console.log('✅ MySQL/MariaDB pool créé');
}

// Test de connexion
async function testConnection() {
  try {
    if (process.env.DB_TYPE === 'postgres') {
      const client = await db.connect();
      console.log('✅ Connexion PostgreSQL établie');
      client.release();
    } else {
      const connection = await db.getConnection();
      console.log('✅ Connexion MySQL/MariaDB établie');
      connection.release();
    }
  } catch (error) {
    console.error('❌ Erreur de connexion à la base de données:', error.message);
  }
}

testConnection();

module.exports = db;
