

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [boats, setBoats] = useState({});

  useEffect(() => {
    const fetchBoats = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/boats');
        const data = await response.json();
        setBoats(data);
      } catch (error) {
        console.error('Failed to fetch boat positions:', error);
      }
    };

    fetchBoats();
    const interval = setInterval(fetchBoats, 5000); // Fetch every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Boat Positions</h1>
        <ul>
          {Object.entries(boats).map(([id, position]) => (
            <li key={id}>Boat {id}: {position.join(', ')}</li>
          ))}
        </ul>
      </header>
    </div>
  );
} 

export default App;
