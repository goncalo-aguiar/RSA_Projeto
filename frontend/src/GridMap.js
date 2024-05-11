import React, { useRef, useEffect } from 'react';

function GridMap({ boats }) {
    const canvasRef = useRef(null);
    const scale = 20; // Scale factor to enlarge the boat and buoy positions

    const draw = (ctx) => {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); // Clear the canvas
        ctx.fillStyle = '#0000FF'; // Blue color for boats

        Object.entries(boats).forEach(([id, [type, position]]) => {
            ctx.beginPath(); // Start drawing a shape
            // Multiply position coordinates by the scale factor
            ctx.arc(position[0] * scale, position[1] * scale, 10, 0, 2 * Math.PI); // Draw a circle for each boat
            ctx.fill();
        });
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        let animationFrameId;

        // Animation loop
        const render = () => {
            draw(context);
            animationFrameId = window.requestAnimationFrame(render);
        };
        render();
        
        return () => {
            window.cancelAnimationFrame(animationFrameId);
        };
    }, [boats]);

    return <canvas ref={canvasRef} width={1000} height={1000} style={{ backgroundColor: 'lightblue' }} />;
}

export default GridMap;