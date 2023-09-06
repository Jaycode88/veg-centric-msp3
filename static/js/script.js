/**
 * Initialize mobile navigation bar dropdown menus.
 *
 * This function is called when the document is ready, and it initializes
 * any dropdown-trigger elements to create dropdown menus for mobile navigation.
 * It makes use of the Dropdown jQuery plugin to handle the dropdown functionality.
 */
$(document).ready(function() {
    var dropdownMobile = $('.dropdown-trigger');
    dropdownMobile.dropdown();
});

/**
 * Initialize the category selection dropdown on the Add Recipe page.
 * This function should be called when the document is ready.
 */
$(document).ready(function(){
    $('select').formSelect();
  });
