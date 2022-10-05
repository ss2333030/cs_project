document.addEventListener("DOMContentLoaded", () => {
  // Achieve autocompletion
  document.querySelector("#place").addEventListener("keyup", function () {
    // Get the place entered by the user and construct the URL
    const placeValue = document.querySelector("#place").value;
    const URL = `/places?place=${placeValue}`;

    // Request the backend server to get a list of candidate places
    fetch(URL)
      .then((response) => response.json())
      .then((data) => {
        const results = document.querySelector("#places");
        data["predictions"].forEach((e) => {
          const option = document.createElement("option");
          option.innerHTML = `${e["structured_formatting"]["main_text"]} ${e["structured_formatting"]["secondary_text"]}`;
          option.value = e["place_id"];
          results.appendChild(option);
        });
      })
      .catch((error) => {
        console.log("Error:", error);
      });
    return false;
  });

  document.querySelector("#add_place").addEventListener("click", async () => {
    const suburbPlaceId = document.querySelector("#suburb_place_id").value;
    const desiredPlacePlaceId = document.querySelector("#place").value;

    // Build the URL and then send a request to the server
    const URL = `/direction?suburb_place_id=${suburbPlaceId}&desired_place_place_id=${desiredPlacePlaceId}`;
    let response = await fetch(URL);

    if (response.status == 404) {  // If no directions were returned 
      const directions = document.querySelector("#directions");

      const row = document.createElement("tr");

      const endAddress = document.createElement("td");
      endAddress.innerHTML = document.querySelector("#place").value;

      const info = document.createElement("td");
      info.innerHTML = "Information not available";

      const removeButtonContainer = document.createElement("td");
      const removeButton = document.createElement("button");
      removeButton.setAttribute("type", "button");
      removeButton.setAttribute("class", "btn btn-outline-danger remove-button");
      removeButton.innerHTML = "Remove";

      removeButtonContainer.appendChild(removeButton);

      row.appendChild(endAddress);
      row.appendChild(info);
      row.appendChild(removeButtonContainer);

      directions.appendChild(row);
    } else {
      response = await response.json();

      const directions = document.querySelector("#directions");

      const newRow = document.createElement("tr");

      const endAddress = document.createElement("td");
      const info = document.createElement("td");
      const removeButtonContainer = document.createElement("td");

      endAddress.innerHTML = response.end_address;


      const distance = document.createElement("h6");
      const duration = document.createElement("h6");

      distance.innerHTML = response.distance.text;
      duration.innerHTML = response.duration.text;

      info.appendChild(distance);
      info.appendChild(duration);


      const removeButton = document.createElement("button");
      removeButton.type = "button";
      removeButton.className = "btn btn-outline-danger remove-button";
      removeButton.innerHTML = "Remove";

      removeButton.addEventListener("click", () => {
        const removeButtonContainer = removeButton.parentElement;
        const enclosingRow = removeButtonContainer.parentElement;
        enclosingRow.remove();
      })

      removeButtonContainer.appendChild(removeButton);

      newRow.appendChild(endAddress);
      newRow.appendChild(info);
      newRow.appendChild(removeButtonContainer);

      directions.appendChild(newRow);
    }
  })

});
