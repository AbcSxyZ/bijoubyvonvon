/*
** gallery-filter.js:
**
** Retrieve applied filters for the gallery and format
** URL dynamically to change gallery content.
*/

/*
** retrieveTypeFilter:
**
** Return an array with ids of all checked types.
*/

function retrieveTypeFilter()
{
    let CSSquery = "#type-filter input";
    let selectedTypes = document.querySelectorAll(CSSquery);
    let typeTag, typeIds;

    typeIds = new Array();
    for (typeTag of selectedTypes)
    {
        if (typeTag.checked)
            typeIds.push(typeTag.getAttribute("value"));
    }
    return (typeIds);
}

/*
** retrieveTechniqueFilter:
**
** Retrieve the activate tab in the list of technique,
** and return his ids.
*/

function retrieveTechniqueFilter()
{
    let CSSquery = "#technique-filter li.is-active";
    let selectedTechnique = document.querySelector(CSSquery);
    return (selectedTechnique.getAttribute("data-technique"));
}

/*
** formatFiltersUrl:
**
** Prepare parameters to update the content of the gallery.
** Retrieve filters for technique and type and format the url
** according to it.
*/

function formatFiltersUrl()
{
    let selectedTechniqueId = retrieveTechniqueFilter();
    let selectedTypesIds = retrieveTypeFilter();
    let URLoptions = `technique=${selectedTechniqueId}`;
    let formattedTypes;
    
    if (selectedTypesIds.length > 0)
    {
        formattedTypes = selectedTypesIds.join(",");
        URLoptions += `&types=${formattedTypes}`;
    }
    return (URLoptions);
}
