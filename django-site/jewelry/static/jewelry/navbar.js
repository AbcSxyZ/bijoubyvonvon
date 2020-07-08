function activateBurger()
{
    var burger = document.querySelector('.burger');
    var menu = document.querySelector('#' + burger.dataset.target);
    burger.addEventListener('click', function () {
        burger.classList.toggle('is-active');
        menu.classList.toggle('is-active');
    });
}

function closeOnClickBurger()
{
    let links;
    var burger = document.querySelector('.burger');
    var menu = document.querySelector('#' + burger.dataset.target);
    var burgerLinks = document.querySelectorAll("#navMenu a.navbar-item");

    for (links of burgerLinks)
    {
        links.addEventListener("click", function(){
            burger.classList.toggle("is-active");
            menu.classList.toggle("is-active");
        });
    }
}
closeOnClickBurger();
