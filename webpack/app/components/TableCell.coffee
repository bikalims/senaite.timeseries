React = require 'react'
class TableCell  extends React.Component

  constructor: (props) ->
    super(props)

  render: ->
    <p>WTF</p>


# TableCell as OriginalTableCell = require 'SenaiteAppListing/TableCell.coffee'  # Import the existing component from the main app
# 
# # Define the HOC that wraps the existing component
# withExtension = (WrappedComponent) ->
#   class extends React.Component
#     render: ->
#       React.createElement 'div', null, [
#         React.createElement(WrappedComponent, this.props),  # Render the original component
#         React.createElement 'div', null, "Extended content from the addon!"  # Add extended content
#       ]
# 
# # Wrap TableCell with the HOC
# TableCell = withExtension(OriginalTableCell)

module.exports = TableCell  # Export the extended component
