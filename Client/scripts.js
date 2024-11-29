// script.js

let secretGame = null;

// Use inline data and select a random secret game
secretGame = data[Math.floor(Math.random() * data.length)];
console.log("Secret Game:", secretGame);

// Get the modal elements
const congratsModal = document.getElementById("congratsModal");
const closeModal = document.getElementById("closeModal");

// Get the input field and create a dropdown container
const guessInput = document.getElementById("guessInput");
const dropdown = document.createElement("div");
dropdown.id = "autocompleteDropdown";
dropdown.classList.add("dropdown");
document.body.appendChild(dropdown);

// Add an event listener for the "keydown" event on the input field
guessInput.addEventListener("keydown", (event) => {
    // Check if the Enter key (key code 13) is pressed
    if (event.key === "Enter") {
        // Trigger the guess submission
        const userGuess = guessInput.value.trim();
        if (userGuess) {
            compareWithSecretGame(userGuess);
            guessInput.value = ""; // Clear the input field
        }
    }
});

// Listen for input changes
guessInput.addEventListener("input", () => {
    const userInput = guessInput.value.trim().toLowerCase();

    // Show suggestions only if the input is at least 3 characters
    if (userInput.length >= 3) {
        showSuggestions(userInput);
    } else {
        dropdown.style.display = "none"; // Hide the dropdown if input is too short
    }
});

// Function to handle user guess
document.getElementById("guessButton").addEventListener("click", () => {
    const userGuess = document.getElementById("guessInput").value.trim();
    if (userGuess) {
        compareWithSecretGame(userGuess);
        document.getElementById("guessInput").value = "";
    }
});

// Function to compare the guessed game with the secret game
function compareWithSecretGame(guess) {
    const guessedGame = data.find(game => game.Name.toLowerCase() === guess.toLowerCase());

    // If the guessed game is found, perform the comparison
    if (guessedGame) {
        const isCorrectGuess = guessedGame.Name.toLowerCase() === secretGame.Name.toLowerCase();

        if (isCorrectGuess) {
            showCongratsModal();
        }

        const tableBody = document.getElementById("guessTableBody");
        const row = document.createElement("tr");

        // Compare and create cells for each attribute
        const nameCell = createComparisonCell(guessedGame.Name, secretGame.Name);
        const genreCell = createComparisonCell(guessedGame.Genres, secretGame.Genres, true);
        const categoryCell = createComparisonCell(guessedGame.Categories, secretGame.Categories, true);
        const developerCell = createComparisonCell(guessedGame.Developers, secretGame.Developers, true);
        const publisherCell = createComparisonCell(guessedGame.Publishers, secretGame.Publishers, true);
        const releaseDateCell = createReleaseDateCell(guessedGame["Release date"], secretGame["Release date"]);

        row.append(nameCell, genreCell, categoryCell, developerCell, publisherCell, releaseDateCell);
        tableBody.appendChild(row);
    } else {
        alert("Game not found! Please try a different guess.");
    }
}

// Helper function to create comparison cells with color-coding
function createComparisonCell(guessedValue, secretValue, isList = false) {
    const cell = document.createElement("td");

    // If the value is a list (e.g., Genres), split and compare each item
    if (isList) {
        const guessedItems = guessedValue.split(',').map(item => item.trim().toLowerCase());
        const secretItems = secretValue.split(',').map(item => item.trim().toLowerCase());

        // Create a formatted string with color-coded matches
        const matchedItems = guessedItems.map(item => {
            if (secretItems.includes(item)) {
                return `<span class="correct">${item}</span>`;
            } else {
                return `<span class="incorrect">${item}</span>`;
            }
        }).join(', ');

        cell.innerHTML = matchedItems;
    } else {
        // Simple comparison for non-list values
        if (guessedValue.toLowerCase() === secretValue.toLowerCase()) {
            cell.innerHTML = `<span class="correct">${guessedValue}</span>`;
        } else {
            cell.innerHTML = `<span class="incorrect">${guessedValue}</span>`;
        }
    }

    return cell;
}

// Helper function to create the release date cell with an arrow icon
function createReleaseDateCell(guessedDate, secretDate) {
    const cell = document.createElement("td");

    const dateText = document.createElement("span");
    dateText.classList.add("release-date-text");
    dateText.textContent = guessedDate || "N/A";

    const arrowIcon = document.createElement("img");
    arrowIcon.src = "arrow-up.svg";
    arrowIcon.style.width = "16px";
    arrowIcon.style.height = "16px";

    // Parse the dates for comparison
    const guessedDateObj = new Date(guessedDate);
    const secretDateObj = new Date(secretDate);

    // Check if the guessed date is correct
    const isCorrectDate = guessedDateObj.getTime() === secretDateObj.getTime();

    // If the release date is correct, set the text color to green and hide the arrow icon
    if (isCorrectDate) {
        dateText.className = "correct";
        arrowIcon.style.display = "none";
    } else {
        // Set the text color to red for incorrect date
        dateText.className = "incorrect";

        // Flip the arrow if the secret game was released before the guessed game
        if (secretDateObj < guessedDateObj) {
            arrowIcon.style.transform = "rotate(180deg)";
        }
    }

    cell.append(dateText, arrowIcon);
    return cell;
}

// Function to show autocomplete suggestions
function showSuggestions(input) {
    // Filter the first 10 games that match the input
    const matches = data
        .filter(game => game.Name.toLowerCase().includes(input))
        .slice(0, 10);

    // Clear previous suggestions
    dropdown.innerHTML = "";

    // If there are no matches, hide the dropdown
    if (matches.length === 0) {
        dropdown.style.display = "none";
        return;
    }

    // Show the dropdown and position it below the input field
    const inputRect = guessInput.getBoundingClientRect();
    dropdown.style.left = `${inputRect.left}px`;
    dropdown.style.top = `${inputRect.bottom}px`;
    dropdown.style.width = `${inputRect.width}px`;
    dropdown.style.display = "block";

    // Create a suggestion item for each match
    matches.forEach(match => {
        const suggestionItem = document.createElement("div");
        suggestionItem.classList.add("suggestion-item");
        suggestionItem.textContent = match.Name;

        // When a suggestion is clicked, fill the input field and hide the dropdown
        suggestionItem.addEventListener("click", () => {
            guessInput.value = match.Name;
            dropdown.style.display = "none";
        });

        dropdown.appendChild(suggestionItem);
    });
}

// Function to show the modal and trigger the confetti animation
function showCongratsModal() {
    congratsModal.style.display = "flex";
    triggerConfetti();
}

// Close the modal when the user clicks on the close button
closeModal.addEventListener("click", () => {
    congratsModal.style.display = "none";
});

// Close the modal when the user clicks outside of it
window.addEventListener("click", (event) => {
    if (event.target === congratsModal) {
        congratsModal.style.display = "none";
    }
});

// Function to show the modal and trigger the confetti animation
function showCongratsModal() {
    congratsModal.style.display = "flex";
    triggerConfetti();
}

// Function to trigger the confetti animation
function triggerConfetti() {
    const duration = 3 * 1000; // Confetti duration in milliseconds
    const animationEnd = Date.now() + duration;
    const colors = ["#4ecca3", "#f5d042", "#e94560", "#f5f5f5"];

    (function frame() {
        confetti({
            particleCount: 5,
            angle: 60,
            spread: 55,
            origin: { x: 0 },
            colors: colors
        });
        confetti({
            particleCount: 5,
            angle: 120,
            spread: 55,
            origin: { x: 1 },
            colors: colors
        });

        if (Date.now() < animationEnd) {
            requestAnimationFrame(frame);
        }
    })();
}