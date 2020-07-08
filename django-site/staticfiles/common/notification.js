/*
** removeNotificationPopup:
**
** @popup : Element, or string of the parent id.
**
** Remove given notification popup. Delete the given
** element, or retrieve the popup from his parent id.
*/

function removeNotificationPopup(popup)
{
    let query;

    if (typeof popup == "string")
    {
        query = popup + " .notification";
        popup = document.querySelector(query);
    }
    if (popup)
        popup.remove();
}

/*
** createNotification:
**
** Create a notification popup who will be displayed in
** the Element given by in_id parameter.
**
** Insert a custom message, and add "is-danger" or "is-success"
** html class if it's expected to be an error message.
**
** Remove the previous notif if needed.
*/

function createNotification(in_id, message, is_error)
{
    let notif = document.createElement("div");
    let notifParent = document.querySelector(in_id);
    let notifButton;

    removeNotificationPopup(in_id);
    // Fill the notification with a closing button
    // and his custom message.
    notif.classList.add("notification");
    notif.innerHTML = "<button class='delete'></button>";
    notif.innerHTML += message;

    // Change the bulma class to create error or success message
    notif.classList.add(is_error ? "is-danger" : "is-success");

    // Display the notification in his parent given by in_id.
    // Add eventListener to close the message from his parent.
    notifButton = notif.querySelector("button");
    notifButton.addEventListener("click", function(){
        removeNotificationPopup(notif);
    })
    notifParent.appendChild(notif);
}

