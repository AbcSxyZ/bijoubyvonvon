// CUSTOM CONFIG FOR THE PAGINATION BAR
const PAGINATION_DIV = "#jewel-pagination";
const PAGINATION_ACTIVATE = true;
const PAGINATION_LIMIT = 9;

// USEFUL GLOBALS
var JEWEL_TEMPLATE;
var JEWELS_LIST;

/*
** moveToGallery:
**
** Scroll manually to the top of gallery with anchor.
*/

function moveToGallery()
{
    // Move to anchor manually
    let gallery = document.querySelector("#jewel-gallery");
    gallery.scrollIntoView({behavior:"instant"});
}

/*
** loadJewelsJSON:
**
** Return JSON data of all jewels to display
** inside the gallery.
*/

function loadJewelsJSON(options)
{
    return new Promise(function(resolve, reject){
        let request = new XMLHttpRequest();
        let requestedURL = "/jewels/";
    
        if (options)
            requestedURL += `?${options}`;
        request.open("GET", requestedURL);
        request.onload = function(requestResponse){
            if (requestResponse.target.status != 200)
                reject(requestResponse);
            else
                resolve(requestResponse);
        };
        request.send();
    });
}

/*
** loadTemplate:
**
** Retrieve the template's tag for a jewel card.
** Convert the template's content into it's own javascript Element.
** Remove the template for cross browser compatibility.
*/

function loadTemplate()
{
    let template = document.querySelector("template#jewel-template");
    let jewelTemplate = document.createElement("div");

    jewelTemplate.innerHTML = template.innerHTML;
    template.remove();
    JEWEL_TEMPLATE = jewelTemplate.firstElementChild;
}

/*
** formatJewelSrc:
**
** Format the img src attribute.
** Add size to the filemane according to the screen width.
** Size will be treated by the server to reduce image.
*/

function formatJewelSrc(imageName)
{
    let maxWidth, divider;

    if (window.screen.width > 1024)
        divider = 3
    else if (window.screen.width > 768)
        divider = 2
    else
        divider = 1
    maxWidth = Math.floor((window.screen.width / divider) * 2);
    return `${imageName}.s-${maxWidth}`
}

/*
** setupJewelCard:
**
** Called for each jewel inserted in the job.
** Format his bulma card with all avaible data
*/

function setupJewelCard(jewelData)
{
    let cardTag, jewelCard;

    jewelCard = JEWEL_TEMPLATE.cloneNode(true);

    // Setup click event to display modal
    jewelCard.addEventListener("click", jewelModalListener);
    // Change card description
    cardTag = jewelCard.querySelector(".card-content .jewel-description");
    // Add price on description if available
    let descriptionText = jewelData.description;
    if (jewelData.price)
        descriptionText += ` - ${jewelData.price} €` 
    cardTag.innerHTML = descriptionText;

    //Add jewel reference
    jewelRef = jewelCard.querySelector(".jewel-reference");
    if (jewelData.reference)
        jewelRef.innerHTML = `Ref : ${jewelData.reference}`;

    //Replace image
    cardTag = jewelCard.querySelector(".card-image img");
    return new Promise(function(resolve, reject){
        cardTag.onload = function(){
            resolve(jewelCard);
        };
        cardTag.setAttribute("src", formatJewelSrc(jewelData.image));
    });
}

/*
** convertJewelsJson:
**
** Convert loaded array of string into an array of Element.
** Create bulma card for each Jewel.
*/

function convertJewelsJson(jewelList)
{
    let jewelData;
    let elementsJewel = new Array();

    for (jewelData of jewelList)
        elementsJewel.push(setupJewelCard(jewelData));
    return elementsJewel;
}

/*
** displayEmptyShop:
**
** Remove gallery content (jewels and pagination) and display
** expected message.
*/

function displayEmptyShop(msg)
{
    let emptyDiv = document.createElement("div");
    let emptyGallery = document.querySelector("#empty-gallery");

    removeLoader();
    moveToGallery();
    emptyDiv.innerText = msg;
    emptyGallery.appendChild(emptyDiv);
}

/*
** clearPreviousGallery:
**
** Remove content of previously displayed jewel, or remove
** sentence displayed for empty shop.
*/

function clearPreviousGallery()
{
    document.querySelector("#jewel-cards").innerHTML = "";
    document.querySelector("#empty-gallery").innerHTML = "";
    document.querySelector(PAGINATION_DIV).innerHTML = "";

    document.querySelector("#loader").style.display = "flex";
}

/*
** manageGalleryPagination:
**
** Manage the number of page in the pagination bar,
** and which jewels will be displayed.
**
** Globale configuration can impact how it works :
** - PAGINATION_ACTIVATE : true or false if we use pagination mecanism.
** - PAGINATION_LIMIT : Number of jewel per page.
**
** Return the current list of jewels to display for the given page.
*/

function manageGalleryPagination(pageNumber)
{
    let nbrPages, nbrJewels;
    let replacementJewels;

    if (PAGINATION_ACTIVATE == false)
        return (JEWELS_LIST);
    nbrJewels = JEWELS_LIST.length;
    nbrPages = Math.trunc(nbrJewels / PAGINATION_LIMIT);
    nbrPages += nbrJewels % PAGINATION_LIMIT != 0;
    createPaginationBar(nbrPages, pageNumber);

    let from, to;
    from = (pageNumber - 1) * PAGINATION_LIMIT;
    to = pageNumber * PAGINATION_LIMIT;
    return (convertJewelsJson(JEWELS_LIST.slice(from, to)));
}

/*
** removeLoader:
**
** Verify if the loader icon is displayed, remove it if it's
** the case.
*/

function removeLoader()
{
    let loader;

    loader = document.querySelector("#loader");
    if (loader.style.display == "flex")
        loader.style.display = "none";
}

/*
** displayJewelPage:
**
** Display all card of jewels. Display the given page number,
** or all jewels if PAGINATION_ACTIVATE is false.
*/

async function displayJewelPage(pageNumber)
{
    let galleryTag;
    let jewelCard, cardPromise;
    let listCard = new Array();

    // Remove previous page and scroll to gallery anchor
    clearPreviousGallery();
    moveToGallery();

    // Retrieve all loaded card in a single list
    for (cardPromise of manageGalleryPagination(pageNumber))
        listCard.push(await cardPromise);

    // Remove loader animation, the css icon
    removeLoader();

    //Display finally all card at once
    galleryTag = document.querySelector("#jewel-cards");
    for (jewelCard of listCard)
        galleryTag.append(jewelCard);
    //Force moving to gallery, Firefox scroll down when inserting
    //data...
    moveToGallery();
}


/*
** updateShopJewels:
**
** Setup a new list of jewels used in the gallery,
** according to the given filters.
*/

async function updateShopJewels()
{
    let imgTag, galleryTag;

    JEWELS_LIST = await loadJewelsJSON(formatFiltersUrl());
    JEWELS_LIST = JSON.parse(JEWELS_LIST.target.responseText);

    clearPreviousGallery();
    //If an ajax error occur
    if (JEWELS_LIST === null)
        displayEmptyShop("Bijoux non disponible, erreur lors de la recherche.");
    //If no jewel corresponding to the search
    else if (JEWELS_LIST.length == 0)
        displayEmptyShop("Aucun bijou ne correspond à votre recherche");
    //Display founded jewel
    else if (JEWELS_LIST)
        displayJewelPage(1);
}
