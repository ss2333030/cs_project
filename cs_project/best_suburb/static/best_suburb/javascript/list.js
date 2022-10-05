document.addEventListener("DOMContentLoaded", async () => {
    function initialise() {
        document.querySelector("#uni_id").value = localStorage.getItem("uni_id");
        document.querySelector("#rent_min").value = localStorage.getItem("rent_min");
        document.querySelector("#rent_max").value = localStorage.getItem("rent_max");
        document.querySelector("#crime_rate_max").value = localStorage.getItem("crime_rate_max");
        document.querySelector("#distance_min").value = localStorage.getItem("distance_min");
        document.querySelector("#distance_max").value = localStorage.getItem("distance_max");
    }

    /**
     * Remove all suburbs on list page
     */
    function removeSuburbs() {
        let suburbs = document.querySelectorAll(".suburb");
        suburbs.forEach(suburb => suburb.remove());
    }

    /**
     * Display the suburbs in the variable suburbList.
     */
    function displaySuburbs() {
        // Clean up the list page
        removeSuburbs();

        let suburbs = document.querySelector("#suburbs");

        for (let i = 0; i < suburbList.length; i++) {
            let suburb = document.querySelector("#suburb_template").cloneNode(true);

            // Set properties
            suburb.removeAttribute("id");
            suburb.classList.add("suburb");
            suburb.hidden = false;
            suburb.href = `/info?suburb_id=${suburbList[i].id}&place_id=${suburbList[i].place_id}&uni_id=${localStorage.getItem("uni_id")}`;

            suburb.querySelector("#photo").src = suburbList[i].photo;
            suburb.querySelector("#photo").alt = suburbList[i].name;
            suburb.querySelector("#name").innerHTML = suburbList[i].name;
            suburb.querySelector("#state").insertBefore(document.createTextNode("VIC "), suburb.querySelector("#postcode"))
            suburb.querySelector("#postcode").innerHTML = suburbList[i].postcode;
            suburb.querySelector("#crime_rate").innerHTML = `Crime Rate:&nbsp;${suburbList[i].crime_rate}`;
            suburb.querySelector("#average_rent").innerHTML = `Average Rent: $${suburbList[i].average_rent}/per week`;

            // Add this suburb to the list suburbs on list page
            suburbs.append(suburb);
        }
    }


    /**
     * Get a list of suburbs from the server based on user input.
     */
    async function getSuburbs() {
        // Build the URL and then send a request to the server
        const URL = `/suburbs?uni_id=${localStorage.getItem("uni_id")}&rent_min=${localStorage.getItem("rent_min")}&rent_max=${localStorage.getItem("rent_max")}&distance_min=${localStorage.getItem("distance_min")}&distance_max=${localStorage.getItem("distance_max")}&crime_rate_max=${localStorage.getItem("crime_rate_max")}`;
        let response = await fetch(URL);

        if (response.status == 404) {  // If no suburbs were returned 
            // Remove the suburbs that are currently on list page
            removeSuburbs();

            // Build the error message
            const errorMessage = document.createElement("h5");
            errorMessage.innerHTML = "Sorry, we couldn't find what you're looking for.";
            document.querySelector("#suburbs").appendChild(errorMessage);
        } else if (response.status == 400) {   // If something went wrong
            // Remove all suburbs currently on list page
            removeSuburbs();

            // Build the error message
            const errorMessage = document.createElement("h5");
            errorMessage.innerHTML = "Sorry, something went wrong.";
            document.querySelector("#suburbs").appendChild(errorMessage);
        } else {  // Suburbs were retrieved successfully

            // Save the suburbs in a variable
            suburbList = await response.json();

            // Sort suburbs in suburbList by average rent
            suburbList.sort((a, b) => {
                if (a.average_rent < b.average_rent) {
                    return -1;
                }

                if (a.average_rent > b.average_rent) {
                    return 1;
                }
                return 0;
            });

            displaySuburbs();
        }
    }

    /**
     * Save user input in the browser for later use.
     */
    function saveParameters() {
        localStorage.setItem("uni_id", document.querySelector("#uni_id").value);
        localStorage.setItem("rent_min", document.querySelector("#rent_min").value);
        localStorage.setItem("rent_max", document.querySelector("#rent_max").value);
        localStorage.setItem("crime_rate_max", document.querySelector("#crime_rate_max").value);
        localStorage.setItem("distance_min", document.querySelector("#distance_min").value);
        localStorage.setItem("distance_max", document.querySelector("#distance_max").value);
    }



    let suburbList;   // Variable used to store the list of suburbs to be displayed on list page
    initialise();
    getSuburbs();

    document.querySelector("#the_form").addEventListener("submit", () => {
        saveParameters();
        initialise();
        getSuburbs();
        return false;
    });



    document.querySelector("#sort_by_rent_price").addEventListener("click", () => {
        // Remove the suburbs that are currently on list page
        removeSuburbs();

        // Sort suburbs in suburbList by average rent
        suburbList.sort((a, b) => {
            if (a.average_rent < b.average_rent) {
                return -1;
            }

            if (a.average_rent > b.average_rent) {
                return 1;
            }
            return 0;
        });

        // Display the suburbs in suburbList on list page
        displaySuburbs();
    });

    document.querySelector("#sort_by_distance").addEventListener("click", () => {
        // Remove the suburbs that are currently on list page
        removeSuburbs();

        // Sort suburbs in suburbList by distance
        suburbList.sort((a, b) => {
            if (a.distance < b.distance) {
                return -1;
            }

            if (a.distance > b.distance) {
                return 1;
            }
            return 0;
        });

        // Display the suburbs in suburbList on list page
        displaySuburbs();
    });

    document.querySelector("#sort_by_crime_rate").addEventListener("click", () => {
        // Remove the suburbs that are currently on list page
        removeSuburbs();

        // Sort suburbs in suburbList by crime rate
        suburbList.sort((a, b) => {
            if (a.crime_rate < b.crime_rate) {
                return -1;
            }

            if (a.crime_rate > b.crime_rate) {
                return 1;
            }
            return 0;
        });

        // Display the suburbs in suburbList on list page
        displaySuburbs();
    });


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