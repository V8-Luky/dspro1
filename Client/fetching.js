const BASE_API_URL = "https://game-guesser-517951749380.us-east4.run.app";

// Function to fetch all games
async function fetchGames() {
    try {
        const response = await fetch(`${BASE_API_URL}/games`, {
            method: "GET",
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const games = await response.json();
        return games;
    } catch (error) {
        console.error("Error fetching games:", error);
    }
}

// Function to make a guess
async function makeGuess(gameName) {
    try {
        const response = await fetch(`${BASE_API_URL}/guess?name=${gameName}`, {
            method: "POST",
        });

        const result = await response.json();

        processFeedback(result);
      
        return result;
    } catch (error) {
        console.error("Error making a guess:", error);
    }
}

// Function to get a hint
async function hint(gameName) {
    try {
        const response = await fetch(`${BASE_API_URL}/hint?name=${gameName}`, {
            method: "GET",
        });

        const result = await response.json();
        return result;
    } catch (error) {
        console.error("Error making a guess:", error);
    }
}

// Function to fetch the secret game after give up
async function fetchSecretGame() {
    try {
        const response = await fetch(`${BASE_API_URL}/target`, {
            method: "GET",
        });

        const secretGame = await response.json();
        return secretGame;
    } catch (error) {
        console.error("Error fetching target game:", error);
    }
}