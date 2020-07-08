/*
** gallery-filter-switch.js:
**
** Manage the dynamic display of the filter menu.
** Change state of links, and change content of the gallery
** using gallery-filter.js functions.
*/

/*
** resetActiveTechnique:
**
** Deactivate all links of the technique filter.
*/

function resetActiveTechnique()
{
    let techniqueLink;
    let listTechniques = document.querySelectorAll("#technique-filter li");

    for (techniqueLink of listTechniques)
        techniqueLink.setAttribute("class", "");
}

/*
** setActiveTechnique:
**
** Callback for the '#technique-filter' item on click event.
** Switch the display to the selected technique, and update the
** content of the gallery according to the filter.
*/

function setActiveTechnique(event)
{
    resetActiveTechnique();
    event.target.parentNode.setAttribute("class", "is-active");
    updateShopJewels();
}

/*
** filterMenus_AddEventListener:
**
** Setup click event listener on '#technique-filter li' items to allow
** tab switch.
** Add event listener on the list of type in "#type-filter"
** to update the shop whenever a modification append.
*/

function filterMenus_AddEventListener()
{
    let listTechniques = document.querySelectorAll("#technique-filter li a");
    let techniqueLink, typeLink;

    for (techniqueLink of listTechniques)
        techniqueLink.addEventListener("click", setActiveTechnique);

    for (typeLink of document.querySelectorAll("#type-filter li input"))
        typeLink.addEventListener("click", updateShopJewels);
}
