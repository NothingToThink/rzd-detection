import React, { useEffect, useState } from "react";
import RailNetwork from "./RailNetwork";

function App() {
  const [rails, setRails] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/rails`)
      .then((response) => response.json())
      .then((data) => setRails(data))
      .catch((error) => console.error("Error fetching rails:", error));
  }, []);

  return (
    <div className="App">
      <h1>Rail Network</h1>
      <RailNetwork rails={rails} />
    </div>
  );
}

export default App;
