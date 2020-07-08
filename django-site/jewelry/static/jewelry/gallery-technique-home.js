/*
** toggleGalleryDisplay:
**
** Switch between the selection of technique (#technique-selection)
** and the jewel gallery (#jewel-display), both aren't displayed
** simultaneously.
**
** Make the gallery title clickable when the jewel gallery is
** displayed to come back to the selection of technique.
*/

function toggleGalleryDisplay()
{
    let techniqueHome = document.querySelector("#technique-selection");
    let jewelGallery = document.querySelector("#jewel-display");
    let galleryTitle = document.querySelector("#gallery-title");
    
    if (techniqueHome.style.display != 'none')
    {
        techniqueHome.style.display = 'none';
        jewelGallery.style.display = 'initial';
        galleryTitle.onclick = toggleGalleryDisplay;
    }
    else
    {
        techniqueHome.style.display = 'initial';
        jewelGallery.style.display = 'none';
        galleryTitle.onclick = null;
    }
    galleryTitle.classList.toggle("display-jewel");
}

/*
** setTechnique:
**
** Callback for click event on a technique card.
** Set this technique as a filter for the jewel gallery,
** and display this gallery.
*/

async function setTechnique(techniqueLink)
{
    let techniqueTabs, techniqueId;
    let cssQuery;

    resetActiveTechnique();
    techniqueId = techniqueLink.getAttribute("data-technique");
    cssQuery = `#technique-filter li[data-technique='${techniqueId}']`;
    techniqueTabs = document.querySelector(cssQuery);
    techniqueTabs.setAttribute("class", "is-active");
    await updateShopJewels();
    toggleGalleryDisplay();
}

/*
** setupTechniqueHome:
**
** Add event listener on all technique card in their home
** to allow their selection.
*/

function setupTechniqueHome()
{
    let listTechniques, techniqueLink;

    listTechniques = document.querySelectorAll("#technique-selection a");
    for (techniqueLink of listTechniques)
    {
        techniqueLink.onclick = (function()
        {
            let targetTechnique = techniqueLink;
            return ()=>{setTechnique(targetTechnique)};
        })();
    }
}
