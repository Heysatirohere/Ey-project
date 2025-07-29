import React, { useState } from 'react';
import { Button } from '../components/Button';
import { enviarRelatorio } from '../services/api';
import './Home.css';

export function Home() {
  const [relatorio, setRelatorio] = useState('');
  const [norma, setNorma] = useState('');
  const [resultado, setResultado] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleEnviar() {
    setLoading(true);
    setError('');
    setResultado('');
    try {
      const res = await enviarRelatorio(relatorio, norma);
      setResultado(res.resultado);
    } catch (e) {
      setError('Erro ao enviar os dados. Tente novamente.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="home-container">
      <h1>GRC - Análise de Relatório</h1>
      <textarea
        placeholder="Digite o relatório..."
        value={relatorio}
        onChange={e => setRelatorio(e.target.value)}
        rows={6}
      />
      <textarea
        placeholder="Digite a norma..."
        value={norma}
        onChange={e => setNorma(e.target.value)}
        rows={4}
      />
      <Button onClick={handleEnviar} disabled={loading || !relatorio || !norma}>
        {loading ? 'Enviando...' : 'Enviar para análise'}
      </Button>

      {error && <p className="error">{error}</p>}

      {resultado && (
        <div className="resultado">
          <h2>Resultado da Análise:</h2>
          <pre>{resultado}</pre>
        </div>
      )}
    </div>
  );
}
