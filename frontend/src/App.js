import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const rows = 50;
  const cols = 101;
  const side = 15;
  const [boats, setBoats] = useState([]);
  const [buoys, setBuoys] = useState([]);
  const [trash, setTrash] = useState([]);
  const [visited, setVisited] = useState([]);

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

        const responseVisited = await fetch('http://localhost:8080/api/visited');
        const visitedData = await responseVisited.json();
        setVisited(visitedData);

      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 1000); // Fetch every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const createGrid = () => {
    const grid = [];
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const foundBuoys = buoys.filter(buoy => buoy.position[0] === j && buoy.position[1] === i);
        const foundBoats = boats.filter(boat => boat.position[0] === j && boat.position[1] === i);
        const foundTrash = trash.filter(tr => tr.trashLocation[0] === j && tr.trashLocation[1] === i);
        const isVisited = visited.some(location => location[0] === j && location[1] === i); // Check if current cell is in visited list

        const cell = (
          <div
            key={`${i}-${j}`}
            style={{
              width: side,
              height: side,
              border: '1px solid black',
              position: 'absolute',
              top: i * side,
              left: j * side,
              backgroundColor: isVisited ? 'grey' : '#282c34', // Set background color based on visited status
            }}
          >
            {foundBoats.map(boat => (
              <div
                key={boat.id}
                style={{
                  width: '100%',
                  height: '100%',
                  backgroundColor: boat.type === 'boat' ? 'blue' : 'red',
                  borderRadius: '50%',
                  position: 'relative',
                  zIndex: 2, // Ensure boat is on top
                }}
              >
                <div
                  style={{
                    position: 'absolute',
                    top: -side * 4,
                    left: -side * 4,
                    width: side * 9,
                    height: side * 9,
                    borderRadius: '50%',
                    border: '3px dashed rgba(154, 205, 50, 1)',
                    pointerEvents: 'none',
                  }}
                />
                {`${boat.type} ${boat.id} ${boat.intention}`}
              </div>
            ))}
            {foundBuoys.map(buoy => (
              <div
                key={buoy.id}
                style={{
                  width: '100%',
                  height: '100%',
                  backgroundColor: buoy.type === 'boat' ? 'blue' : 'red',
                  borderRadius: '50%',
                  position: 'relative',
                  zIndex: 2, // Ensure buoy is on top
                }}
              >
                <div
                  style={{
                    position: 'absolute',
                    top: -side * 4,
                    left: -side * 4,
                    width: side * 9,
                    height: side * 9,
                    borderRadius: '50%',
                    border: '3px dashed rgba(238, 130, 238, 1)',
                    pointerEvents: 'none',
                  }}
                />
                {`${buoy.type} ${buoy.id}`}
              </div>
            ))}
            {foundTrash.map(tr => (
              <div
                key={tr.id}
                style={{
                  width: '100%',
                  height: '100%',
                  backgroundColor: 'yellow',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  color: 'white',
                  zIndex: 2, // Ensure trash is on top
                }}
              >
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
