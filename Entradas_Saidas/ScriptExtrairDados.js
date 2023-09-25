/**
 * Download Nubank invoice data as CSV from web app.
 */

const chargeData = document.querySelectorAll(".charge");
const chargeArray = [...chargeData];

const chargeObj = chargeArray.map(charge => {
  const description = charge.querySelector(".description").textContent;
  const amount = charge.querySelector(".amount").textContent;
  const date = charge.querySelector(".date").textContent;
  return {
    date: date,
    description: description,
    amount: amount
  };
});

// Convert any array of objects into CSV string;
function arrayOfObjectsToCSV(array) {
  const data = array || null;
  if (data == null || !data.length) {
    return null;
  }

  const columnDelimiter = ";";
  const lineDelimiter = "\n";
  const keys = Object.keys(data[0]);

  let result = "";
  result += keys.join(columnDelimiter);
  result += lineDelimiter;

  data.forEach(function(item) {
    ctr = 0;
    keys.forEach(function(key) {
      if (ctr > 0) result += columnDelimiter;
      result += item[key];
      ctr++;
    });
    result += lineDelimiter;
	});
	
  return result;
}

const csvData = arrayOfObjectsToCSV(chargeObj);

//Create blob from string content and download as file;
function download(content, fileName, contentType) {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  const url = window.URL.createObjectURL(file);
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  setTimeout(function() {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(file);
  }, 100);
}

download(csvData, "chargeData.csv", "text/plain");