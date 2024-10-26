import React, { useEffect, useState } from 'react';
import RailNetwork from './RailNetwork';

function App() {
  const [rails, setRails] = useState([]);

  useEffect(() => {
    // Получаем данные рельсов с бэкенда
    fetch(`${process.env.REACT_APP_API_URL}/rails`)
      .then((response) => response.json())
      .then((data) => {
        // Преобразуем координаты в числа
        const processedData = data.map((rail) => ({
          ...rail,
          coordinates: {
            x1: Number(rail.coordinates.x1),
            y1: Number(rail.coordinates.y1),
            x2: Number(rail.coordinates.x2),
            y2: Number(rail.coordinates.y2),
          },
        }));
        setRails(processedData);
      })
      .catch((error) => console.error('Error fetching rails:', error));

    // Подключаемся к WebSocket для обновлений в реальном времени
    const socket = new WebSocket(`ws://localhost:8000/ws`);

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'update') {
        setRails((prevRails) =>
          prevRails.map((rail) =>
            rail.id === message.rail_id ? { ...rail, status: message.status } : rail
          )
        );
      }
    };

    socket.onclose = (event) => {
      console.warn('WebSocket closed:', event);
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="App">
      <h1>Rail Network</h1>
      <RailNetwork rails={rails} />
    </div>
  );
}

export default App;
