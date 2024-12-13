// Select a random secret game
let data = []; // To hold the fetched games

// Fetch the games using the fetchGames function from fetching.js
async function initializeGame() {
    try {
        // Fetch all games
        const allGamesResponse = await fetchGames(); // Using fetchGames from fetching.js
        data = allGamesResponse; // Populate the data array
        console.log("Fetched games:", data);

    } catch (error) {
        console.error("Error initializing the game:", error);
    }
}

// Initialize the game
initializeGame();

// Modal elements
const congratsModal = document.getElementById("congratsModal");
const closeModal = document.getElementById("closeModal");

// Input field and dropdown container
const guessInput = document.getElementById("guessInput");
const dropdown = document.createElement("div");
dropdown.id = "autocompleteDropdown";
dropdown.classList.add("dropdown");
document.body.appendChild(dropdown);

// Event listener for "Enter" key on the input field
guessInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        const userGuess = guessInput.value.trim();
        if (userGuess) {
            compareWithSecretGame(userGuess);
            guessInput.value = ""; // Clear the input field
        }
    }
});

// Autocomplete suggestions on input change
guessInput.addEventListener("input", () => {
    const userInput = guessInput.value.trim().toLowerCase();
    if (userInput.length >= 3) {
        showSuggestions(userInput);
    } else {
        dropdown.style.display = "none"; // Hide the dropdown if input is too short
    }
});

// Submit guess button functionality
document.getElementById("guessButton").addEventListener("click", () => {
    const userGuess = guessInput.value.trim();
    if (userGuess) {
        compareWithSecretGame(userGuess);
        guessInput.value = "";
    }
});

// Dropdown elements
const menuIcon = document.getElementById("menuIcon");
const dropdownMenu = document.getElementById("dropdownMenu");

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

// Dropdown button actions
document.getElementById("hintButton").addEventListener("click", () => {
    alert("Here's a hint!");
});

document.getElementById("giveUpButton").addEventListener("click", () => {
    alert("You gave up! The correct answer is: " + secretGame.Name);
});

// Add guessed game details to the table
function addGuessToTable(guessedGame) {
    const tableBody = document.getElementById("guessTableBody");
    const row = document.createElement("tr");

    // Create and append cells
    row.appendChild(createComparisonCell(guessedGame.Name, secretGame.Name));
    row.appendChild(createComparisonCell(guessedGame.Genres, secretGame.Genres, true));
    row.appendChild(createComparisonCell(guessedGame.Categories, secretGame.Categories, true));
    row.appendChild(createComparisonCell(guessedGame.Developers, secretGame.Developers));
    row.appendChild(createComparisonCell(guessedGame.Publishers, secretGame.Publishers));
    row.appendChild(createReleaseDateCell(guessedGame["Release date"], secretGame["Release date"]));

    tableBody.appendChild(row);
}

// Create a comparison cell with color-coded matches
function createComparisonCell(guessedValue, secretValue, isList = false) {
    const cell = document.createElement("td");

    if (isList) {
        const guessedItems = guessedValue.split(", ").map(item => item.toLowerCase());
        const secretItems = secretValue.split(", ").map(item => item.toLowerCase());
        cell.innerHTML = guessedItems
            .map(item => (secretItems.includes(item) ? `<span class="correct">${item}</span>` : `<span class="incorrect">${item}</span>`))
            .join(", ");
    } else {
        cell.innerHTML =
            guessedValue.toLowerCase() === secretValue.toLowerCase()
                ? `<span class="correct">${guessedValue}</span>`
                : `<span class="incorrect">${guessedValue}</span>`;
    }

    return cell;
}

// Create a release date cell with an arrow indicator
function createReleaseDateCell(guessedDate, secretDate) {
    const cell = document.createElement("td");
    const dateText = document.createElement("span");
    dateText.textContent = guessedDate || "N/A";

    const arrow = document.createElement("span");
    arrow.textContent = "↑";
    arrow.style.color = "red";
    arrow.style.marginLeft = "5px";

    const guessedDateObj = new Date(guessedDate);
    const secretDateObj = new Date(secretDate);

    if (guessedDateObj.getTime() === secretDateObj.getTime()) {
        dateText.classList.add("correct");
        arrow.style.display = "none";
    } else {
        dateText.classList.add("incorrect");
        arrow.textContent = guessedDateObj > secretDateObj ? "↓" : "↑";
    }

    cell.appendChild(dateText);
    cell.appendChild(arrow);
    return cell;
}

// Show autocomplete suggestions
function showSuggestions(input) {
    const matches = data
        .filter(game => game.Name.toLowerCase().includes(input))
        .slice(0, 10);

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

    matches.forEach(match => {
        const suggestionItem = document.createElement("div");
        suggestionItem.classList.add("suggestion-item");
        suggestionItem.textContent = match.Name;
        suggestionItem.addEventListener("click", () => {
            guessInput.value = match.Name;
            dropdown.style.display = "none";
        });
        dropdown.appendChild(suggestionItem);
    });
}

// Show modal and trigger confetti animation
function showCongratsModal() {
    congratsModal.style.display = "flex";
    triggerConfetti();
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
