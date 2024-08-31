import { useMutation } from '@tanstack/react-query';
import { deleteNewsEntityAPI } from '../ApiRequest';

export const useDeleteNewsEntity = () => {
  const mutation = useMutation({
    mutationKey: ['useDeleteNewsEntity'],
    mutationFn: async (id: number) => deleteNewsEntityAPI(id),
  });

  return mutation;
};
