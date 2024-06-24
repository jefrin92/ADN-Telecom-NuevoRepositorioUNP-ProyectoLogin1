document.addEventListener("DOMContentLoaded", function () {
  var ctxEquipos = document.getElementById("chartEquipos").getContext("2d");
  var ctxRecomendaciones = document
    .getElementById("chartRecomendaciones")
    .getContext("2d");
    var ctxAprobacion = document.getElementById('aprobacionChart').getContext('2d');

  // Datos para la gráfica de distribución de equipos
  var equiposData = JSON.parse(
    document.getElementById("equiposData").textContent
  );
  var labelsEquipos = equiposData.map(function (item) {
    return item.Equipo;
  });
  var dataEquipos = equiposData.map(function (item) {
    return item.Cantidad;
  });

  new Chart(ctxEquipos, {
    type: "bar",
    data: {
      labels: labelsEquipos,
      datasets: [
        {
          label: "Cantidad",
          data: dataEquipos,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  // Datos para la gráfica de número de recomendaciones
  var numRecomendaciones = JSON.parse(
    document.getElementById("recomendacionesData").textContent
  );
  var totalComponents = 27;
  var restantes = Math.max(totalComponents - numRecomendaciones, 0); // Asegurarse de que no haya valores negativos

  new Chart(ctxRecomendaciones, {
    type: "doughnut",
    data: {
      labels: ["Recomendaciones", "Restantes"],
      datasets: [
        {
          data: [numRecomendaciones, restantes],
          backgroundColor: [
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: ["rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      cutout: "70%",
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              return context.raw + " de " + totalComponents;
            },
          },
        },
      },
    },
  });
// Datos para la gráfica de índice de aprobación
var approvalData = JSON.parse(document.getElementById("approvalIndices").textContent);
var labelsAprobacion = approvalData.map(function (item) {
  return item.MODELO;
});
var dataAprobacion = approvalData.map(function (item) {
  return item.approval_Index;
});

new Chart(ctxAprobacion, {
  type: "bar",
  data: {
    labels: labelsAprobacion,
    datasets: [
      {
        label: "Índice de Aprobación (%)",
        data: dataAprobacion,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  },
});
});