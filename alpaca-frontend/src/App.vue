<template>
  <div id="app">
    <h1>Arbitrage Monitor: AAPL vs BTC (Simulé)</h1>
    <div class="status">
      <span class="dot alpaca"></span> Alpaca (Actions)
      <span class="dot binance"></span> Binance (Crypto)
    </div>

    <div v-if="loading" class="loading">Chargement...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div class="chart-container" v-if="chartData.datasets.length > 0">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const loading = ref(true);
const error = ref(null);
const chartData = ref({ labels: [], datasets: [] });
let timer = null;

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: "index",
    intersect: false,
  },
  scales: {
    y: {
      ticks: { callback: (value) => `$${value}` },
    },
    x: { display: false }, // On cache les dates pour plus de clarté
  },
  plugins: {
    legend: { display: true },
  },
});

function formatTimestamp(timestamp) {
  return new Date(timestamp).toLocaleTimeString("fr-FR");
}

async function fetchData() {
  try {
    // On appelle notre nouvelle API (limitée à 50+50 points)
    const response = await axios.get("http://localhost:3000/api/data/AAPL");
    const rawData = response.data.reverse(); // On remet dans l'ordre chronologique

    // Axe X commun (tous les timestamps)
    const labels = rawData.map((d) => formatTimestamp(d.timestamp));

    // Préparation des données pour les deux lignes
    // Si la donnée n'est pas de la bonne source, on met 'null' pour laisser un trou
    const alpacaPrices = rawData.map((d) =>
      d.source === "Alpaca" ? d.price : null
    );
    const binancePrices = rawData.map((d) =>
      d.source === "Binance" ? d.price : null
    );

    chartData.value = {
      labels: labels,
      datasets: [
        {
          label: "Alpaca (Official)",
          borderColor: "#42b983", // Vert Vue.js
          backgroundColor: "#42b983",
          data: alpacaPrices,
          spanGaps: true, // Important : relie les points entre eux malgré les trous
          tension: 0.3,
          pointRadius: 2,
        },
        {
          label: "Binance (Simulé)",
          borderColor: "#ff9f43", // Orange Binance
          backgroundColor: "#ff9f43",
          data: binancePrices,
          spanGaps: true, // Important
          tension: 0.3,
          pointRadius: 2,
        },
      ],
    };
    loading.value = false;
  } catch (err) {
    console.error(err);
    error.value = "Erreur de connexion backend...";
  }
}

onMounted(() => {
  fetchData();
  timer = setInterval(fetchData, 2000); // Mise à jour rapide (2s)
});

onUnmounted(() => {
  clearInterval(timer);
});
</script>

<style>
#app {
  font-family: sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
}
.chart-container {
  position: relative;
  width: 95%;
  height: 500px;
  margin: 0 auto;
}
.status {
  margin-bottom: 20px;
}
.dot {
  height: 10px;
  width: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-left: 15px;
}
.dot.alpaca {
  background-color: #42b983;
}
.dot.binance {
  background-color: #ff9f43;
}
</style>
