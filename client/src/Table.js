import React, {useState, useEffect} from 'react'
import styled from 'styled-components'
import { useTable, useSortBy } from 'react-table'

const Styles = styled.div`
  padding: 1rem;

  table {
    border-spacing: 0;
    border: 1px solid black;

    tr {
      :last-child {
        td {
          border-bottom: 0;
        }
      }
    }

    th,
    td {
      margin: 0;
      padding: 0.5rem;
      border-bottom: 1px solid black;
      border-right: 1px solid black;

      :last-child {
        border-right: 0;
      }
    }
  }
`

function Table({ columns, data }) {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      columns,
      data,
    },
    useSortBy
  )

  // We don't want to render all rows for this example, so cap
  // it at 20 for this use case
  const firstPageRows = rows.slice(0, 20)

  return (
    <>
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                // Add the sorting props to control sorting. For this example
                // we can add them into the header props
                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render('Header')}
                  {/* Add a sort direction indicator */}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? ' 🔽'
                        : ' 🔼'
                      : ''}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {firstPageRows.map(
            (row, i) => {
              prepareRow(row);
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map(cell => {
                    return (
                      <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                    )
                  })}
                </tr>
              )}
          )}
        </tbody>
      </table>
      <br />
      <div>Showing the first 20 results of {rows.length} rows</div>
    </>
  )
}

function TableWrapper() {
  const columns = React.useMemo(
    () => [
      {
        Header: 'Click on a column to sort data',
        columns: [
          {
            Header: 'ID',
            accessor: 'id',
          },
          {
            Header: 'Tweet',
            accessor: 'text',
          },
          {
            Header: 'Likes',
            accessor: 'like_count',
          },
          {
            Header: 'Retweets',
            accessor: 'retweet_count',
          },
          {
            Header: 'Replies',
            accessor: 'reply_count',
          },
          {
            Header: 'Views',
            accessor: 'view_count',
          },
        ],
      },
    ],
    []
  )

  const [tweets, setTweets] = useState([{}])
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/tweets');
      const json = await response.json();
      setTweets(json.tweets)
    }
    fetchData();
  }, [])

  return (
    <Styles>
      <Table columns={columns} data={tweets} />
    </Styles>
  )
}

export default TableWrapper;