document.addEventListener("DOMContentLoaded", async () => {
    const uniId = document.querySelector("#uni_id").value = localStorage.getItem("uni_id");
    const rentMin = document.querySelector("#rent_min").value = localStorage.getItem("rent_min");
    const rentMax = document.querySelector("#rent_max").value = localStorage.getItem("rent_max");
    const crimeRateMax = document.querySelector("#crime_rate_max").value = localStorage.getItem("crime_rate_max");
    const distanceMin = document.querySelector("#distance_min").value = localStorage.getItem("distance_min");
    const distanceMax = document.querySelector("#distance_max").value = localStorage.getItem("distance_max");

    let suburbList;

    function setSuburbs() {
        let suburbs = document.querySelector("#suburbs");

        for (let i = 0; i < suburbList.length; i++) {
            let suburb = document.querySelector("#suburb_template").cloneNode(true);
            suburb.removeAttribute("id");
            suburb.classList.add("suburb");
            suburb.hidden = false;
            suburb.href = `/info?suburb_id=${suburbList[i].id}&place_id${suburbList[i].place_id}`;
            suburb.querySelector("#image").src = suburbList[i].photo;
            suburb.querySelector("#image").alt = suburbList[i].name;
            suburb.querySelector("#name").innerHTML = suburbList[i].name;
            suburb.querySelector("#state").innerHTML = suburbList[i].state;
            // suburb.querySelector("#postcode").innerHTML = response[i].postcode;
            suburb.querySelector("#crime_rate").innerHTML = `Crime Rate:&nbsp;${suburbList[i].crime_rate}`;
            suburb.querySelector("#average_rent").innerHTML = `Average Rent: $${suburbList[i].average_rent}/per week`;

            suburbs.append(suburb);
        }
    }

    async function sendRequest() {
        const URL = `/suburbs?uni_id=${localStorage.getItem("uni_id")}&rent_min=${localStorage.getItem("rent_min")}&rent_max=${localStorage.getItem("rent_max")}&distance_min=${localStorage.getItem("distance_min")}&distance_max=${localStorage.getItem("distance_max")}&crime_rate_max=${localStorage.getItem("crime_rate_max")}`;
        let response = await fetch(URL);

        if (response.status == 404) {
            const errorMessage = document.createElement("h5");
            errorMessage.innerHTML = "Sorry, we couldn't find what you're looking for.";
            document.querySelector("#suburbs").appendChild(errorMessage);
        } else if (response.status == 400) {
            const errorMessage = document.createElement("h5");
            errorMessage.innerHTML = "Sorry, something went wrong.";
            document.querySelector("#suburbs").appendChild(errorMessage);
        } else {
            suburbList = await response.json();
            setSuburbs();
        }
    }

    function saveParameters() {
        localStorage.setItem("uni_id", document.querySelector("#uni_id").value);
        localStorage.setItem("rent_min", document.querySelector("#rent_min").value);
        localStorage.setItem("rent_max", document.querySelector("#rent_max").value);
        localStorage.setItem("crime_rate_max", document.querySelector("#crime_rate_max").value);
        localStorage.setItem("distance_min", document.querySelector("#distance_min").value);
        localStorage.setItem("distance_max", document.querySelector("#distance_max").value);
    }

    function removeSuburbs() {
        let suburbs = document.querySelectorAll(".suburb");
        suburbs.forEach(suburb => suburb.remove());
    }


    document.querySelector("#btnradio1").onclick = () => {
        removeSuburbs();
        suburbList.sort((a, b) => {
            if (a.average_rent < b.average_rent) {
                return -1;
            }

            if (a.average_rent > b.average_rent) {
                return 1;
            }
            return 0;
        });

        setSuburbs();
    }

    document.querySelector("#btnradio2").onclick = () => {
        removeSuburbs();
        suburbList.sort((a, b) => {
            if (a.distance < b.distance) {
                return -1;
            }

            if (a.distance > b.distance) {
                return 1;
            }
            return 0;
        });

        setSuburbs();
    }

    document.querySelector("#btnradio3").onclick = () => {
        removeSuburbs();
        suburbList.sort((a, b) => {
            if (a.crime_rate < b.crime_rate) {
                return -1;
            }

            if (a.crime_rate > b.crime_rate) {
                return 1;
            }
            return 0;
        });

        setSuburbs();
    }

    document.querySelector("#the_form").onclick = () => {
        saveParameters();
        sendRequest();
    };

    // input.addEventListener('input', async function () {
    //     let response = await fetch('/search?q=' + input.value);
    //     let shows = await response.json();
    //     let html = '';
    //     for (let id in shows) {
    //         let title = shows[id].title.replace('<', '&lt;').replace('&', '&amp;');
    //         html += '<li>' + title + '</li>';
    //     }
    //     document.querySelector('ul').innerHTML = html;
    // });


    // fetch(URL).then(response => response.json()).then(data => {
    //     // const suburbList = document.querySelector("#suburb_list");
    //     // let suburbs = [];

    //     // for (let i = 0; i < data.length; i++) {
    //     //     let suburb = suburbList.firstChild.cloneNode(true);
    //     //     suburb.href = `/info?name=${data[i].name}`;
    //     //     suburb.querySelector("#image").alt = data[i].name;
    //     //     suburb.querySelector("#name").innerHTML = data[i].name;
    //     //     suburb.querySelector("#postcode").innerHTML = data[i].postcode;
    //     //     suburb.querySelector("#crime_rate").innerHTML = `Crime Rate:&nbsp;${data[i].crime_rate}`;
    //     //     suburb.querySelector("#average_rent").innerHTML = `Average Rent: $${data[i].average_rent}/per week`;

    //     //     suburbs.push(suburb);
    //     // }

    //     // suburbList.replaceChildren(suburbs);
    //     console.log(data);
    // }).catch(error => {
    //     console.log('Error:', error);
    // });



    // document.querySelector("").addEventListener('change', () => {
    //     // const uni = document.querySelector("#uni").value;
    //     const uni_name = document.querySelector("#uni_name").value;
    //     const rent_min = document.querySelector("#rent_min").value;
    //     const rent_max = document.querySelector("#rent_max").value;
    //     const distance_min = document.querySelector("#distance_min").value;
    //     const distance_max = document.querySelector("#distance_max").value;
    //     const crime_rate_max = document.querySelector("#crime_rate_max").value;
    //     const URL = `/suburbs?uni_name=${uni_name}&rent_min=${rent_min}&rent_max=${rent_max}&distance_min=${distance_min}&distance_max=${distance_max}&crime_rate_max=${crime_rate_max}`;

    //     fetch(URL).then(response => response.json()).then(data => {
    //         const suburbList = document.querySelector("#suburb_list");
    //         let suburbs = [];

    //         for (let i = 0; i < data.length; i++) {
    //             let suburb = suburbList.firstChild.cloneNode(true);
    //             suburb.href = `/info?name=${data[i].name}`;
    //             suburb.querySelector("#image").alt = data[i].name;
    //             suburb.querySelector("#name").innerHTML = data[i].name;
    //             suburb.querySelector("#postcode").innerHTML = data[i].postcode;
    //             suburb.querySelector("#crime_rate").innerHTML = `Crime Rate:&nbsp;${data[i].crime_rate}`;
    //             suburb.querySelector("#average_rent").innerHTML = `Average Rent: $${data[i].average_rent}/per week`;

    //             suburbs.push(suburb);
    //         }

    //         suburbList.replaceChildren(suburbs);
    //     }).catch(error => {
    //         console.log('Error:', error);
    //     });
    //     return false;
    // });

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

});