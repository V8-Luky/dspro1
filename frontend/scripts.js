let data = [];
let lastGuess = null;


async function initializeGame() {
    try {
        // Fetch all games
        const allGamesResponse = await fetchGames();
        data = allGamesResponse.games // Populate the data array

    } catch (error) {
        console.error("Error initializing the game:", error);
    }
}

// Initialize the game
initializeGame();

const congratsModal = document.getElementById("congratsModal");
const closeModal = document.getElementById("closeModal");
const guessButton = document.getElementById("guessButton");
const guessInput = document.getElementById("guessInput");
const dropdown = document.createElement("div");
const menuIcon = document.getElementById("menuIcon");
const dropdownMenu = document.getElementById("dropdownMenu");

dropdown.id = "autocompleteDropdown";
dropdown.classList.add("dropdown");
document.body.appendChild(dropdown);

// Handle suggestions for input field
guessInput.addEventListener("input", () => {
    const userInput = guessInput.value.trim().toLowerCase();
    if (userInput.length >= 3) {
        showSuggestions(userInput);
    } else {
        dropdown.style.display = "none";
    }
});

// Handle submit button click
guessButton.addEventListener("click", async () => {
    if (guessButton.disabled) return;

    // Trigger the guess submission with the first match
    await submitFirstMatchingGame();
});

// Handle enter keydown event on input field
guessInput.addEventListener("keydown", async (event) => {
    if (event.key === "Enter") {

        if (guessButton.disabled) return;

        // Trigger the guess submission with the first match
        await submitFirstMatchingGame();
    }
});

// Toggle dropdown visibility
menuIcon.addEventListener("click", () => {
    dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
});

// Close dropdown when clicking outside
document.addEventListener("click", (event) => {
    if (!menuIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.style.display = "none";
    }
});

function processFeedback(feedback) {
    const tableBody = document.getElementById("guessTableBody");
    const row = document.createElement("tr");

    // Name Cell
    const nameCell = document.createElement("td");
    nameCell.innerHTML = feedback.name; // Display the guessed name
    nameCell.classList.add(feedback.is_correct ? "correct" : "incorrect"); // Green if correct
    row.appendChild(nameCell);

    // Genres Cell
    const genresCell = createMatchMismatchCell(feedback.genres);
    row.appendChild(genresCell);

    // Categories Cell
    const categoriesCell = createMatchMismatchCell(feedback.categories);
    row.appendChild(categoriesCell);

    // Tags Cell
    const tagsCell = createMatchMismatchCell(feedback.tags);
    row.appendChild(tagsCell);

    // Developers Cell
    const developersCell = createMatchMismatchCell(feedback.developers);
    row.appendChild(developersCell);

    // Publishers Cell
    const publishersCell = createMatchMismatchCell(feedback.publishers);
    row.appendChild(publishersCell);

    // Release Date Cell
    const releaseDateCell = createReleaseDateCell(feedback.release_date);
    row.appendChild(releaseDateCell);

    const similarityCell = createSimilarityCell(feedback.similarity);
    row.appendChild(similarityCell);

    tableBody.prepend(row);

    if (feedback.is_correct) {
        showCongratsModal();
    }
}

// Helper function to create cells for match/mismatch
function createMatchMismatchCell(data) {
    const cell = document.createElement("td");

    const matchItems = data.match.map(
        item => `<span class="correct">${item}</span>`
    ).join(", ");

    const mismatchItems = data.mismatch.map(
        item => `<span class="incorrect">${item}</span>`
    ).join(", ");

    let cellContent = "";

    if (matchItems && mismatchItems) {
        // Both matchItems and mismatchItems are not empty
        cellContent = `${matchItems}, ${mismatchItems}`;
    } else if (matchItems) {
        // Only matchItems is not empty
        cellContent = `${matchItems}`;
    } else if (mismatchItems) {
        // Only mismatchItems is not empty
        cellContent = `${mismatchItems}`;
    } else {
        cellContent = "";
    }

    cell.innerHTML = cellContent;
    return cell;
}


// Helper function to create the release date cell
function createReleaseDateCell(releaseData) {
    const cell = document.createElement("td");

    const guessedDate = releaseData.guessed || "N/A";
    const arrowDirection = releaseData.target_direction === 1 ? "↓" : "↑";

    const dateText = releaseData.target_direction !== 0
        ?`<span class = incorrect>${guessedDate}</span>`
        :`<span class = correct>${guessedDate}</span>`;
    const arrow = releaseData.target_direction !== 0
        ? `<span style="color: red;">${arrowDirection}</span>`
        : "";

    cell.innerHTML = `${dateText} ${arrow}`;
    return cell;
}

function createSimilarityCell(similarity) {
    const cell = document.createElement("td");
    const color = getSimilarityColor(similarity);

    // Styling for the cell background and text
    cell.style.background = color;
    cell.style.color = "black";
    cell.style.textAlign = "center";
    cell.style.fontWeight = "bold";
    cell.textContent = `${(similarity * 100).toFixed(1)}%`; // Display percentage

    return cell;
}

function getSimilarityColor(similarity) {
    const brightnessFactor = 0.7;

    if (similarity <= 0.5) {
        // Transition from red to yellow
        const red = Math.floor(255 * brightnessFactor);
        const green = Math.floor(255 * (similarity / 0.5) * brightnessFactor);
        return `rgb(${red}, ${green}, 0)`;
    } else {
        // Transition from yellow to green
        const red = Math.floor(255 * ((1 - similarity) / 0.5) * brightnessFactor);
        const green = Math.floor(255 * brightnessFactor);
        return `rgb(${red}, ${green}, 0)`;
    }
}


