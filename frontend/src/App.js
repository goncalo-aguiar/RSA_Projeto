import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const rows = 15;  // Example, adjust based on your actual data
  const cols = 30;  // Example, adjust based on your actual data
  const side = 50;  // Cell size in pixels
  const [boats, setBoats] = useState([]);
  const [trash, setTrash] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/boats_buoys');
        const data = await response.json();
        setBoats(Object.entries(data).map(([id, [type, position]]) => ({ id, type, position })));

        const trashResponse = await fetch('http://localhost:8080/api/trash');
        const trashData = await trashResponse.json();
        setTrash(Object.entries(trashData).map(([id, [type,trashLocation]]) => ({ id, type,trashLocation })));
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 1000); // Fetch every 5 seconds

    return () => clearInterval(interval);
  }, []);

  // Function to create the grid with boats, buoys, and trash
  const createGrid = () => {
    const grid = [];
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const foundBoats = boats.filter(boat => boat.position[0] === j && boat.position[1] === i);
        const foundTrash = trash.filter(tr => tr.trashLocation[0] === j && tr.trashLocation[1] === i);

        const cell = (
          <div key={`${i}-${j}`} style={{ width: side, height: side, border: '1px solid black', position: 'absolute', top: i * side, left: j * side }}>
            {/* Rendering boats and buoys */}
            {foundBoats.map(boat => (
              <div key={boat.id} style={{ width: '100%', height: '100%', backgroundColor: boat.type === 'boat' ? 'blue' : 'red', display: 'flex', justifyContent: 'center', alignItems: 'center', color: 'white' }}>
                {boat.type} {boat.id}
              </div>
            ))}
            {/* Rendering trash */}
            {foundTrash.map(tr => (
              <div key={tr.id} style={{ width: '100%', height: '100%', backgroundColor: 'grey', display: 'flex', justifyContent: 'center', alignItems: 'center', color: 'white' }}>
                Trash {tr.id}
              </div>
            ))}
          </div>
        );
        grid.push(cell);
      }
    }
    return grid;
  };

  return (
    <div className="App">
      <header className="App-header">
        <div style={{ position: 'relative', width: cols * side, height: rows * side }}>
          {createGrid()}
        </div>
      </header>
    </div>
  );
}

export default App;