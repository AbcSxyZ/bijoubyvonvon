
/*
 * gallery-pagination.js
 *
 * Manage the behavior of the pagination for the jewel gallery.
 */

const BAR_UNFINISHED = 0,
      BAR_FINISHED = 1;

/*
** addBarItem:
**
** Insert into the pagination bar a new Element of any type.
** Pack the given node into a li tag.
*/

function addBarItem(paginationBar, childNode)
{
    let liElem = document.createElement("li");
    liElem.appendChild(childNode);
    paginationBar.querySelector("ul").appendChild(liElem);
}

/*
** addElipsis:
**
** Add into the pagination bar an ellipsis element.
*/

function addElipsis(paginationBar)
{
    let elipsisElem = document.createElement("span");
    elipsisElem.innerHTML = "&hellip;";
    elipsisElem.setAttribute("class", "pagination-ellipsis"); 
    addBarItem(paginationBar, elipsisElem);
}

/*
** addPageNumber:
**
** Add a link for the given page number into the pagination bar.
** Display the link as active if the new number is the selected one.
*/

function addPageNumber(paginationBar, pageNumber, selectedPage)
{
    let linkNumber = document.createElement("a");
    let classStr = "pagination-link";
    if (pageNumber == selectedPage)
        classStr += " is-current";
    linkNumber.setAttribute("class", classStr);
    linkNumber.innerText = pageNumber.toString();
    addBarItem(paginationBar, linkNumber);

    //Create event listener, to display the expected page on click
    linkNumber.addEventListener("click", function (event){
        displayJewelPage(pageNumber);
    });
}

/*
** addPaginationRange:
**
** Add to the pagination bar numbers in range [from; to].
*/

function addPaginationRange(paginationBar, from, to, selectedPage)
{
    let index = from;

    while (index <= to)
        addPageNumber(paginationBar, index++, selectedPage);
}

/*
** addPaginationBegin:
**
** Filling up the entire pagination bar if the number of page is small
** enough, or if the selected page it at the beginning of the pagination
** list. Otherwise, create an ellipsis of the left part.
**
** return values : BAR_FINISHED if the entire bar is created,
**                 BAR_UNFINISHED otherwise.
*/

function addPaginationBegin(paginationBar, totalPages, selectedPage)
{
    let tmpIndex;

    //Add all pages where there is less than 4 pages.
    if (totalPages - 4 <= 0)
    {
        addPaginationRange(paginationBar, 2, totalPages, selectedPage);
        return BAR_FINISHED;
    }
    if (selectedPage - 3 <= 0)
    {
        tmpIndex = selectedPage + 1;
        addPaginationRange(paginationBar, 2, tmpIndex, selectedPage);
        if (selectedPage == 3 && totalPages == 5)
            addPageNumber(paginationBar, 5, selectedPage);
        else
        {
            addElipsis(paginationBar);
            addPageNumber(paginationBar, totalPages, selectedPage);
        }
        return BAR_FINISHED;
    }
    addElipsis(paginationBar);
    return BAR_UNFINISHED;
}

/*
** addPaginationEnd:
**
** If the bar is not filled with only a left side (of an ellipsis),
** try to add a middle part (between 2 ellipsis) or only a right part
** at the end of the pagination bar.
*/


function addPaginationEnd(paginationBar, totalPages, selectedPage)
{
    let tmpIndex;

    //Check if the selected page is at the end of the
    //pagination bar
    if (selectedPage + 2 >= totalPages)
    {
        tmpIndex = selectedPage - 1;
        addPaginationRange(paginationBar, tmpIndex, totalPages, selectedPage);
        return ;
    }
    //Whenever the selected page is far from the beginning or the
    //end of the bar, at a range [selectedPage - 1;selectedPage + 1]
    //at the middle of the pagination bar. Having ellipsis of both side.
    addPaginationRange(paginationBar, selectedPage - 1, selectedPage + 1, selectedPage);
    addElipsis(paginationBar);
    addPageNumber(paginationBar, totalPages, selectedPage);
}

/*
** createPaginationBar:
**
** Create a pagination bar, with the expected number of page.
** Activate the selected page link.
** According to the position of the user selection, and the size
** of the bar, add ellipses.
*/

function createPaginationBar(totalPages, selectedPage)
{
    // Create the default pagination bar and
    // add him an <ul> element.
    let paginationBar = document.createElement("div");
    let ulList = document.createElement("ul");
    paginationBar.setAttribute("class", "pagination is-centered");
    ulList.setAttribute("class", "pagination-list");
    paginationBar.appendChild(ulList);

    // Fill up the pagination in two times.
    // Filling up the begining part in first,
    // and if the bar isn't complete, fill the middle and/or the end
    // of the bar.
    let state;
    addPageNumber(paginationBar, 1, selectedPage);
    state = addPaginationBegin(paginationBar, totalPages, selectedPage);
    if (state == BAR_UNFINISHED)
        addPaginationEnd(paginationBar, totalPages, selectedPage);

    //Add the new pagination bar into the webpage, remove the previous
    let paginationContainer;
    paginationContainer = document.querySelector(PAGINATION_DIV);
    paginationContainer.appendChild(paginationBar);
}
