// Import necessary dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import TableCell from "./components/TableCell.coffee"

// Import any other custom components or logic here if needed
// Since the resolve.alias in webpack already points to your overridden TableCell,
// there's no need to import it explicitly unless you're using it in a custom way.


// If you need to directly inject or use your TableCell component somewhere
// in a specific DOM element, you can do that here. For example:

function initializeCustomComponents() {
  // Example: Attach your custom TableCell or another React component to a target element
  const targetElement = document.getElementsByClassName('.Result')
  if (targetElement) {
    // This is just an example: modify it to suit your component usage
    ReactDOM.render(<TableCell />, targetElement);
  }
}

// Initialize components (you can add more custom logic here)
initializeCustomComponents();
