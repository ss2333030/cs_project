document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("").addEventListener('change', () => {
        // const uni = document.querySelector("#uni").value;
        const uni_name = document.querySelector("#uni_name").value;
        const rent_min = document.querySelector("#rent_min").value;
        const rent_max = document.querySelector("#rent_max").value;
        const distance_min = document.querySelector("#distance_min").value;
        const distance_max = document.querySelector("#distance_max").value;
        const crime_rate_max = document.querySelector("#crime_rate_max").value;
        const URL = `/suburbs?uni_name=${uni_name}&rent_min=${rent_min}&rent_max=${rent_max}&distance_min=${distance_min}&distance_max=${distance_max}&crime_rate_max=${crime_rate_max}`;

        fetch(URL).then(response => response.json()).then(data => {
            const suburbList = document.querySelector("#suburb_list");
            let suburbs = [];

            for (let i = 0; i < data.length; i++) {
                let suburb = suburbList.firstChild.cloneNode(true);
                suburb.href = `/info?name=${data[i].name}`;
                suburb.querySelector("#image").alt = data[i].name;
                suburb.querySelector("#name").innerHTML = data[i].name;
                suburb.querySelector("#postcode").innerHTML = data[i].postcode;
                suburb.querySelector("#crime_rate").innerHTML = `Crime Rate:&nbsp;${data[i].crime_rate}`;
                suburb.querySelector("#average_rent").innerHTML = `Average Rent: $${data[i].average_rent}/per week`;

                suburbs.push(suburb);
            }

            suburbList.replaceChildren(suburbs);
        }).catch(error => {
            console.log('Error:', error);
        });
        return false;
    });

        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
           })

});