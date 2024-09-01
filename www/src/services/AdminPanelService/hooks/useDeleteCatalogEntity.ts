import { useMutation } from '@tanstack/react-query';
import { deleteCatalogEntityAPI } from '../ApiRequest';

export const useDeleteCatalogEntity = () => {
  const mutation = useMutation({
    mutationKey: ['useDeleteCatalogEntity'],
    mutationFn: async (id: number) => deleteCatalogEntityAPI(id),
  });

  return mutation;
};
