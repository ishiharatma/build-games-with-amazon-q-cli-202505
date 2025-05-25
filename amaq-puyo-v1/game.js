// Game constants
const COLS = 6;
const ROWS = 12;
const BLOCK_SIZE = 40;
const COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00']; // Red, Green, Blue, Yellow

// Game variables
let board = [];
let score = 0;
let currentPiece = null;
let nextPiece = null;
let gameInterval = null;
let gameOver = false;

// Canvas setup
const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const nextCanvas = document.getElementById('next-canvas');
const nextCtx = nextCanvas.getContext('2d');
const scoreElement = document.getElementById('score');
const startButton = document.getElementById('start-button');

// Initialize the game board
function initBoard() {
    board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
}

// Create a new piece
function createPiece() {
    // In Puyo Puyo, pieces are typically pairs of colored blobs
    const color1 = Math.floor(Math.random() * COLORS.length);
    const color2 = Math.floor(Math.random() * COLORS.length);
    
    return {
        // Position of the main blob (the one that others are attached to)
        x: Math.floor(COLS / 2),
        y: 0,
        // The second blob is below the first one initially
        shape: [
            { x: 0, y: 0, color: color1 },
            { x: 0, y: 1, color: color2 }
        ],
        rotation: 0
    };
}

// Draw a single block
function drawBlock(ctx, x, y, colorIndex) {
    const color = COLORS[colorIndex];
    
    // Draw the main block
    ctx.fillStyle = color;
    ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
    
    // Draw highlight (lighter shade)
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE / 2);
    ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE / 2, BLOCK_SIZE);
    
    // Draw outline
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
}

// Draw the game board
function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw the placed blocks
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            if (board[y][x] !== 0) {
                drawBlock(ctx, x, y, board[y][x] - 1);
            }
        }
    }
    
    // Draw the current piece
    if (currentPiece) {
        currentPiece.shape.forEach(block => {
            const x = currentPiece.x + block.x;
            const y = currentPiece.y + block.y;
            drawBlock(ctx, x, y, block.color);
        });
    }
}

// Draw the next piece preview
function drawNextPiece() {
    nextCtx.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
    
    if (nextPiece) {
        nextPiece.shape.forEach(block => {
            const x = block.x + 1;  // Center in the preview
            const y = block.y + 1;
            drawBlock(nextCtx, x, y, block.color);
        });
    }
}

// Check if the current position is valid
function isValidMove(piece, offsetX = 0, offsetY = 0) {
    return piece.shape.every(block => {
        const x = piece.x + block.x + offsetX;
        const y = piece.y + block.y + offsetY;
        
        // Check boundaries
        if (x < 0 || x >= COLS || y < 0 || y >= ROWS) {
            return false;
        }
        
        // Check if the position is already occupied
        if (y >= 0 && board[y][x] !== 0) {
            return false;
        }
        
        return true;
    });
}

// Rotate the current piece
function rotatePiece() {
    if (!currentPiece) return;
    
    const rotated = {
        ...currentPiece,
        shape: currentPiece.shape.map(block => {
            // Rotate 90 degrees clockwise around the first block
            return {
                x: -block.y,
                y: block.x,
                color: block.color
            };
        }),
        rotation: (currentPiece.rotation + 1) % 4
    };
    
    // Check if the rotation is valid
    if (isValidMove(rotated)) {
        currentPiece = rotated;
    }
}

// Lock the current piece in place
function lockPiece() {
    currentPiece.shape.forEach(block => {
        const x = currentPiece.x + block.x;
        const y = currentPiece.y + block.y;
        
        if (y >= 0) {
            board[y][x] = block.color + 1; // +1 because 0 means empty
        }
    });
}

