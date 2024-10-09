// Import necessary dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import TableCell from './components/TableCell.coffee';

document.addEventListener("DOMContentLoaded", () => {
  console.debug("*** SENAITE TIMESERIES JS LOADED ***");

  const waitForResultElement = setInterval(() => {
    const root = document.querySelector('#sample-sections > div > div:nth-child(2) > div table > tbody>  tr > td.contentcell.Result');

    if (root) {
      clearInterval(waitForResultElement);
      console.debug("Root element found:", root);

      // Render the customized TableCell
      ReactDOM.render(<TableCell />, root);
    } else {
      console.debug("Root element not found, waiting...");
    }
  }, 100);  // Check every 100ms
});





//   // Import any other custom components or logic here if needed
//   // Since the resolve.alias in webpack already points to your overridden TableCell,
//   // there's no need to import it explicitly unless you're using it in a custom way.
//   
//   
//   // If you need to directly inject or use your TableCell component somewhere
//   // in a specific DOM element, you can do that here. For example:
//   
//   function initializeCustomComponents() {
//     // Example: Attach your custom TableCell or another React component to a target element
//     const targetElement = document.getElementsByClassName('.Result')
//     if (targetElement) {
//       // This is just an example: modify it to suit your component usage
//       ReactDOM.render(<TableCell />, targetElement);
//     }
//   }
//   
//   // Initialize components (you can add more custom logic here)
//   initializeCustomComponents();
//
// class ExtendedTableCell extends TableCell {
//   render() {
//     // debugger;
//     // Optionally call the original render() method with `super.render()`
//     const originalRender = super.render(); // This will render the original content
// 
//     return (
//       <div>
//         {originalRender} {/* This includes the original component's rendering */}
//         <div>Extended content - additional information here</div>
//       </div>
//     );
//   }
// }

// // Create a Higher-Order Component that wraps TableCell
// function withExtension(WrappedComponent) {
//   return class extends React.Component {
//     componentDidMount() {
//       debugger;
//       console.log('Extended component has mounted!');
//     }
// 
//     render() {
//       debugger;
//       return (
//         <div>
//           <WrappedComponent {...this.props} />
//           <div>Additional content added by the addon!</div>
//         </div>
//       );
//     }
//   };
// }
// 
// // Use the HOC to create the extended component
// const ExtendedTableCell = withExtension(TableCell);
// 
// export default ExtendedTableCell;
// // Addon/index.js
