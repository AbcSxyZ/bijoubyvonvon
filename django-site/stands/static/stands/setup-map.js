/*
** addStandsPopup:
**
** Add leaflet popup to the map, based on stands cards.
** Get data of the card, hidden or within field
** to place and fill the popup content.
*/

function addStandsPopup(map, options)
{
    let stand, listStands;
    let latitude, longitude, popupContent, standContent, standName, standMarker;
    let index = 0;

    listStands = document.querySelectorAll("#list-stands .stand-card");
    for (stand of listStands)
    {
        //Retrieve stand coordo to localize popup
        latitude = stand.getAttribute("data-lat");
        longitude = stand.getAttribute("data-long");

        //Initialize map on the first stand
        if (index++ == 0)
            map.setView(new L.LatLng(latitude, longitude), 12);

        //Add the popup content
        standContent = stand.querySelector(".popup-content");
        standContent.remove();
        standContent.style.display = "initial";
        popupContent = standContent.innerHTML;
        standMarker = L.marker([latitude, longitude]).addTo(map).bindPopup(popupContent);

        //Add click event on stand card
        stand.addEventListener("click",
            focusStands(map, standMarker, latitude, longitude));
    }
}

/*
** focusStands:
**
** Click callback for stand cards. Zoom on the stand popup
** on the map.
*/

function focusStands(map, marker, latitude, longitude)
{
    return function (){
        map.closePopup();
        map.setView(new L.LatLng(latitude, longitude));
        marker.openPopup();
        document.querySelector("#stands-map").scrollIntoView();
    }
}
