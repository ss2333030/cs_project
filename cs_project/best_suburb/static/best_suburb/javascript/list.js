document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#id").addEventListener('change', () => {
        const uni_name = document.querySelector("#uni_name").value;
        const rent_min = document.querySelector("#rent_min").value;
        const rent_max = document.querySelector("#rent_max").value;
        const distance_min = document.querySelector("#distance_min").value;
        const distance_max = document.querySelector("#distance_max").value;
        const crime_rate_max = document.querySelector("#crime_rate_max").value;
        const URL = `/suburbs?uni_name=${uni_name}&rent_min=${rent_min}&rent_max=${rent_max}&distance_min=${distance_min}&distance_max=${distance_max}&crime_rate_max=${crime_rate_max}`;

        fetch(URL).then(response => response.json()).then(data => {
            const suburbList = document.querySelector("#suburb_list");

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