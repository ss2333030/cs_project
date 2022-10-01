document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#the_form").onclick = () => {
    localStorage.setItem("uni_id", document.querySelector("#uni_id").value);
    localStorage.setItem("rent_min", document.querySelector("#rent_min").value);
    localStorage.setItem("rent_max", document.querySelector("#rent_max").value);
    localStorage.setItem("crime_rate_max", document.querySelector("#crime_rate_max").value);
    localStorage.setItem("distance_min", document.querySelector("#distance_min").value);
    localStorage.setItem("distance_max", document.querySelector("#distance_max").value);
  };

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })
});
