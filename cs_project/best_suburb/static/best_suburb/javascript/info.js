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

        // const URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Paris&types=geocode&key=AIzaSyDRsqK_7w_eBkmNJZUczRnyC9jJx5gj5xQ";
        // fetch(URL).then(response => response.json()).then(data => {
        //     console.log(data);
        //     document.querySelector('ul').innerHTML = shows;
        //     console.log("hello");
        //     const results = documents.querySelector("#results");
        //     data["predictions"].forEach(e => {
        //         const option = document.createElement("option");
        //         option.value = e["description"];
        //         results.append(li);
        //     })
        // }).catch(error => {
        //     console.log('Error:', error);
        // });
        // return false;

    });
});