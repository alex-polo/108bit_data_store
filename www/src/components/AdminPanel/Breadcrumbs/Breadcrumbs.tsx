import { Link, useMatches } from 'react-router-dom';
import { AgnosticIndexRouteObject } from '@remix-run/router';
import { ReactElement } from 'react';
import { Breadcrumb } from 'react-bootstrap';
import { MdOutlineCottage } from 'react-icons/md';

export interface IndexRouteObject {
  caseSensitive?: AgnosticIndexRouteObject['caseSensitive'];
  pathname?: AgnosticIndexRouteObject['path'];
  id?: AgnosticIndexRouteObject['id'];
  loader?: AgnosticIndexRouteObject['loader'];
  action?: AgnosticIndexRouteObject['action'];
  hasErrorBoundary?: AgnosticIndexRouteObject['hasErrorBoundary'];
  shouldRevalidate?: AgnosticIndexRouteObject['shouldRevalidate'];
  handle?: AgnosticIndexRouteObject['handle'];
  children?: undefined;
  element?: React.ReactNode | null;
  errorElement?: React.ReactNode | null;
  data?: unknown;
}

export const Breadcrumbs = () => {
  let matches: IndexRouteObject[] = useMatches();
  let crumbs: ReactElement[] = matches
    .filter((match) => Boolean(match.handle?.crumb))
    .map((match: IndexRouteObject) => match.handle.crumb(match.data));

  if (crumbs.length > 1)
    return (
      <Breadcrumb>
        {crumbs.map((crumb, index) => (
          <li key={index} className="breadcrumb-item">
            {crumb}
          </li>
        ))}
      </Breadcrumb>
    );
};

type Props = {
  url: string;
  name: string | null;
};

export const BreadcrumbPage = (props: Props) => {
  return (
    <>
      <Link to={props.url}>{props.name ? props.name : <MdOutlineCottage />}</Link>
    </>
  );
};
