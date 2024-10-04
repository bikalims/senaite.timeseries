import React from "react"


class TimeSeries extends React.Component

  ###*
   * TimeSeries Field for the Listing Table
   *
   * A multi value field is identified by the column type "timeseries" in the
   * listing view, e.g.  `self.columns = {"Result": {"type": "timeseries"}, ... }`
   *
  ###
  constructor: (props) ->
    super(props)

    # remember the initial value
    @state =
      value: props.defaultValue

    # bind event handler to the current context
    @on_change = @on_change.bind @

  ###*
   * Event handler when the value changed of the field
   * Extract all values in the matrix and store
   * them in a list of lists
   * @param event {object} ReactJS event object
  ###
  on_change: (event) ->
    el = event.currentTarget
    # Get the parent table
    table = el.parentNode.parentNode.parentNode
    # Extract all row elements that store values
    rows = table.querySelectorAll("tr")
    row_cnt = 0
    values = []
    for row in rows
      row_cnt += 1
      if row_cnt == 1
        # Ignore first row which is the header
        continue
      # Extract all inputs in the row
      inputs = row.querySelectorAll("input")
      console.log "TimeSeries::on_change: row num=#{row_cnt} num inputs=#{inputs.length}"
      # Extract the UID attribute
      uid = el.getAttribute("uid")
      # Extract the column_key attribute
      name = el.getAttribute("column_key") or el.name
      # The value to store is a list of results
      row_values = (input.value.trim() for input in inputs)
      # Filter out empty values
      row_values = row_values.filter (value) -> value isnt ""
      console.log "TimeSeries::on_change: row num=#{row_cnt} values=#{row_values}"
      if row_values.length > 0
        # Ignore empty rows, probably the last row
        values.push(row_values)


    # store the new value
    @setState
      value: values

    # Call the *update* field handler
    if @props.update_editable_field
      @props.update_editable_field uid, name, values, @props.item


  ###
   * Converts the value to an array
  ###
  to_matrix: (value, header_len) ->
    console.debug "TimeSeries::to_matrix:value=#{value}"
    if not value
      return []
    if Array.isArray(value)
      result = []
      for row in value
        len = row.length
        rem = header_len - len
        if rem > 0
          for i in [1..rem]
            row.push("")
        result.push(row)
      return result
    if typeof value is 'string'
      # A string value with a list of lists
      parsed = JSON.parse value
      if not Array.isArray(parsed)
        # This might happen when a default value is set, e.g. 0
        return [parsed]
      return parsed
    console.log "TimeSeries::to_matrix: WE SHOULD NEVER GET HERE!!!!"

  ###
   * Inputs table builder. Generates a table of  inputs as matrix
  ###
  build_rows: ->
    # Convert the result to a matrix of rows
    header_len = @props.item.time_series_columns.length
    values = @state.value
    matrix = @to_matrix(values, header_len)
    console.debug "TimeSeries::build_rows: matrix ='#{matrix}'"

    # Add an empty row at the end
    matrix.push(["", "", "", "", ""])

    # Build the rows
    output = []

    # create header row
    th_inputs = []
    headers = @props.item.time_series_columns
    for head in headers
      th_inputs.push(
        <th>
          <input type="text"
                 # size={@props.size or 5}
                 value={head}
                 uid={@props.uid}
                 name={@props.name}
                 title={@props.help or @props.title}
                 onChange={@props.onChange or @on_change}
                 column_key={@props.column_key}
                 className={@props.className}
                 readonly="readonly"
                 {...@props.attrs} />
        </th>
      )
    output.push(
      <tr>
        {th_inputs}
      </tr>
    )
    # Create rows on inputs
    cnt = 0
    for row in matrix
      cnt += 1
      # Create list of TDs
      td_inputs = []
      for item in row
        if this.props.item.result_type == "timeseries_readonly"
          console.log "TimeSeries::build_rows: READONLY #{cnt}: value=#{row}"
          td_inputs.push(
            <td>
              <input type="text"
                     # size={@props.size or 5}
                     value={item}
                     uid={@props.uid}
                     name={@props.name}
                     title={@props.help or @props.title}
                     onChange={@props.onChange or @on_change}
                     column_key={@props.column_key}
                     className={@props.className}
                     readonly="false"
                     {...@props.attrs} />
            </td>)
        else
          console.log "TimeSeries::build_rows: EDITABLE #{cnt}: value=#{row}"
          td_inputs.push(
            <td>
              <input type="text"
                     # size={@props.size or 5}
                     value={item}
                     uid={@props.uid}
                     name={@props.name}
                     title={@props.help or @props.title}
                     onChange={@props.onChange or @on_change}
                     column_key={@props.column_key}
                     className={@props.className}
                     {...@props.attrs} />
            </td>)
      # Add row to output
      output.push(
        <tr>
          {td_inputs}
        </tr>
      )

    return output

  render: ->
    <div className={@props.field_css or "timeseries"}>
      {@props.before and <span className={@props.before_css or "before_field"} dangerouslySetInnerHTML={{__html: @props.before}}></span>}
      <table class="time-series-table" tabIndex={@props.tabIndex}>
        {@build_rows()}
      </table>
      {@props.after and <span className={@props.after_css or "after_field"} dangerouslySetInnerHTML={{__html: @props.after}}></span>}
    </div>


export default TimeSeries
