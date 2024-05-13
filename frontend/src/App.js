import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const rows = 15;  // Example, adjust based on your actual data
  const cols = 30;  // Example, adjust based on your actual data
  const side = 50;  // Cell size in pixels
  const [boats, setBoats] = useState([]);
  const [buoys, setBuoys] = useState([]);
  const [trash, setTrash] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const responseBuoys = await fetch('http://localhost:8080/api/buoys');
        const buoyData = await responseBuoys.json();
        setBuoys(Object.entries(buoyData).map(([id, [type, position]]) => ({ id, type, position })));

        const responseBoats = await fetch('http://localhost:8080/api/boats');
        const boatData = await responseBoats.json();
        setBoats(Object.entries(boatData).map(([id, [type, position, intention]]) => ({ id, type, position, intention })));

        const responseTrash = await fetch('http://localhost:8080/api/trash');
        const trashData = await responseTrash.json();
        setTrash(Object.entries(trashData).map(([id, [type, trashLocation]]) => ({ id, type, trashLocation })));
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 200); // Fetch every 5 seconds

    return () => clearInterval(interval);
  }, []);

  // Function to create the grid with boats, buoys, and trash
  const createGrid = () => {
    const grid = [];
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const foundBuoys = buoys.filter(buoy => buoy.position[0] === j && buoy.position[1] === i);
        const foundBoats = boats.filter(boat => boat.position[0] === j && boat.position[1] === i);
        const foundTrash = trash.filter(tr => tr.trashLocation[0] === j && tr.trashLocation[1] === i);
  
        const cell = (
          <div key={`${i}-${j}`} style={{ width: side, height: side, border: '1px solid black', position: 'absolute', top: i * side, left: j * side }}>
            {/* Rendering boats and buoys */}
            {foundBoats.map(boat => (
              <React.Fragment key={boat.id}>
                <div style={{ width: '100%', height: '100%', backgroundColor: boat.type === 'boat' ? 'blue' : 'red', borderRadius: '50%', position: 'relative' }}>
                  {`${boat.type} ${boat.id} ${boat.intention}`} {/* Displaying boat intention */}
                  {/* Circle representing the range */}
                  <div style={{ position: 'absolute', top: -side * 4, left: -side * 4, width: side * 9, height: side * 9, borderRadius: '50%', border: '1px dashed rgba(0, 128, 0, 0.5)', pointerEvents: 'none' }}></div>
                </div>
              </React.Fragment>
            ))}
            {foundBuoys.map(buoy => (
              <React.Fragment key={buoy.id}>
                <div style={{ width: '100%', height: '100%', backgroundColor: buoy.type === 'boat' ? 'blue' : 'red', borderRadius: '50%', position: 'relative' }}>
                  {`${buoy.type} ${buoy.id}`}
                  {/* Circle representing the range */}
                  <div style={{ position: 'absolute', top: -side * 4, left: -side * 4, width: side * 9, height: side * 9, borderRadius: '50%', border: '1px dashed rgba(0, 128, 0, 0.5)', pointerEvents: 'none' }}></div>
                </div>
              </React.Fragment>
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