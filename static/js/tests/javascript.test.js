// Import the functions to test
import { initializeDropdown, initializeFormSelect, initializeCollapsible, } from './javascript';

// Add polyfills for TextEncoder and TextDecoder
global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;

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
