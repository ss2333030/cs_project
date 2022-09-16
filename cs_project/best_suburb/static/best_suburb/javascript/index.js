// // var search = document.getElementById("search")

// // search.addEventListener("click", function (e) {
// //     window.location.href = "listpage.html"
// // })

// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelectorAll(".search").forEach(button => {
//         button.addEventListener("click", () => {
//             const uni_name = document.createElement("input");
//             uni_name.type = "hidden";
//             uni_name.name = "uni_name";
//             uni_name.value = document.querySelector("#uni_name").value;

//             const rent_min = document.createElement("input");
//             rent_min.type = "hidden";
//             rent_min.name = "rent_min";
//             rent_min.value = document.querySelector("#rent_min").value;



//             const rent_max = document.createElement("input");
//             rent_max.type = "hidden";
//             rent_max.name = "rent_max";
//             rent_max.value = document.querySelector("#rent_max").value;

//             const distance_min = document.createElement("input");
//             distance_min.type = "hidden";
//             distance_min.name = "distance_min";
//             distance_min.value = document.querySelector("#distance_min").value;

//             const distance_max = document.createElement("input");
//             distance_max.type = "hidden";
//             distance_max.name = "distance_max";
//             distance_max.value = document.querySelector("#distance_max").value;

//             const crime_rate_max = document.createElement("input");
//             crime_rate_max.type = "hidden";
//             crime_rate_max.name = "crime_rate_max";
//             crime_rate_max.value = document.querySelector("#crime_rate_max").value;

//             document.querySelectorAll("form").forEach(form => {
//                 form.append(uni_name);
//                 form.append(rent_min);
//                 form.append(rent_max);
//                 form.append(distance_min);
//                 form.append(distance_max);
//                 form.append(crime_rate_max);
//             });
//         });
//     })
//     // document.querySelector("#advanced-search").onclick = function () {
//     //     document.querySelector("#uni_name_advanced").value = document.querySelector("#uni_name").value;
//     // };

// });