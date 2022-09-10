// var search = document.getElementById("search")

// search.addEventListener("click", function (e) {
//     window.location.href = "listpage.html"
// })

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#advanced-search").onclick = function () {
        document.querySelector("#uni_name_advanced").value = document.querySelector("#uni_name").value;
    };

});