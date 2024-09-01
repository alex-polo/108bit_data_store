import React, { HTMLProps, useEffect, useMemo, useState } from 'react';
import { Button, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

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

import { TableRow } from '../../../utils/TableRow';

import { ApplicationRouting } from '../../../routes/Routes';
import { useAllCatalogsEntity, useDeleteCatalogEntity } from '../../../../services/AdminPanelService/hooks';
import { ICatalogEntityData } from '../../../../services/AdminPanelService';

declare module '@tanstack/react-table' {
  //allows us to define custom properties for our columns
  interface ColumnMeta<TData extends RowData, TValue> {
    filterVariant?: 'text' | 'select_is_enabled' | 'select_parser_scheme_missing';
  }
}

export const CatalogsEntityTable = () => {
  const navigate = useNavigate();

  const [rowSelection, setRowSelection] = React.useState({});
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);
  const [catalogEntityName, setCatalogEntityName] = useState<string | null>(null);
  const deleteEntityMutation = useDeleteCatalogEntity();
  const queryCatalogsEntity = useAllCatalogsEntity();
  // const queryClient = useQueryClient();
  const [disableButton, setDisableButton] = useState<boolean>(true);

  const data = useMemo(() => queryCatalogsEntity.catalogsEntity ?? [], [queryCatalogsEntity.catalogsEntity]);

  const editButtonHandler = () => {
    if (catalogEntityName) navigate(ApplicationRouting.USER_PROFILE_LINK.editCatalogGatheringEntity(catalogEntityName));
  };

  const createButtonHandler = () => {
    navigate(ApplicationRouting.USER_PROFILE_LINK.createCatalogGatheringEntity);
  };

  const deleteButtonHandler = () => {
    deleteEntityMutation.mutate(table.getSelectedRowModel().rows[0].original.id);
  };

  const columnsUser = React.useMemo<ColumnDef<ICatalogEntityData>[]>(
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
        accessorKey: 'name',
        id: 'name',
        header: () => 'Название',
        cell: (info) => info.getValue(),
      },
      {
        accessorFn: (row) => row.url,
        id: 'Адрес',
        header: 'Адрес',
        cell: (info) => info.getValue(),
      },
      {
        accessorFn: (row) => row.description,
        id: 'description',
        header: 'Описание',
        cell: (info) => info.getValue(),
      },
      // {
      //   accessorKey: 'parser_id',
      //   id: 'parser_id',
      //   header: 'Название схемы парсера',
      //   cell: (info) => info.getValue(),
      // },
      {
        accessorKey: 'is_enable',
        accessor: 'is_enable',
        id: 'is_enable',
        header: 'Активен',
        meta: {
          filterVariant: 'select_is_enabled',
        },
        cell: (info) => info.getValue(),
      },
    ],
    []
  );

  useEffect(() => {
    if (table.getSelectedRowModel().rows.length > 0) {
      setCatalogEntityName(table.getSelectedRowModel().rows[0].original.name);
      setDisableButton(false);
    } else {
      setDisableButton(true);
      setCatalogEntityName(null);
    }
  });

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
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onRowSelectionChange: setRowSelection,
  });

  if (queryCatalogsEntity.isLoading) <Spinner animation="grow" variant="primary" />;

  if (queryCatalogsEntity.isError) <p>Ошибка получения данных</p>;

  return (
    <div className="p-2">
      <Button className="btn btn-success" onClick={createButtonHandler}>
        Добавить сайт
      </Button>
      <Button className="btn btn-danger" disabled={disableButton} onClick={editButtonHandler}>
        Редактировать
      </Button>
      <Button className="btn btn-danger" disabled={disableButton} onClick={deleteButtonHandler}>
        Удалить
      </Button>
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
        <span className=" items-center gap-1">
          <div>Страница</div>
          <strong>
            {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
          </strong>
        </span>
        <span className="flex items-center gap-1">
          | Перейти на страницу:
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
              Показать {pageSize}
            </option>
          ))}
        </select>
      </div>
      <hr />
    </div>
  );
};

function Filter({ column }: { column: Column<any, unknown> }) {
  let columnFilterValue = column.getFilterValue();
  const { filterVariant } = column.columnDef.meta ?? {};

  return filterVariant === 'select_is_enabled' ? (
    <select
      onChange={(e) => {
        column.setFilterValue(e.target.value);
      }}
      value={columnFilterValue?.toString()}
    >
      {/* See faceted column filters example for dynamic select options */}
      <option value="">Показать все</option>
      <option value="Да" label="Да" />
      <option value="Нет" label="Нет" />
    </select>
  ) : (
    <DebouncedInput
      className="w-36 border shadow rounded"
      onChange={(value) => column.setFilterValue(value)}
      placeholder={'Поиск'}
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
