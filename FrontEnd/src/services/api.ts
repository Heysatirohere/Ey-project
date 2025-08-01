const BASE_URL = 'http://localhost:3000';

interface RespostaApi {
  resultado: string;
}

export async function enviarRelatorio(relatorio: string, norma: string): Promise<RespostaApi> {
  const res = await fetch(`${BASE_URL}/analise`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ relatorio, norma }),
  });

  if (!res.ok) {
    throw new Error('Erro ao enviar dados');
  }

  return res.json();
}
