import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const rows = 15;
  const cols = 30;
  const side = 50;
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
    const interval = setInterval(fetchData, 200); // Fetch every 5 seconds

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
              backgroundColor: isVisited ? 'grey' : 'light_blue', // Set background color based on visited status
            }}
          >
            {foundBoats.map(boat => (
              <React.Fragment key={boat.id}>
                <div
                  style={{
                    width: '100%',
                    height: '100%',
                    backgroundColor: boat.type === 'boat' ? 'blue' : 'red',
                    borderRadius: '50%',
                    position: 'relative',
                  }}
                >
                  {`${boat.type} ${boat.id} ${boat.intention}`}
                  <div
                    style={{
                      position: 'absolute',
                      top: -side * 4,
                      left: -side * 4,
                      width: side * 9,
                      height: side * 9,
                      borderRadius: '50%',
                      border: '1px dashed rgba(0, 128, 0, 0.5)',
                      pointerEvents: 'none',
                    }}
                  ></div>
                </div>
              </React.Fragment>
            ))}
            {foundBuoys.map(buoy => (
              <React.Fragment key={buoy.id}>
                <div
                  style={{
                    width: '100%',
                    height: '100%',
                    backgroundColor: buoy.type === 'boat' ? 'blue' : 'red',
                    borderRadius: '50%',
                    position: 'relative',
                  }}
                >
                  {`${buoy.type} ${buoy.id}`}
                  <div
                    style={{
                      position: 'absolute',
                      top: -side * 4,
                      left: -side * 4,
                      width: side * 9,
                      height: side * 9,
                      borderRadius: '50%',
                      border: '1px dashed rgba(0, 128, 0, 0.5)',
                      pointerEvents: 'none',
                    }}
                  ></div>
                </div>
              </React.Fragment>
            ))}
            {foundTrash.map(tr => (
              <div
                key={tr.id}
                style={{
                  width: '100%',
                  height: '100%',
                  backgroundColor: 'grey',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  color: 'white',
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

