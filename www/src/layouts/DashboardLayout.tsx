import { ReactElement } from 'react';
import { useOutlet } from 'react-router-dom';

import { Breadcrumbs, NavBar, Sidebar } from '../components/AdminPanel';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../components/context/AuthProvider';

export const DashboardLayout = (): ReactElement => {
  const outlet = useOutlet();
  const { getUserProfile } = useAuth();

  const queryUserProfile = useQuery({ queryKey: ['userProfile'], queryFn: getUserProfile });

  return (
    <>
      <Sidebar username={queryUserProfile.data?.email} isSuperUser={queryUserProfile.data?.is_superuser} />
      <div className="main">
        <NavBar username={queryUserProfile.isSuccess ? queryUserProfile.data?.email : 'undefined'} />

        <main className="content">
          <Breadcrumbs />
          {outlet}
        </main>
      </div>
    </>
  );
};
