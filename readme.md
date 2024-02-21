# Project Overview
This AI Assistant Bot, developed for Telegram, is designed to provide support and motivation for individuals aiming to quit smoking. It leverages the Telegram Bot API to interact with users in real-time, offering personalized advice, daily tasks, and a platform for users to track their progress and deal with cravings. The bot integrates with Firebase Firestore for data storage and management, ensuring a seamless and responsive user experience.

## Key Features
* User Engagement: Sends welcome messages, handles user queries, and provides motivational support.
* UID Linking: Allows users to link their Telegram chat ID with their unique user ID (UID) in the Firestore database for personalized interactions.
* Daily Tasks: Generates and sends users three random daily tasks aimed at supporting their quit-smoking journey, storing the tasks in the user's document for tracking.
* Real-Time Interaction: Utilizes a continuous check on Firestore documents for task generation and user interaction, ensuring timely responses.
## Technologies Used
* Telegram Bot API: For creating and managing the bot, handling messages, and interacting with users on Telegram.
* Firebase Firestore: A NoSQL cloud database used for storing and managing user data, tasks, and interactions in real-time.
* Firebase Admin SDK: Provides the backend logic with authenticated access to Firestore data.
* Python: The core programming language used for scripting the bot's functionality.
## Setup Instructions
1. Environment Setup: Ensure Python is installed on your system and set up a virtual environment for the project.
2. Install Dependencies:
   * Install the required Python packages by running pip install pyTelegramBotAPI firebase-admin.
3. Firebase Configuration:
   * Create a Firebase project and enable Firestore.
   * Generate a new private key for your Firebase Admin SDK and download the secret.json file.
   * Set the TG_BOT_API_TOKEN environment variable with your Telegram Bot API token.
   * Place the secret.json file in your project directory.
4. Running the Bot:
   * Run the bot script using python bot.py. Ensure the environment variables are correctly set before running.
5. Telegram Bot Setup:
   * Create a new bot on Telegram using the BotFather and retrieve your unique API token.
   * Set the TG_BOT_API_TOKEN environment variable to this token.
## Further Development
* Enhance the bot's AI capabilities for more personalized and effective quit-smoking strategies.
* Implement more interactive features like progress tracking, achievements, and user milestones.
* Integrate additional health and wellness resources to support users in their quit-smoking journey.