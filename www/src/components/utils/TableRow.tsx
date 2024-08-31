import { ReactNode, useState } from 'react';

type Props = {
  children: ReactNode;
  onClick(e: React.MouseEvent<HTMLElement>): void;
};

export const TableRow = ({ children, onClick }: Props): ReactNode => {
  const [componentActiveClass, setComponentActiveClass] = useState<boolean>(false);

  const eventHandler = (e: React.MouseEvent<HTMLElement>) => {
    onClick(e);
    setComponentActiveClass(!componentActiveClass);
  };

  return (
    <tr className={componentActiveClass ? 'active' : ''} onClick={eventHandler}>
      {children}
    </tr>
  );
};
