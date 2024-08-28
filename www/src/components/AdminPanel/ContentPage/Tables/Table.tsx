import React, { HTMLProps, useMemo } from 'react';

import {
  Column,
  ColumnDef,
  ColumnFiltersState,
  RowData,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from '@tanstack/react-table';

// import { queryUsers, User } from './TableUsers'
import { TableRow } from './TableRow';
import { IParserData } from '../../../../services/AdminPanelService';
import { Button } from 'react-bootstrap';

declare module '@tanstack/react-table' {
  //allows us to define custom properties for our columns
  interface ColumnMeta<TData extends RowData, TValue> {
    filterVariant?: 'text' | 'select';
  }
}

type Props = {
  serverData: IParserData[] | undefined;
};

export const ParserTable = (props: Props) => {
  const [rowSelection, setRowSelection] = React.useState({});
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);

  //   const { data: serverData } = queryUsers();

  //   const [data, setData] = React.useState<Person[]>([])

  const data = useMemo(() => props.serverData ?? [], [props.serverData]);

  //   const refreshData = () => setData(_old => makeData(50_000))
  // const refreshData = () => setData(_old => serverData)

  const editRow = () => {
    if (table.getSelectedRowModel().rows.length > 0) {
      const system_name = table.getSelectedRowModel().rows[0].original.system_name;
      console.log(system_name);
    }
  };

  const columnsUser = React.useMemo<ColumnDef<IParserData>[]>(
    () => [
      {
        id: 'select',
        cell: ({ row }) => (
          <div className="px-1">
            <IndeterminateCheckbox
              {...{
                checked: row.getIsSelected(),
                disabled: !row.getCanSelect(),
                indeterminate: row.getIsSomeSelected(),
                onChange: row.getToggleSelectedHandler(),
              }}
            />
          </div>
        ),
      },
      {
        accessorKey: 'system_name',
        id: 'system_name',
        header: () => 'Системное имя',
        cell: (info) => info.getValue(),
      },
      {
        accessorFn: (row) => row.parser_name,
        id: 'parser_name',
        header: 'Имя парсера',
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: 'description',
        id: 'description',
        header: 'Описание',
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: 'is_enable',
        accessor: 'is_enable',
        // accessor: d => { return d.is_active ? 'Available' : 'Not available' },
        id: 'is_enable',
        header: 'Активен',
        // meta: {
        //   filterVariant: 'select',
        // },

        cell: (info) => (info.getValue() ? 'Да' : 'Нет'),
        // cell: (info) => info.getValue(),
      },
      //   {
      //     accessorKey: 'is_superuser',
      //     id: 'is_superuser',
      //     header: 'Администратор',
      //     // Filter: () => (
      //     //   <select className='form-control' value={state.availability_value} onChange={(e) => applyFilter(e.target.value)} >
      //     //     <option value={`{ "available": "" }`}>Select</option>
      //     //     <option value={`{ "available": "" }`}>All</option>
      //     //     <option value={`{ "available": "1" }`}>Available</option>
      //     //     <option value={`{ "available": "0" }`}>Not available</option>
      //     //   </select>)
      //     meta: {
      //       filterVariant: 'select',
      //     },
      //     // cell: info => info.getValue() ? 'Да' : 'Нет',
      //   },
      //   {
      //     accessorKey: 'is_tg_bot',
      //     id: 'is_tg_bot',
      //     header: 'Пользователь для бота',
      //     meta: {
      //       filterVariant: 'select',
      //     },
      //     cell: (info) => (info.getValue() ? 'Да' : 'Нет'),
      //   },
      //   {
      //     accessorKey: 'is_verified',
      //     id: 'is_verified',
      //     header: 'Пользователь проверен',
      //     meta: {
      //       filterVariant: 'select',
      //     },
      //     cell: (info) => (info.getValue() ? 'Да' : 'Нет'),
      //   },
    ],
    []
  );

  const table = useReactTable({
    data,
    columns: columnsUser,
    filterFns: {},
    state: {
      columnFilters,
      rowSelection,
    },
    enableMultiRowSelection: false,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(), //client side filtering
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onRowSelectionChange: setRowSelection,
  });

  return (
    <div className="p-2">
      <Button onClick={editRow}>edit</Button>
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <th key={header.id} colSpan={header.colSpan}>
                    {header.isPlaceholder ? null : (
                      <>
                        <div
                          {...{
                            className: header.column.getCanSort() ? 'cursor-pointer select-none' : '',
                            onClick: header.column.getToggleSortingHandler(),
                          }}
                        >
                          {flexRender(header.column.columnDef.header, header.getContext())}
                          {{
                            asc: ' 🔼',
                            desc: ' 🔽',
                          }[header.column.getIsSorted() as string] ?? null}
                        </div>
                        {header.column.getCanFilter() ? (
                          <div>
                            <Filter column={header.column} />
                          </div>
                        ) : null}
                      </>
                    )}
                  </th>
                );
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => {
            return (
              <TableRow key={row.id} onClick={row.getToggleSelectedHandler()}>
                {row.getVisibleCells().map((cell) => {
                  return <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>;
                })}
                {/* </> */}
              </TableRow>
            );
          })}
        </tbody>
      </table>

      <div className="h-2" />
      <div className="flex items-center gap-2">
        <button
          className="border rounded p-1"
          onClick={() => table.setPageIndex(0)}
          disabled={!table.getCanPreviousPage()}
        >
          {'<<'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          {'<'}
        </button>
        <button className="border rounded p-1" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
          {'>'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.setPageIndex(table.getPageCount() - 1)}
          disabled={!table.getCanNextPage()}
        >
          {'>>'}
        </button>
        <span className="flex items-center gap-1">
          <div>Page</div>
          <strong>
            {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
          </strong>
        </span>
        <span className="flex items-center gap-1">
          | Go to page:
          <input
            type="number"
            defaultValue={table.getState().pagination.pageIndex + 1}
            onChange={(e) => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0;
              table.setPageIndex(page);
            }}
            className="border p-1 rounded w-16"
          />
        </span>
        <select
          value={table.getState().pagination.pageSize}
          onChange={(e) => {
            table.setPageSize(Number(e.target.value));
          }}
        >
          {[10, 20, 30, 40, 50].map((pageSize) => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
      <div>Количество строк: {table.getPrePaginationRowModel().rows.length}</div>
      <pre>{JSON.stringify({ columnFilters: table.getState().columnFilters }, null, 2)}</pre>
      <div>
        {Object.keys(rowSelection).length} of {table.getPreFilteredRowModel().rows.length} Total Rows Selected
      </div>
      <hr />
      <br />
      <div>
        <button
          className="border rounded p-2 mb-2"
          onClick={() => console.info('table.getSelectedRowModel().flatRows', table.getSelectedRowModel().flatRows)}
        >
          Log table.getSelectedRowModel().flatRows
        </button>
      </div>
      <div>
        <label>Row Selection State:</label>
        <pre>{JSON.stringify(table.getState().rowSelection, null, 2)}</pre>
      </div>

      <hr />
      <br />
      <hr />
      <br />
    </div>
  );
};

function Filter({ column }: { column: Column<any, unknown> }) {
  let columnFilterValue = column.getFilterValue();
  const { filterVariant } = column.columnDef.meta ?? {};

  // console.log(columnFilterValue?.toString())
  return filterVariant === 'select' ? (
    <select
      onChange={(e) => {
        // console.log(e.target.value)
        // console.log(typeof e.target.value)
        console.log(columnFilterValue?.toString());
        console.log('--------------------');
        column.setFilterValue(e.target.value);
      }}
      value={columnFilterValue?.toString()}
    >
      {/* See faceted column filters example for dynamic select options */}
      <option value="">Все</option>
      <option value="true" label="Да" />
      <option value="false" label="Нет" />
    </select>
  ) : (
    <DebouncedInput
      className="w-36 border shadow rounded"
      onChange={(value) => column.setFilterValue(value)}
      placeholder={`Search...`}
      type="text"
      value={(columnFilterValue ?? '') as string}
    />
    // See faceted column filters example for datalist search suggestions
  );
}

// A typical debounced input react component
function DebouncedInput({
  value: initialValue,
  onChange,
  debounce = 500,
  ...props
}: {
  value: string | number | boolean;
  onChange: (value: string | number | boolean) => void;
  debounce?: number;
} & Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'>) {
  const [value, setValue] = React.useState(initialValue);

  React.useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  React.useEffect(() => {
    const timeout = setTimeout(() => {
      onChange(value);
    }, debounce);

    return () => clearTimeout(timeout);
  }, [value]);

  return <input {...props} value={value} onChange={(e) => setValue(e.target.value)} />;
}

function IndeterminateCheckbox({
  indeterminate,
  className = '',
  ...rest
}: { indeterminate?: boolean } & HTMLProps<HTMLInputElement>) {
  const ref = React.useRef<HTMLInputElement>(null!);

  React.useEffect(() => {
    if (typeof indeterminate === 'boolean') {
      ref.current.indeterminate = !rest.checked && indeterminate;
    }
  }, [ref, indeterminate]);

  return <input type="checkbox" ref={ref} className={className + ' cursor-pointer'} {...rest} />;
}
