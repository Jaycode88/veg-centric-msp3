# Testing

Return back to the [README.md](README.md) file.

I have used various tools to Test Funcionality, Validity and responsiveness. I have been sure to check all layouts, colours, text, forms, links, buttons are functioning on all devices and screen sizes that I have tested.

## Code Validation

### HTML

I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.

- links to results:

N.B Images of results

### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate all of my CSS files.

- link to results:

N.B Images of Results

### JavaScript

I have used the recommended [JShint Validator](https://jshint.com) to validate my JS file. I used version 11 which does not throw errors due to use of ES6 syntax.

N.B Image of results

### PEP8

I have used ..............  to check all Python files are PEP8 compliant.

N.B Image of Results

## User Story Testing

N.B Add table for user stories with link to image like example.

## Browser Compatability / Cross Platform Testing

### CRUD (create, read, update, delete) Testing

N.B Add table following example

### Form Validation Testing

N.B Add table following example

### LightHouse Testing
I used Google Chrome Lighthouse testing to assess the quality of the web app.

N.B Table or Images of Results

## Responsiveness
I've tested my deployed project on multiple devices to check for responsiveness issues.

N.B note here the minimum screen size and research on devices. add image of researched table.

N.B Add responsiveness table as in previous project

## Automated Testing
### Jest Testing JQuery

I first attempted to test my JQuery code with jest version 29.7.0, I first installed the nessacery packages using the commands bellow:

To install Jest:
```
npm install --save-dev jest
```

To install jsdom:
```
npm install --save-dev jest-environment-jsdom
```

To install jQuery as a development dependancy:
```
npm install --save-dev juery
```

I then created the jest.config.js file in the root directory as well as a new ```__tests__```folder containing my jquery-mock.js(to mock jquery globally. instead of writing it into each test) and my script.test.js(containing my tests). I kept recieving the this error:
```
ReferenceError: $ is not defined
```
Despite having installed jquery as a dependancy I could not find a way for Jest to test my jQuery code. 

### Jest Testing JavaScript
I decided to re-write all jQuery functions into Javascript functions in a seperate  file called javascript.js(in a tests directory within the "JS" directory where my script.js file is located). I found I also needed to install Babel and some related packages using:
```
npm install --save-dev @babel/core @babel/preset-env babel-jest
```
I also had to create a "babel.config.js file in my root directory its contents as follows:
```
module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        targets: {
          node: 'current',
        },
      },
    ],
  ],
};
```
This also required me to Update my jest configuration file to match below:
```
module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
};
```
From there I was able to write tests for the initializeDropdown, initializeCollapsible and initializeFormSelect Functions which all passed:
![mockup](./static/documentation/jestpassed.webp)

Below is a description of the the functions I attempted to test with no success.

- **initializeModals Function**
    1. **Setup**: I set up a testing environment using Jest and included the tests for the `initializeModals` function within the same file as the other tests.

    2. **Mocking Dependencies**: I successfully mocked the dependencies required by the `initializeModals` function, such as `M.Modal.init` and the event listeners for the Terms and Privacy links.

    3. **Testing Initialization**: I initially attempted to test whether the `initializeModals` function correctly initializes the modals by checking if `M.Modal.init` is called for each modal element with the '.modal' class. This part of the test passed without issues.

    4. **Simulating Click Events**: To test the modal control functionality, I tried to simulate click events on the Terms and Privacy links ('#termsLink' and '#privacyLink') to ensure that the respective modals are opened.

    5. **Challenges and Issues**:

    - **Failure to Open Modals**: Despite my efforts, I encountered persistent issues with simulating the click events on the links. Specifically, I faced challenges with the modal not opening as expected when simulating the click events. This issue prevented me from verifying a valid test for this function.

    - **Debugging Attempts**: I made several debugging attempts by adding `console.log` statements and using `async/await` to synchronize the test, but the problem persisted. Even though I could verify that the event listeners were correctly set up, the modals were not being opened during the test.

    6. **Conclusion**: Due to the issues encountered and the challenges faced in simulating the modal open behavior, I was unable to complete testing for the `initializeModals` function. I have documented my testing process and challenges in this document for future reference.
