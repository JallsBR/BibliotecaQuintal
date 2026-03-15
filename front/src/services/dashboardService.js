import api from '@/services/APIService'

/**
 * Retorna contagens agregadas para o dashboard da home.
 * Uma única requisição; o backend devolve apenas números (respeitando permissões).
 * @returns {{ livros: number, leitores: number, emprestimos_abertos: number, reservas_ativas: number, recompensas: number }}
 */
export async function getStats() {
  const { data } = await api.get('/dashboard/stats/')
  return {
    livros: Number(data?.livros) || 0,
    leitores: Number(data?.leitores) || 0,
    emprestimos_abertos: Number(data?.emprestimos_abertos) || 0,
    emprestimos_em_atraso: Number(data?.emprestimos_em_atraso) || 0,
    reservas_ativas: Number(data?.reservas_ativas) || 0,
    recompensas: Number(data?.recompensas) || 0
  }
}
