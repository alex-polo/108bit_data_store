import { useMutation } from '@tanstack/react-query';
import { ICatalogEntityData } from '../service.types';
import { updateCatalogEntityAPI } from '../ApiRequest';

export const useUpdateCatalogEntity = () => {
  const mutation = useMutation({
    mutationKey: ['useUpdateCatalogEntity'],
    mutationFn: async (data: ICatalogEntityData) => updateCatalogEntityAPI(data),
  });

  return mutation;
};
