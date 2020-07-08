
var JEWEL_MODAL = "#jewel-modal";

/*
** jewelModalClose:
**
** Close the modal popup, whenever the background or
** the exit cross is pressed.
*/

function jewelModalClose()
{
    let modal = document.querySelector(JEWEL_MODAL);

    modal.classList.remove("is-active");
}

/*
** setupModalCloseListener:
**
** Prepare event listener to left the modal.
** Used on background and exit cross of the modal.
*/

function setupModalCloseListener()
{
    let modal = document.querySelector(JEWEL_MODAL);
    let background;
    let exitButton;

    background = modal.querySelector(".modal-background");
    exitButton = modal.querySelector(".modal-close");

    background.addEventListener("click", jewelModalClose);
    exitButton.addEventListener("click", jewelModalClose);
}

/*
** jewelModalListener:
**
** Click listener for jewel image. Use the url of the clicked
** image and display it within the modal.
*/

function jewelModalListener(event)
{
    let modalElement = document.querySelector(JEWEL_MODAL);
    let modalImage = modalElement.querySelector("img");
    let imgUrlToDisplay;

    // Remove the size part '.s-1234' of an img src
    imgUrlToDisplay = event.target.getAttribute("src");
    imgUrlToDisplay = imgUrlToDisplay.split(".");
    imgUrlToDisplay.pop();
    imgUrlToDisplay = imgUrlToDisplay.join(".");

    //Display image
    modalImage.onload = function(){ 
        modalElement.classList.add("is-active");
    }
    modalImage.setAttribute("src", imgUrlToDisplay);
}
