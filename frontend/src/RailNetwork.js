import React from "react";
import Rail from "./Rail";

const RailNetwork = ({ rails }) => {
  return (
    <svg width="800" height="600">
      {rails.map((rail) => (
        <Rail key={rail.id} rail={rail} />
      ))}
    </svg>
  );
};

export default RailNetwork;
