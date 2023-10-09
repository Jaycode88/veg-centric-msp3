// Initialize mobile navigation bar dropdown menus
function initializeDropdown() {
    var dropdownMobile = document.querySelectorAll('.dropdown-trigger');
    for (var i = 0; i < dropdownMobile.length; i++) {
        M.Dropdown.init(dropdownMobile[i]);
    }
}

document.addEventListener("DOMContentLoaded", initializeDropdown);

// Initialize the category selection dropdown on the Add Recipe page
function initializeFormSelect() {
    var selectElements = document.querySelectorAll('select');
    for (var i = 0; i < selectElements.length; i++) {
        M.FormSelect.init(selectElements[i]);
    }
}

document.addEventListener("DOMContentLoaded", initializeFormSelect);

// Handles the "Add Ingredients" functionality for a dynamic form
function handleAddIngredient() {
    const ingredientFields = document.querySelector("#ingredientFields");
    const addIngredientButton = document.querySelector("#addIngredientButton");

    addIngredientButton.addEventListener("click", function(event) {
        event.preventDefault();

        const newIngredient = document.createElement("div");
        newIngredient.className = "ingredient";
        newIngredient.innerHTML = "<input type='text' name='ingredient[]' placeholder='Ingredient' aria-label='Ingredient Input'>" +
            "<input type='text' name='quantity[]' placeholder='Quantity' aria-label='Quantity Input'>" +
            "<button class='removeButton btn-small custom-darkgreen black-text' aria-label='Remove Ingredient Button'><strong>Remove</strong> <i class='fas fa-trash-alt black-text'></i></button>";

        ingredientFields.appendChild(newIngredient);
    });

    ingredientFields.addEventListener("click", function(event) {
        if (event.target.classList.contains("removeButton")) {
            event.preventDefault();
            const ingredient = event.target.closest(".ingredient");
            ingredientFields.removeChild(ingredient);
        }
    });
}

document.addEventListener("DOMContentLoaded", handleAddIngredient);

// Handles the "Add Method Step" functionality for a dynamic form
function handleAddMethodStep() {
    const methodFields = document.querySelector("#methodFields");
    const addMethodStepButton = document.querySelector("#addMethodStepButton");

    addMethodStepButton.addEventListener("click", function(event) {
        event.preventDefault();

        const newMethodStep = document.createElement("div");
        newMethodStep.className = "method-step";
        newMethodStep.innerHTML = "<input type='text' name='method_step[]' placeholder='Step' aria-label='Step of Method Input'>" +
            "<button class='removeButton btn-small custom-darkgreen black-text' aria-label='Remove Step Button'><strong>Remove</strong> <i class='fas fa-trash-alt black-text'></i></button>";

        methodFields.appendChild(newMethodStep);
    });

    methodFields.addEventListener("click", function(event) {
        if (event.target.classList.contains("removeButton")) {
            event.preventDefault();
            const methodStep = event.target.closest(".method-step");
            methodFields.removeChild(methodStep);
        }
    });
}

document.addEventListener("DOMContentLoaded", handleAddMethodStep);

// Function to initialize and control the Terms and Privacy modals
function initializeModals() {
    var modals = document.querySelectorAll('.modal');
    for (var i = 0; i < modals.length; i++) {
        M.Modal.init(modals[i]);
    }

    var termsLink = document.querySelector('#termsLink');
    termsLink.addEventListener('click', function () {
        var termsModal = document.querySelector('#termsModal');
        var instance = M.Modal.getInstance(termsModal);
        instance.open();
    });

    var privacyLink = document.querySelector('#privacyLink');
    privacyLink.addEventListener('click', function () {
        var privacyModal = document.querySelector('#privacyModal');
        var instance = M.Modal.getInstance(privacyModal);
        instance.open();
    });
}

document.addEventListener("DOMContentLoaded", initializeModals);

// Initialize collapsible elements on the profile page
function initializeCollapsible() {
    var collapsibleElements = document.querySelectorAll('.collapsible');
    for (var i = 0; i < collapsibleElements.length; i++) {
        M.Collapsible.init(collapsibleElements[i]);
    }
}

document.addEventListener("DOMContentLoaded", initializeCollapsible);

module.exports = {
    initializeDropdown,
    initializeFormSelect,
    initializeCollapsible,
}