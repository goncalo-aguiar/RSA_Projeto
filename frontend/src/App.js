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
  const [buoyStatus, setBuoyStatus] = useState({});
  const [cleanedMessage, setCleanedMessage] = useState('');

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

        // Atualiza o status das boias
        const newBuoyStatus = {};
        trash.forEach(({ id, trashLocation }) => {
          newBuoyStatus[id] = trashLocation.length === 0 ? 'clean' : 'dirty';
        });
        setBuoyStatus(newBuoyStatus);

        // Verifica se o trash foi limpo
        trash.forEach(({ id, trashLocation }) => {
          console.log(buoyStatus[id])
          if (trashLocation.length === 0 && buoyStatus[id] === 'dirty') {
            setCleanedMessage(`Boia ${id} foi limpa!`);
            setTimeout(() => {
              setCleanedMessage('');
            }, 3000);
          }
        });



      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 600); // Fetch every 5 seconds

    return () => clearInterval(interval);
  }, [trash, buoyStatus]);

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
                    top: -side * 5,
                    left: -side * 5,
                    width: side * 11,
                    height: side * 11,
                    borderRadius: '50%',
                    border: '3px dashed rgba(154, 205, 50, 1)',
                    pointerEvents: 'none',
                  }}
                />
                {`${boat.type} ${boat.id}`}
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
                Lixo {tr.id}
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
          {cleanedMessage && <div style={{ position: 'absolute', top: '-65px', left: '50%', transform: 'translateX(-50%)', backgroundColor: 'green', color: 'white', padding: '5px', borderRadius: '5px' }}>{cleanedMessage}</div>}
        </div>
      </header>
    </div>
  );
}

export default App;
