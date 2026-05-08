import { useState, useEffect } from 'react';
import type { Place } from './types';
import { fetchPlaces, deleteAllPlaces, deletePlace, sendChat } from './api';
import './App.css';

function App() {
  const [places, setPlaces] = useState<Place[]>([]);
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [noMorePlaces, setNoMorePlaces] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<{role: 'user' | 'assistant', content: string}[]>([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [chatInput, setChatInput] = useState('');

  const loadPlaces = async (newLimit: number, isLoadingMore: boolean = false) => {
    if (isLoadingMore) {
      setLoadingMore(true);
    } else {
      setLoading(true);
    }
    setError(null);
    setNoMorePlaces(false);
    
    try {
      const data = await fetchPlaces(newLimit);
      
      if (isLoadingMore) {
        // Detectar duplicados comparando IDs
        const currentIds = new Set(places.map(p => p.id));
        const newPlaces = data.filter(p => !currentIds.has(p.id));
        
        if (newPlaces.length === 0) {
          // No hay lugares nuevos, todos son duplicados
          setNoMorePlaces(true);
        } else {
          // Agregar solo los nuevos
          setPlaces(prev => [...prev, ...newPlaces]);
        }
      } else {
        setPlaces(data);
      }
      
      setLimit(newLimit);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const handleLoadMore = () => {
    const newLimit = Math.min(limit + 10, 50);
    if (newLimit > limit) {
      loadPlaces(newLimit, true);
    }
  };

  const handleDelete = async () => {
    if (!confirm('¿Sabés qué querés borrar todos los lugares?')) {
      return;
    }

    setDeleting(true);
    setError(null);
    setNoMorePlaces(false);

    try {
      await deleteAllPlaces();
      setPlaces([]);
      setLimit(10);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteOne = async (placeId: number) => {
    if (!confirm('¿Borrar este lugar?')) {
      return;
    }

    setDeletingId(placeId);
    setError(null);

    try {
      await deletePlace(placeId);
      setPlaces(prev => prev.filter(p => p.id !== placeId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setDeletingId(null);
    }
  };

  const handleChatSubmit = async () => {
    if (!chatInput.trim() || chatLoading) return;
    
    const userMessage = chatInput;
    setChatInput('');
    setChatLoading(true);
    
    setChatMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    try {
      const response = await sendChat(userMessage);
      
      if (response.limit_reached) {
        setChatMessages(prev => [...prev, { role: 'assistant', content: '⛔ Has alcanzado el límite de 5 preguntas. Chat bloqueado.' }]);
        setChatOpen(false);
      } else {
        setChatMessages(prev => [...prev, { role: 'assistant', content: response.answer + `\n\n💬 Preguntas restantes: ${response.remaining}` }]);
      }
    } catch (err) {
      setChatMessages(prev => [...prev, { role: 'assistant', content: 'Disculpame, tengo problemitas ahora. Probá de nuevo más tarde.' }]);
    } finally {
      setChatLoading(false);
    }
  };

  useEffect(() => {
    loadPlaces(10);
  }, []);

  const getCategoryEmoji = (category: string) => {
    const cat = category.toLowerCase();
    if (cat.includes('bar')) return '🍺';
    if (cat.includes('café') || cat.includes('cafe')) return '☕';
    if (cat.includes('restaurante')) return '🍽️';
    return '📍';
  };

  const getCategoryLabel = (category: string) => {
    const cat = category.toLowerCase();
    if (cat.includes('bar')) return 'Bar';
    if (cat.includes('café') || cat.includes('cafe')) return 'Café';
    if (cat.includes('restaurante')) return 'Resto';
    return category;
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header__badge">
          <span className="header__badge-dot"></span>
          Tucumán
        </div>
        <h1>Tuc-Bares</h1>
        <p className="header__subtitle">
          Los mejores <span className="header__highlight">bares</span> y restaurantes
        </p>
      </header>

      {/* Error state */}
      {error && (
        <div className="error">
          <strong>Ups!</strong> {error}
        </div>
      )}

      {/* Controls */}
      <div className="controls">
        <button 
          className="btn btn-primary" 
          onClick={handleLoadMore}
          disabled={loadingMore || limit >= 50 || noMorePlaces}
        >
          <span className="btn__icon">➕</span>
          {loadingMore ? 'Buscando...' : noMorePlaces ? 'No hay más' : 'Cargar más'}
        </button>
        
        <button 
          className="btn btn-danger" 
          onClick={handleDelete}
          disabled={deleting || places.length === 0}
        >
          <span className="btn__icon">🗑️</span>
          {deleting ? 'Borrando...' : 'Limpiar'}
        </button>
      </div>

      {/* No more places message */}
      {noMorePlaces && (
        <div className="info-message">
          🏁 Ya no hay restaurantes nuevos para mostrar. Todos los resultados adicionales ya están en la lista.
        </div>
      )}

      {/* Counter */}
      <div className="count">
        {places.length > 0 
          ? `Mostrando ${places.length} lugares` 
          : 'Sin resultados aún'}
      </div>

      {/* Loading state */}
      {loading && places.length === 0 ? (
        <div className="loading">
          <div className="loading__spinner"></div>
          Buscando lugares...
        </div>
      ) : places.length === 0 ? (
        /* Empty state */
        <div className="empty">
          <span className="empty__icon">🍻</span>
          No hay lugares.{' '}
          <button className="link" onClick={() => loadPlaces(10)}>
            Cargar ahora
          </button>
        </div>
      ) : (
        /* Places grid */
        <div className="places">
          {places.map((place, index) => (
            <article 
              key={place.id} 
              className={`place-card ${index < 3 && place.rating && place.rating >= 4.5 ? 'featured' : ''}`}
            >
              <button 
                className="place-delete-btn"
                onClick={() => handleDeleteOne(place.id)}
                disabled={deletingId === place.id}
                title="Borrar este lugar"
              >
                {deletingId === place.id ? '⏳' : '✕'}
              </button>
              
              <div className="place-emoji-large">
                {getCategoryEmoji(place.category)}
              </div>
              
              <h2 className="place-name">{place.name}</h2>
              
              <span className="place-category">
                {getCategoryLabel(place.category)}
              </span>
              
              <p className="place-address">{place.address}</p>
              
              {place.rating && (
                <div className="place-rating">
                  <span className="rating-value">{place.rating.toFixed(1)}</span>
                  <span className="rating-stars">⭐</span>
                </div>
              )}
            </article>
          ))}
        </div>
      )}

      {/* Chat toggle button */}
      <button 
        className="chat-toggle"
        onClick={() => setChatOpen(!chatOpen)}
      >
        💬
      </button>
      
      {/* Chat panel */}
      {chatOpen && (
        <div className="chat-panel">
          <div className="chat-header">
            <h3>Asistente</h3>
            <button onClick={() => setChatOpen(false)}>✕</button>
          </div>
          
          <div className="chat-messages">
            {chatMessages.length === 0 && (
              <div className="chat-message assistant">
                Hola! Preguntame sobre restaurantes, bares o cafeterías en Tucumán! 🍻
              </div>
            )}
            {chatMessages.map((msg, i) => (
              <div key={i} className={`chat-message ${msg.role}`}>
                {msg.content}
              </div>
            ))}
            {chatLoading && (
              <div className="chat-message assistant">
                <span className="typing">Escribiendo...</span>
              </div>
            )}
          </div>
          
          <form className="chat-input" onSubmit={(e) => { e.preventDefault(); handleChatSubmit(); }}>
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Preguntame sobre restaurantes..."
              disabled={chatLoading}
            />
            <button type="submit" disabled={chatLoading || !chatInput.trim()}>
              ➤
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;