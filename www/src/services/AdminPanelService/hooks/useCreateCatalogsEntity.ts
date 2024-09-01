import { useMutation } from '@tanstack/react-query';
import { ICatalogEntityData } from '../service.types';
import { createCatalogEntityAPI } from '../ApiRequest';

export const useCreateCatalogEntity = () => {
  const mutation = useMutation({
    mutationKey: ['useCreateCatalogEntity'],
    mutationFn: async (data: ICatalogEntityData) => createCatalogEntityAPI(data),
  });

  return mutation;
};
