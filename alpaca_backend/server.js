const express = require("express");
const mysql = require("mysql2/promise");
const cors = require("cors");

const app = express();
const port = 3000;

// Configuration BDD
const dbConfig = {
  host: process.env.DB_HOST || "localhost",
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASS || "fabrice",
  database: process.env.DB_NAME || "trading_dashboard",
};

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("API Trading Dashboard OK");
});

app.get("/api/data/:symbol", async (req, res) => {
  const symbol = req.params.symbol;
  // On demande 50 points par source pour avoir un graphique équilibré
  const limitPerSource = 50;

  let connection;
  try {
    connection = await mysql.createConnection(dbConfig);

    // REQUÊTE MAGIQUE (UNION) :
    // Elle récupère les X derniers points d'Alpaca
    // ET les X derniers points de Binance
    // Puis elle mélange le tout et trie par date.
    const query = `
            (SELECT * FROM market_data WHERE symbol = ? AND source = 'Alpaca' ORDER BY timestamp DESC LIMIT ${limitPerSource})
            UNION
            (SELECT * FROM market_data WHERE symbol = ? AND source = 'Binance' ORDER BY timestamp DESC LIMIT ${limitPerSource})
            ORDER BY timestamp DESC;
        `;

    // On passe le symbole deux fois (une pour chaque SELECT)
    const [rows] = await connection.execute(query, [symbol, symbol]);

    res.status(200).json(rows);
  } catch (error) {
    console.error("Erreur SQL:", error);
    res.status(500).json({ error: "Erreur serveur BDD" });
  } finally {
    if (connection) await connection.end();
  }
});

app.listen(port, () => {
  console.log(`Serveur API démarré sur http://localhost:${port}`);
});
