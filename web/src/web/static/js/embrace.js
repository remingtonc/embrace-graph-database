function setupDropdown(dropdownId) {
    let btnNode = document.getElementById(dropdownId);
    let selection = document.getElementById(dropdownId + "Dropdown");
    btnNode.onclick = function() {
        selection.classList.toggle("active");
    }
}
