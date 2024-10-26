import React from "react";

const Rail = ({ rail }) => {
  const colorMap = {
    default: "gray",
    active: "green",
    inactive: "red",
  };

  const handleClick = () => {
    const newStatus = rail.status === "active" ? "inactive" : "active";

    fetch(`${process.env.REACT_APP_API_URL}/rails/${rail.id}/status?status=${newStatus}`, {
      method: "PUT",
    })
      .then(() => {
        // Обновление статуса локально (опционально)
        rail.status = newStatus;
      })
      .catch((error) => console.error("Error updating rail status:", error));
  };

  return (
    <line
      x1={rail.coordinates.x1}
      y1={rail.coordinates.y1}
      x2={rail.coordinates.x2}
      y2={rail.coordinates.y2}
      stroke={colorMap[rail.status]}
      strokeWidth={5}
      onClick={handleClick}
      style={{ cursor: "pointer" }}
    >
      <title>{`Rail ID: ${rail.id}`}</title>
    </line>
  );
};

export default Rail;
