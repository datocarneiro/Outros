document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const processButton = document.getElementById("processButton");
    const resultDiv = document.getElementById("result");
    const tableContainer = document.getElementById("tableContainer");
    const downloadLink = document.getElementById("downloadLink");

    processButton.addEventListener("click", function () {
        const file = fileInput.files[0];
        if (!file) {
            alert("Por favor, selecione um arquivo Excel.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        fetch("/processar", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    const table = createTable(data.result);
                    tableContainer.innerHTML = "";
                    tableContainer.appendChild(table);

                    resultDiv.style.display = "block";
                    downloadLink.href = data.download_link;
                    downloadLink.style.display = "block";
                } else {
                    alert("Ocorreu um erro ao processar o arquivo.");
                }
            })
            .catch((error) => {
                console.error(error);
                alert("Ocorreu um erro ao processar o arquivo.");
            });
    });

    function createTable(data) {
        const table = document.createElement("table");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");

        const headerRow = document.createElement("tr");
        const headers = ["ID", "CEP Modificado"];

        headers.forEach((headerText) => {
            const th = document.createElement("th");
            th.textContent = headerText;
            headerRow.appendChild(th);
        });

        thead.appendChild(headerRow);
        table.appendChild(thead);

        data.forEach((row) => {
            const tr = document.createElement("tr");
            Object.values(row).forEach((cellValue) => {
                const td = document.createElement("td");
                td.textContent = cellValue;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });

        table.appendChild(tbody);
        return table;
    }
});
