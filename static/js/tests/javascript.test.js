import { initializeDropdown, initializeFormSelect, initializeCollapsible, handleAddIngredient, handleAddMethodStep, } from './javascript';

// polyfills for TextEncoder and TextDecoder
global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;

// initializeDropdown function
//------------------------------//
// Mock the document and M.Dropdown
document.body.innerHTML = '<div class="dropdown-trigger"></div>';
const mockDropdownInit = jest.fn();
window.M = {
  Dropdown: {
    init: mockDropdownInit,
  },
};

// Mock the M.FormSelect.init separately
const mockFormSelectInit = jest.fn();
window.M.FormSelect = {
  init: mockFormSelectInit,
};

// Test the initializeDropdown function
test('Initialize mobile navigation bar dropdown menus', () => {
  initializeDropdown();

  // Ensure M.Dropdown.init is called for each element with the '.dropdown-trigger' class
  const dropdownElements = document.querySelectorAll('.dropdown-trigger');
  expect(mockDropdownInit).toHaveBeenCalledTimes(dropdownElements.length);
});

// Test the initializeFormSelect function
test('Initialize form select elements', () => {
  initializeFormSelect();

  // Ensure M.FormSelect.init is called for each select element
  const selectElements = document.querySelectorAll('select');
  expect(mockFormSelectInit).toHaveBeenCalledTimes(selectElements.length);
});

// initializeCollapsible Function
//--------------------------------//
// Mock the document and M.Collapsible
document.body.innerHTML = '<div class="collapsible"></div>';
const mockCollapsibleInit = jest.fn();
window.M = {
  Collapsible: {
    init: mockCollapsibleInit,
  },
};

// Test the initializeCollapsible function
test('Initialize collapsible elements on the profile page', () => {
  initializeCollapsible();

  // Ensure M.Collapsible.init is called for each element with the '.collapsible' class
  const collapsibleElements = document.querySelectorAll('.collapsible');
  expect(mockCollapsibleInit).toHaveBeenCalledTimes(collapsibleElements.length);
});

// handleAddIngridient Function
//------------------------------//
// test setup for handleAddIngredient
describe('handleAddIngredient', () => {
  let ingredientFields;
  let addIngredientButton;

  beforeEach(() => {
    document.body.innerHTML = `
      <div id="ingredientFields">
        <!-- Existing ingredients if any -->
      </div>
      <button id="addIngredientButton">Add Ingredient</button>
    `;

    handleAddIngredient();

    ingredientFields = document.querySelector('#ingredientFields');
    addIngredientButton = document.querySelector('#addIngredientButton');
  });

  test('clicking "Add Ingredient" button adds a new ingredient input', () => {
    // Initial ingredient count
    const initialIngredientCount = ingredientFields.querySelectorAll('.ingredient').length;

    // Simulate click on the "Add Ingredient" button
    addIngredientButton.click();

    // Expect one more ingredient to be added
    const updatedIngredientCount = ingredientFields.querySelectorAll('.ingredient').length;
    expect(updatedIngredientCount).toBe(initialIngredientCount + 1);
  });

  test('clicking "Remove" button removes an ingredient input', () => {
    // Add a new ingredient manually
    const newIngredient = document.createElement('div');
    newIngredient.className = 'ingredient';
    newIngredient.innerHTML = `
      <button class='removeButton'>Remove</button>
    `;
    ingredientFields.appendChild(newIngredient);

    // Initial ingredient count
    const initialIngredientCount = ingredientFields.querySelectorAll('.ingredient').length;

    // Find the "Remove" button in the newly added ingredient and simulate a click
    const removeButton = newIngredient.querySelector('.removeButton');
    if (removeButton) {
      removeButton.click();
    }

    // Expect one less ingredient after removal
    const updatedIngredientCount = ingredientFields.querySelectorAll('.ingredient').length;
    expect(updatedIngredientCount).toBe(initialIngredientCount - 1);
  });
});

// handleAddMethodStep Function
//------------------------------//
// test setup for handleAddMethodStep
describe('handleAddMethodStep', () => {
  let methodFields;
  let addMethodStepButton;

  beforeEach(() => {
    document.body.innerHTML = `
      <div id="methodFields">
        <!-- Existing method steps if any -->
      </div>
      <button id="addMethodStepButton">Add Method Step</button>
    `;

    handleAddMethodStep();

    methodFields = document.querySelector('#methodFields');
    addMethodStepButton = document.querySelector('#addMethodStepButton');
  });

  test('clicking "Add Method Step" button adds a new method step input', () => {
    // Initial method step count
    const initialMethodStepCount = methodFields.querySelectorAll('.method-step').length;

    // Simulate click on the "Add Method Step" button
    addMethodStepButton.click();

    // Expect one more method step to be added
    const updatedMethodStepCount = methodFields.querySelectorAll('.method-step').length;
    expect(updatedMethodStepCount).toBe(initialMethodStepCount + 1);
  });

  test('clicking "Remove" button removes a method step input', () => {
    // Add a new method step manually
    const newMethodStep = document.createElement('div');
    newMethodStep.className = 'method-step';
    newMethodStep.innerHTML = `
      <button class='removeButton'>Remove</button>
    `;
    methodFields.appendChild(newMethodStep);

    // Initial method step count
    const initialMethodStepCount = methodFields.querySelectorAll('.method-step').length;

    // Find the "Remove" button in the newly added method step and simulate a click
    const removeButton = newMethodStep.querySelector('.removeButton');
    if (removeButton) {
      removeButton.click();
    }

    // Expect one less method step after removal
    const updatedMethodStepCount = methodFields.querySelectorAll('.method-step').length;
    expect(updatedMethodStepCount).toBe(initialMethodStepCount - 1);
  });
});
