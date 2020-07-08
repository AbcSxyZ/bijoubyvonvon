/*
** isDanger:
**
** Check if the current div input is having is-danger class.
** Return true if it's in danger state, false otherwise.
*/

function isDanger(div)
{
    inputTag = div.querySelector("input");
    if (inputTag == null)
        inputTag = div.querySelector("textarea");
    return (inputTag.classList.contains("is-danger"));
}

/*
** removeDanger:
**
** For a single html div, remove input danger state and
** information message of the error.
*/

function removeDanger(div)
{
    let dangerTags = div.querySelectorAll(".is-danger");
    let tag;

    for (tag of dangerTags)
    {
        if (tag.tagName == "INPUT" || tag.tagName == "TEXTAREA")
            tag.classList.remove("is-danger");
        else
            tag.style.display = "none";
    }
}

/*
** cleanFormInputWarnings:
**
** Remove all error information for email (ex:invalid format)
** and message (ex:empty) inputs.
*/

function cleanFormInputWarnings(form)
{
    let emailDiv = form.querySelector(".email-user");
    let msgDiv = form.querySelector(".msg-input");

    if (isDanger(emailDiv))
        removeDanger(emailDiv);
    if (isDanger(msgDiv))
        removeDanger(msgDiv);
}

/*
** activeDangerInput:
**
** For a given html div, set the input or textarea with
** danger state, and display error message under the input.
*/

function activeDangerInput(div)
{
    let inputTag;
    let helperTag;
    
    inputTag = div.querySelector("input");
    if (inputTag == null)
        inputTag = div.querySelector("textarea");
    inputTag.classList.add("is-danger");
    helperTag = div.querySelector("p.help");
    helperTag.style.display = "initial";
}

/*
** retrieveMailData:
**
** Create an array with all form input of each fields.
*/

function retrieveMailData()
{
    let emailTag = document.querySelector(".email-user input");
    let subjectTag = document.querySelector(".user-subject select");
    let msgTag = document.querySelector(".msg-input textarea");
    let subjectOption;
    let mailData = new Array();

    mailData["email"] = emailTag.value;
    mailData["msg"] = msgTag.value;

    //retrieve subject
    subjectOption = subjectTag[subjectTag.selectedIndex];
    mailData["subject"] = subjectOption.innerHTML;
    return mailData;
}

/*
** getCSRFToken:
**
** Retrieve in an hidden input tag the django csrf token.
*/

function getCSRFToken()
{
    let csrfToken;

    csrfToken = document.querySelector("#contact-form input[name='csrfmiddlewaretoken']")
    return csrfToken.value;
}

/*
** cleanContactFields:
**
** Set to default state each form's fields.
*/

function cleanContactFields()
{
    let emailTag = document.querySelector(".email-user input");
    let subjectTag = document.querySelector(".user-subject select");
    let msgTag = document.querySelector(".msg-input textarea");

    emailTag.value = "";
    subjectTag.selectedIndex = 0;
    msgTag.value = "";
}

/*
** displaySendingBanner:
**
** Callback when ajax request for contact form is over.
** Display a notification banner depending of the request
** status.
** Remove loading state to the form's button
*/

function displaySendingBanner(callback)
{
    let request = callback.target;
    let notifTag = "#contact-form #notification";
    let buttonTag = document.querySelector("#contact-form button");
    let message, is_error;

    //Remove loading animation
    buttonTag.classList.remove("is-loading");

    //Fill up the end of the notification div depending of the
    //request status
    is_error = request.status != 200;
    if (is_error)
        message = "Erreur lors de l'envoi du message.";
    else
        message = "Votre message a bien été envoyé.";
    createNotification(notifTag, message, is_error);
}

/*
** sendMailData:
**
** Send form data to the server with AJAX.
** Clean up contact fields, and manage form button
** to look like loading.
**
** Try also to remove previous popup.
*/

function sendMailData()
{
    let request = new XMLHttpRequest();
    let formData = new FormData();
    let msgData = retrieveMailData();
    let dataName;
    let buttonTag;

    //Remove previous popup if available
    removeNotificationPopup("#contact-form #notification");
    //Fill formData with all available data.
    for (dataName in msgData)
        formData.append(dataName, msgData[dataName]);

    //Display loading button during request.
    buttonTag = document.querySelector("#contact-form button");
    buttonTag.classList.add("is-loading");
    request.onload = displaySendingBanner;
    request.open("POST", "contact/");
    //Need django csrf token
    request.setRequestHeader("X-CSRFToken", getCSRFToken());
    request.send(formData);
    cleanContactFields();
}

/*
** verifyMailData:
**
** Click handler for contact form. Control the validity of
** the data (email format, content in message).
** Send data to the server if it's correct, or display
** error message otherwise.
*/

function verifyMailData()
{
    let form = document.querySelector("#contact-form");
    let email = form.querySelector(".email-user");
    let emailInput = email.querySelector("input");
    let msg = form.querySelector(".msg-input");
    let invalid = false;

    cleanFormInputWarnings(form);
    //Check email validity
    if (emailInput.validity.valid == false || emailInput.value == "")
    {
        activeDangerInput(email);
        invalid = true;
    }
    // Check if message is not empty
    if (msg.querySelector("textarea").value.length == 0)
    {
        activeDangerInput(msg);
        invalid = true;
    }
    if (invalid == false)
        sendMailData();
}
