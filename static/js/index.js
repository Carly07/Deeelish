// jQuery Initialization Materialize CSS components

$(document).ready(function(){
    // Navbar dropdown for larger screens:
    $(".dropdown-button").dropdown();

    // Initialize side navigation for small screens:
    $(".button-collapse").sideNav();

    // Initialize parallax images on index.html:
    $('.parallax').parallax();

    // Initialize Seasonal recipes carousel on index.html:
    $('.carousel').carousel();

    // Initialize accordion to display recipe and category results:
    $('.collapsible').collapsible();

    // Initialize modals for Tips Section:
    $('.modal').modal();

    // Initialize select dropdown menu for displaying categories:
    $('select').material_select();
    
});