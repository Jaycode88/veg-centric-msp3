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
 *
 * This function initializes the category selection dropdown by calling the 'formSelect' method
 * on all 'select' elements within the document. It should be called when the document is ready
 * to ensure that the dropdowns are properly enhanced and functional.
 *
 * @function initializeCategoryDropdown
 */
$(document).ready(function(){
    $('select').formSelect();
  });

/**
 * Handles the "Add Ingredients" functionality for a dynamic form.
 *
 * This function sets up event handlers to add and remove ingredient fields in a dynamic form.
 * It targets the specified elements, such as the form, ingredient container, and buttons, and
 * provides the logic for adding new ingredient fields and removing them when needed.
 *
 * @function handleAddIngredients
 */
$(document).ready(function() {
    // Select necessary elements
    const form = $("#recipeForm"); // The form element
    const ingredientFields = $("#ingredientFields"); // The container for ingredient fields
    const addIngredientButton = $("#addIngredientButton"); // The button to add new ingredients
  
    // Event handler for clicking the "Add Ingredient" button
    addIngredientButton.on("click", function(event) {
      event.preventDefault(); // Prevent the default form submission behavior
  
      // Create a new ingredient field container
      const newIngredient = $("<div class='ingredient'>" +
        "<input type='text' name='ingredient[]' placeholder='Ingredient'>" +
        "<input type='text' name='quantity[]' placeholder='Quantity'>" +
        "<button class='removeButton btn-small custom-darkgreen'><strong>Remove</strong> <i class='fas fa-trash-alt white-text'></i></button>" +
        "</div>");
  
      ingredientFields.append(newIngredient); // Add the new ingredient field to the container
    });
  
    // Event delegation for removing ingredients
    ingredientFields.on("click", ".removeButton", function(event) {
      event.preventDefault(); // Prevent the default form submission behavior
  
      // Remove the closest ingredient field container when the "Remove" button is clicked
      $(this).closest(".ingredient").remove();
    });
  });

/**
 * Handles the "Add Method Step" functionality for a dynamic form.
 *
 * This function sets up event handlers to add and remove method steps in a dynamic form.
 * It targets the specified elements and provides the logic for adding new method step fields
 * and removing them when needed.
 *
 * @function handleAddMethodStep
 */
  $(document).ready(function() {
    // Select necessary elements
    const methodFields = $("#methodFields"); // The container for method step fields
    const addMethodStepButton = $("#addMethodStepButton"); // The button to add new method steps
  
    // Event handler for clicking the "Add Method Step" button
    addMethodStepButton.on("click", function(event) {
      event.preventDefault(); // Prevent the default form submission behavior
  
      // Create a new method step field container
      const newMethodStep = $("<div class='method-step'>" +
        "<input type='text' name='method_step[]' placeholder='Step'>" +
        "<button class='removeButton btn-small custom-darkgreen'><strong>Remove</strong> <i class='fas fa-trash-alt white-text'></i></button>" +
        "</div>");
  
      methodFields.append(newMethodStep); // Add the new method step field to the container
    });
  
    // Event delegation for removing method steps
    methodFields.on("click", ".removeButton", function(event) {
      event.preventDefault(); // Prevent the default form submission behavior
  
      // Remove the closest method step field container when the "Remove" button is clicked
      $(this).closest(".method-step").remove();
    });
  });

  /**
 * Initializes a full-width carousel with indicators for the welcome page.
 *
 * This function initializes a carousel on elements with the class 'carousel.carousel-slider'
 * to create a full-width carousel with navigation indicators. It provides a user-friendly
 * way to display content on the welcome page with a carousel effect.
 *
 * @function initWelcomePageCarousel
 *
 * @param {Object} options - The configuration options for the carousel.
 * @param {boolean} options.fullWidth - Set to `true` to enable full-width mode for the carousel.
 * @param {boolean} options.indicators - Set to `true` to display navigation indicators for the carousel.
 *
 */
  $('.carousel.carousel-slider').carousel({
    fullWidth: true,
    indicators: true
  });