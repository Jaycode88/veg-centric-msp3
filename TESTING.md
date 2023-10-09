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
I decided to re-write all jQuery functions into Javascript functions in a seperate  file called javascript.js(in the same directory as my script.js file)Just for the purpose of testing those functions with jest. To do this I found I also needed to install Babel and some related packages using:
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