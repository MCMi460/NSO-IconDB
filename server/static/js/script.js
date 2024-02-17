let searchBox;

function load() {
    searchBox = document.getElementById("searchBox");

    var url = window.location.pathname.split('/');
    var i = 0;
    for (option of searchBox.options) {
        if (option.id == url[url.length - 1]) {
            searchBox.selectedIndex = i;
            break;
        }
        i++;
    }
}

function search() {
    var target = searchBox.options[searchBox.selectedIndex];
    window.location.href = target.id == "none" ? "/" : `/key/${target.id}`;
}