// Show autocomplete suggestions
function showSuggestions(input) {
    const matches = data
        .filter(name => name.trim().toLowerCase().includes(input)) // Case-insensitive matching
        .slice(0, 10); // Limit to the first 10 matches

    dropdown.innerHTML = "";

    if (matches.length === 0) {
        dropdown.style.display = "none";
        return;
    }

    const inputRect = guessInput.getBoundingClientRect();
    dropdown.style.left = `${inputRect.left}px`;
    dropdown.style.top = `${inputRect.bottom}px`;
    dropdown.style.width = `${inputRect.width}px`;
    dropdown.style.display = "block";

    // Populate dropdown with matching game names
    matches.forEach(match => {
        const suggestionItem = document.createElement("div");
        suggestionItem.classList.add("suggestion-item");
        suggestionItem.textContent = match.trim();

        // When a suggestion is clicked, fill the input field and hide the dropdown
        suggestionItem.addEventListener("click", () => {
            guessInput.value = match.trim();
            dropdown.style.display = "none";
        });
        dropdown.appendChild(suggestionItem);
    });
}

// Show modal and trigger confetti animation
function showCongratsModal() {
    congratsModal.style.display = "flex";
    triggerConfetti();
    disableSubmitButton();
}

// Close modal functionality
closeModal.addEventListener("click", () => {
    congratsModal.style.display = "none";
});

window.addEventListener("click", (event) => {
    if (event.target === congratsModal) {
        congratsModal.style.display = "none";
    }
});

// Trigger confetti animation
function triggerConfetti() {
    const duration = 3 * 1000; // 3 seconds
    const animationEnd = Date.now() + duration;
    const colors = ["#4ecca3", "#f5d042", "#e94560", "#f5f5f5"];

    (function frame() {
        confetti({
            particleCount: 5,
            angle: 60,
            spread: 55,
            origin: { x: 0 },
            colors: colors,
        });
        confetti({
            particleCount: 5,
            angle: 120,
            spread: 55,
            origin: { x: 1 },
            colors: colors,
        });

        if (Date.now() < animationEnd) {
            requestAnimationFrame(frame);
        }
    })();
}

document.getElementById("hintItem").addEventListener("click", async () => {
    const hintBox = document.getElementById("hintBox");

    try {
        if (!lastGuess) {
            hintBox.textContent = "Enter a guess first to get a hint!";
            return;
        }

        const hintText = await hint(lastGuess);
        hintBox.textContent = hintText.hint;
    } catch (error) {
        hintBox.textContent = "Unable to fetch a hint. Try again later.";
    }
});


document.getElementById("giveUpItem").addEventListener("click", async () => {
    try {
        const correctGame = await fetchSecretGame()
        disableSubmitButton();
        addCorrectGameToTable(correctGame);
    } catch (error) {

    }
});


function addCorrectGameToTable(game) {
    const tableBody = document.getElementById("guessTableBody");
    const row = document.createElement("tr");

    const safeJoin = (array) => Array.isArray(array) && array.length > 0 ? array.join(", ") : "N/A";

    // Name Cell
    const nameCell = document.createElement("td");
    nameCell.innerHTML = `<span class="correct">${game.name || "N/A"}</span>`;
    row.appendChild(nameCell);

    // Genres Cell
    const genresCell = document.createElement("td");
    genresCell.innerHTML = `<span class="correct">${safeJoin(game.genres)}</span>`;
    row.appendChild(genresCell);

    // Categories Cell
    const categoriesCell = document.createElement("td");
    categoriesCell.innerHTML = `<span class="correct">${safeJoin(game.categories)}</span>`;
    row.appendChild(categoriesCell);

    // Tags Cell
    const tagsCell = document.createElement("td");
    tagsCell.innerHTML = `<span class="correct">${safeJoin(game.tags)}</span>`;
    row.appendChild(tagsCell);

    // Developers Cell
    const developersCell = document.createElement("td");
    developersCell.innerHTML = `<span class="correct">${safeJoin(game.developers)}</span>`;
    row.appendChild(developersCell);

    // Publishers Cell
    const publishersCell = document.createElement("td");
    publishersCell.innerHTML = `<span class="correct">${safeJoin(game.publishers)}</span>`;
    row.appendChild(publishersCell);

    // Release Date Cell
    const releaseDateCell = document.createElement("td");
    releaseDateCell.innerHTML = `<span class="correct">${game.release_date || "N/A"}</span>`;
    row.appendChild(releaseDateCell);

    // Similarity Cell
    const similarityCell = createSimilarityCell(1); // Pass 1 for 100% similarity
    row.appendChild(similarityCell);

    tableBody.prepend(row);
}

// Function to disable the submit button
function disableSubmitButton() {
    guessButton.disabled = true;
    guessButton.style.backgroundColor = "#555";
    guessButton.style.cursor = "not-allowed";
}

// Function to find the first matching game and make the API call
async function submitFirstMatchingGame() {
    const userInput = guessInput.value.trim().toLowerCase();

    dropdown.style.display = "none";

    const firstMatch = data
        .filter(name => name.trim().toLowerCase().includes(userInput))
        .slice(0, 1);

    if (firstMatch) {
        // Use the first match and make the API call
        lastGuess = firstMatch;
        await makeGuess(firstMatch);
        guessInput.value = "";
    } else {
        alert("No matching game found! Please try a different guess.");
    }
}