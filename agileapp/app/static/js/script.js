// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("claimBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// CSS Grid height adjustments and resizing of boxes
function resizeGridItem(item) {
    const grid = document.getElementsByClassName('gallery')[0];
    const rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-gap'));
    const rowHeight = 10;
    const contentHeight = item.closest('.grid').querySelector('.grid_content').getBoundingClientRect().height;
    const rowSpan = Math.ceil((contentHeight + rowGap) / (rowHeight + rowGap));
    item.closest('.grid').style.gridRowEnd = 'span ' + rowSpan;
}

function resizeAllGridItems() {
    const allItems = document.getElementsByClassName('item');
    for (let x = 0; x < allItems.length; x++) {
        resizeGridItem(allItems[x].querySelector('img'));
    }
}

window.onload = resizeAllGridItems;
window.addEventListener('resize', resizeAllGridItems);

function handleImageError(itemId) {
    const itemElement = document.getElementById('item-' + itemId);
    if (itemElement) {
        itemElement.remove();
    }
}


