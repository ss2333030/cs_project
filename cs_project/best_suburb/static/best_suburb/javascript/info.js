document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#place").addEventListener('input', async function () {
        const placeValue = document.querySelector("#place").value;
        const URL = "/places?place=" + placeValue;

        fetch(URL).then(response => response.json()).then(data => {
            const results = document.querySelector("#places");
            data["predictions"].forEach(e => {
                const option = document.createElement("option");
                option.value = e["description"];
                results.append(option);
            });
        }).catch(error => {
            console.log('Error:', error);
        });
        return false;
    });
});