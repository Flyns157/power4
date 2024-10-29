const boardElement = document.getElementById('board');
const currentPlayerElement = document.getElementById('current-player');
const ROWS = 6;
const COLUMNS = 7;
let currentPlayer = 1;
function createBoard() {
    boardElement.innerHTML = '';
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLUMNS; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = row;
            cell.dataset.col = col;
            cell.addEventListener('click', () => makeMove(col));
            boardElement.appendChild(cell);
        }
    }
}
function updateBoard(board) {
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLUMNS; col++) {
            const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
            cell.classList.remove('player1', 'player2');
            if (board[row][col] === 1) cell.classList.add('player1');
            else if (board[row][col] === 2) cell.classList.add('player2');
        }
    }
}
function makeMove(col) {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ column: col })
    })
    .then(response => response.json())
    .then(data => {
        if (data.winner) {
            alert(`Joueur ${data.winner} a gagné !`);
            createBoard();
        } else if (data.board) {
            updateBoard(data.board);
            currentPlayer = data.current_player;
            currentPlayerElement.textContent = currentPlayer;
        } else if (data.error) {
            alert(data.error);
        }
    });
}
createBoard();
