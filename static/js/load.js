var myVar;

function loader() {
  	document.getElementById("loader").style.display = "block";
  	document.getElementById("chart_page").style.display = "none";
    myVar = setTimeout(showPage, 120000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("chart_page").style.display = "block";
}