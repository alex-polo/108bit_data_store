import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

import App from './App.tsx';

import './index.css';

export const queryClient = new QueryClient({
  // defaultOptions: {
  //   queries: {
  //     refetchOnWindowFocus: true,
  //     // gcTime: 1000,
  //   },
  // },
  // },
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: true,
      refetchOnReconnect: true,
      retry: 3,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    {/* <React.StrictMode> */}
    <App />
    {/* </React.StrictMode> */}
    <ReactQueryDevtools initialIsOpen={false} />
  </QueryClientProvider>
);
