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
        return games; // Return the games list
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

        /*
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
         */

        const result = await response.json();

        processFeedback(result);
      
        return result; // Return the guess result
    } catch (error) {
        console.error("Error making a guess:", error);
    }
}


async function hint(gameName) {
    try {
        const response = await fetch(`${BASE_API_URL}/hint?name=${gameName}`, {
            method: "GET",
        });

        /*
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
         */

        const result = await response.json();
        return result; // Return the guess result
    } catch (error) {
        console.error("Error making a guess:", error);
    }
}

async function fetchSecretGame() {
    try {
        const response = await fetch(`${BASE_API_URL}/target`, {
            method: "GET",
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const secretGame = await response.json();
        console.log("Fetched Secret Game:", secretGame);
        return secretGame; // Return the target game object
    } catch (error) {
        console.error("Error fetching target game:", error);
    }
}