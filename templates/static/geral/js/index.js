function selectNavLinkToActive(navLinkTextContent) {
    const navLinks = document.querySelectorAll('.nav-link');
    let currentNavLinkActive = document.querySelector('.nav-link.active');

    currentNavLinkActive.classList.remove('active');
    currentNavLinkActive.removeAttribute('aria-current');

    navLinks.forEach(navLink => {
        if(navLink.textContent == navLinkTextContent) {
            navLink.classList.add('active');
            navLink.setAttribute('aria-current', 'page');
        }
    })
}

function selectDropDownToActive(dropDownItemTextContent) {
    const dropDownItems = document.querySelectorAll('.dropdown-item');
    let currentDropDownItemActive = document.querySelector('.dropdown-item.active');

    if(currentDropDownItemActive != undefined){
        currentDropDownItemActive.classList.remove('active');
        currentDropDownItemActive.removeAttribute('aria-current');
    }

    dropDownItems.forEach(dropDownItem => {
        if(dropDownItem.textContent == dropDownItemTextContent) {
            dropDownItem.classList.add('active');
            dropDownItem.setAttribute('aria-current', 'page');
        }
    });
}