// Check for and remove connected groups
function checkConnections() {
    // Create a visited array
    const visited = Array.from({ length: ROWS }, () => Array(COLS).fill(false));
    let totalRemoved = 0;
    
    // Function to find connected blobs of the same color
    function findConnectedGroup(row, col, color, group = []) {
        // Out of bounds or already visited or different color
        if (row < 0 || row >= ROWS || col < 0 || col >= COLS || 
            visited[row][col] || board[row][col] !== color) {
            return group;
        }
        
        visited[row][col] = true;
        group.push({ row, col });
        
        // Check all four directions
        findConnectedGroup(row + 1, col, color, group); // down
        findConnectedGroup(row - 1, col, color, group); // up
        findConnectedGroup(row, col + 1, color, group); // right
        findConnectedGroup(row, col - 1, color, group); // left
        
        return group;
    }
    
    // Check the entire board
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            if (!visited[row][col] && board[row][col] !== 0) {
                const color = board[row][col];
                const group = findConnectedGroup(row, col, color);
                
                // If we have 4 or more connected blobs of the same color
                if (group.length >= 4) {
                    // Remove the connected blobs
                    group.forEach(pos => {
                        board[pos.row][pos.col] = 0;
                    });
                    
                    totalRemoved += group.length;
                    score += group.length * 10;
                }
            }
        }
    }
    
    return totalRemoved;
}

// Apply gravity to make blocks fall
function applyGravity() {
    let moved = false;
    
    // Start from the bottom row and move up
    for (let col = 0; col < COLS; col++) {
        for (let row = ROWS - 2; row >= 0; row--) {
            if (board[row][col] !== 0 && board[row + 1][col] === 0) {
                // Move the block down
                board[row + 1][col] = board[row][col];
                board[row][col] = 0;
                moved = true;
            }
        }
    }
    
    return moved;
}

// Move the current piece down
function moveDown() {
    if (!currentPiece) return false;
    
    if (isValidMove(currentPiece, 0, 1)) {
        currentPiece.y++;
        return true;
    } else {
        // Lock the piece in place
        lockPiece();
        
        // Check for game over
        if (currentPiece.y <= 0) {
            gameOver = true;
            clearInterval(gameInterval);
            alert('Game Over! Your score: ' + score);
            return false;
        }
        
        // Check for connections and apply gravity until no more moves
        let connectionsFound;
        do {
            connectionsFound = checkConnections() > 0;
            
            // Apply gravity until no more blocks fall
            let gravityApplied;
            do {
                gravityApplied = applyGravity();
            } while (gravityApplied);
            
        } while (connectionsFound);
        
        // Update the score display
        scoreElement.textContent = score;
        
        // Get the next piece
        currentPiece = nextPiece;
        nextPiece = createPiece();
        drawNextPiece();
        
        return false;
    }
}

// Move the current piece left or right
function moveHorizontal(dir) {
    if (!currentPiece) return;
    
    if (isValidMove(currentPiece, dir, 0)) {
        currentPiece.x += dir;
    }
}

// Hard drop the current piece
function hardDrop() {
    if (!currentPiece) return;
    
    while (moveDown()) {
        // Keep moving down until it can't move anymore
    }
}

// Game loop
function gameLoop() {
    moveDown();
    drawBoard();
}

// Handle keyboard input
document.addEventListener('keydown', (e) => {
    if (gameOver) return;
    
    switch (e.key) {
        case 'ArrowLeft':
            moveHorizontal(-1);
            break;
        case 'ArrowRight':
            moveHorizontal(1);
            break;
        case 'ArrowUp':
            rotatePiece();
            break;
        case 'ArrowDown':
            moveDown();
            break;
        case ' ':
            hardDrop();
            break;
    }
    
    drawBoard();
});

// Start the game
startButton.addEventListener('click', () => {
    // Reset game state
    initBoard();
    score = 0;
    gameOver = false;
    scoreElement.textContent = '0';
    
    // Clear any existing interval
    if (gameInterval) {
        clearInterval(gameInterval);
    }
    
    // Create the first pieces
    currentPiece = createPiece();
    nextPiece = createPiece();
    
    // Start the game loop
    gameInterval = setInterval(gameLoop, 500);
    
    // Initial draw
    drawBoard();
    drawNextPiece();
    
    // Focus on the canvas for keyboard input
    canvas.focus();
});

// Initialize the game
initBoard();
drawBoard();
drawNextPiece();
