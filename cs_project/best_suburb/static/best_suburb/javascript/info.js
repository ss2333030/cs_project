document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("").addEventListener('input', function () {
        const placeValue = document.querySelector("").value;
        const URL = "/places?place=" + placeValue;

        fetch(URL).then(response => response.json()).then(data => {
            const results = document.querySelector("#places");
            data["predictions"].forEach(e => {
                const option = document.createElement("option");
                option.innerHTML = `${e["structured_formatting"]["main_text"]} ${e["structured_formatting"]["secondary_text"]}`;
                option.value = e["place_id"];
                results.append(option);
            });
        }).catch(error => {
            console.log('Error:', error);
        });
        return false;
    });
});

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
});




