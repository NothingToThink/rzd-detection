import React from 'react';

const Rail = ({ id, x1, y1, x2, y2, status, is_curve }) => {
  const x1Num = Number(x1);
  const y1Num = Number(y1);
  const x2Num = Number(x2);
  const y2Num = Number(y2);

  if (
    isNaN(x1Num) ||
    isNaN(y1Num) ||
    isNaN(x2Num) ||
    isNaN(y2Num)
  ) {
    console.error(`Invalid coordinates: x1=${x1}, y1=${y1}, x2=${x2}, y2=${y2}`);
    return null;
  }

  const minX = Math.min(x1Num, x2Num);
  const minY = Math.min(y1Num, y2Num);
  const maxX = Math.max(x1Num, x2Num);
  const maxY = Math.max(y1Num, y2Num);
  const padding = 50;
  const width = maxX - minX + padding * 2;
  const height = maxY - minY + padding * 2;
  const offsetX = minX - padding;
  const offsetY = minY - padding;

  let railColor = '#7f8c8d';
  if (status === 'inactive') {
    railColor = 'green';
  } else if (status === 'active' || status === 'red') {
    railColor = 'red';
  }

  // Обработчик клика для изменения статуса
  const handleClick = () => {
    fetch(`${process.env.REACT_APP_API_URL}/rails/${id}/status?status=red`, {
      method: 'PUT',
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Status updated:', data);
      })
      .catch((error) => console.error('Error updating status:', error));
  };

  if (is_curve) {
    //console.log("hello world")
    // Вычисляем контрольные точки для кривой
    const controlPoint1 = {
      x: x1Num,
      y: y1Num - Math.abs(y2Num - y1Num) / 3
    };
    const controlPoint2 = {
      x: x2Num,// + (x2Num - x1Num) * 0.5,
      y: y2Num - Math.abs(y2Num - y1Num) / 3,
    };

    return (
      <svg
        width={width}
        height={height}
        style={{
          position: 'absolute',
          left: `${offsetX}px`,
          top: `${offsetY}px`,
        }}
        onClick={handleClick}
      >
        <path
          d={`
            M ${x1Num - offsetX} ${y1Num - offsetY}
            C ${controlPoint1.x - offsetX} ${controlPoint1.y - offsetY}, ${controlPoint2.x - offsetX} ${controlPoint2.y - offsetY}, ${x2Num - offsetX} ${y2Num - offsetY}
          `}
          stroke={railColor}
          strokeWidth="10"
          fill="none"
        />
        {/* Добавьте дополнительные элементы, такие как шпалы, если необходимо */}
      </svg>
    );
  } else {
    //console.log("SDJASKDHAS;DJAHDJKSHSALKDHDSLKJ\n")
    // Рисуем прямую линию
    return (
      <svg
        width={width}
        height={height}
        style={{
          position: 'absolute',
          left: `${offsetX}px`,
          top: `${offsetY}px`,
        }}
        onClick={handleClick}
      >
        <line
          x1={x1Num - offsetX}
          y1={y1Num - offsetY}
          x2={x2Num - offsetX}
          y2={y2Num - offsetY}
          stroke={railColor}
          strokeWidth="10"
        />
        {/* Добавьте балки, шпалы и другие элементы */}
      </svg>
    );
  }
};

export default Rail;
