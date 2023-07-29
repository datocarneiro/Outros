document.addEventListener("DOMContentLoaded", function () {
    const apiUrl = "http://192.168.0.166:5000/api/resultados";

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const resultadosDiv = document.getElementById("resultados");
            resultadosDiv.innerHTML = JSON.stringify(data.resultados, null, 2);
        })
        .catch(error => {
            console.error("Erro ao obter dados da API:", error);
            const resultadosDiv = document.getElementById("resultados");
            resultadosDiv.innerHTML = "Erro ao obter dados da API.";
        });
});