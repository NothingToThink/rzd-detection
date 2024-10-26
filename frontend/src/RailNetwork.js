import React from 'react';
import Rail from './Rail';

const RailNetwork = ({ rails }) => {
  const networkStyle = {
    position: 'relative',
    width: '100%',
    height: '600px',
    backgroundColor: '#ecf0f1',
  };

  // Создаём копию массива рельсов
  const sortedRails = [...rails];

  // Сортируем рельсы: рельс с ID '3' будет последним
  sortedRails.sort((a, b) => {
    if (a.id === '3') return 1;
    if (b.id === '3') return -1;
    return 0;
  });

  return (
    <div style={networkStyle}>
      {sortedRails.map((rail) => (
        <Rail
          key={rail.id}
          id={rail.id}
          x1={rail.coordinates.x1}
          y1={rail.coordinates.y1}
          x2={rail.coordinates.x2}
          y2={rail.coordinates.y2}
          status={rail.status}
          is_curve={rail.is_curve || false}
        />
      ))}
    </div>
  );
};

export default RailNetwork;
