function create_tr(table_id) {
    let table_body = document.getElementById(table_id),
        first_tr = table_body.firstElementChild
    tr_clone = first_tr.cloneNode(true);
    table_body.append(tr_clone);
    clean_first_tr(table_body.firstElementChild);
}
function clean_first_tr(firstTr) {
    let children = firstTr.children;

    children = Array.isArray(children) ? children : Object.values(children);
    children.forEach(x => {
        if (x !== firstTr.lastElementChild) {
            x.firstElementChild.value = '';
        }
    });
}
function remove_tr(This) {
    if (This.closest('tbody').childElementCount == 1) {
        alert("You Don't have Permission to Delete This ?");
    } else {
        This.closest('tr').remove();
    }
}

// function updateResults() {
//     let distance = document.querySelector('#distance');
//     let rent = document.querySelector('#rent');
//     let crime_rate = document.querySelector('#crime_rate');

//     let response = await fetch('/search?distance=' + distance.value);
//     let shows = await response.json();
//     let html = '';
//     for (let id in shows) {
//         let title = shows[id].title.replace('<', '&lt;').replace('&', '&amp;');
//         html += '<li>' + title + '</li>';
//     }
//     document.querySelector('ul').innerHTML = html;

// }
