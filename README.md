# 🤖 Discord Parafrase Bot (Powered by Gemini AI)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-5865F2)
![AI Model](https://img.shields.io/badge/AI-Google_Gemini-orange)

A smart Discord bot designed to **paraphrase and humanize text** using Google's advanced Generative AI (Gemini). This bot is optimized to rewrite text in various styles while aiming to bypass AI detection systems (Humanizer).

Developed by **[Aldi Nur Syarrifuddin]**.

---

## ✨ Key Features

* **🧠 Smart Humanizer:** Uses advanced prompting to vary sentence structure and emotion, making the output less likely to be detected as AI.
* **🎭 Multiple Styles:**
    * `Formal`: Academic/Professional tone.
    * `Santai`: Casual/Daily conversation tone.
    * `Jaksel`: Code-mixing (Indonesian-English) style.
    * `Lucu`: Humorous and witty tone.
    * `English`: Natural English translation/paraphrasing.
* **🚀 Auto-Model Detection:** Automatically scans and selects the best available Gemini model (e.g., `gemini-2.5-flash`, `gemini-pro`) to prevent "Model Not Found" errors.
* **⚡ Direct API Integration:** Uses `aiohttp` for lightweight and fast direct API calls to Google, bypassing heavy SDK dependencies.
* **📄 Long Text Support:** Automatically sends results as a `.txt` file if the output exceeds Discord's character limit.
* **🛠️ Slash Commands:** Fully supports modern Discord `/` commands with dropdown menus.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Framework:** Discord.py
* **AI Provider:** Google Gemini API (Generative Language)
* **Libraries:** `aiohttp`, `python-dotenv`

---

## ⚙️ Installation & Setup

Follow these steps to run the bot on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/anursyarrifuddin-mage/discord-parafrase-bot.git](https://github.com/anursyarrifuddin-mage/discord-parafrase-bot.git)
cd discord-parafrase-bot
```
### 2. Install Depedencies
Make sure you have Python installed. Then run:
```bash
pip install -r requirements.txt
```
### 3. Configure Environment Variables
Create a new file named .env in the root directory. Add your credentials (do not share this file):
```env
DISCORD_TOKEN=your_discord_bot_token_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```

Note:
- Get Discord Token from [Discord Developer Portal](https://discord.com/developers/applications).
- Get Gemini API Key from [Google AI Studio](https://aistudio.google.com/api-keys).

### 4. Run the bot
```bash
python bot_parafrase.py
```
(Note: If you renamed the main file, use that filename instead).

## 📖 Usage
Slash Commands
Type / in any channel where the bot is invited to see the menu.
| Command | Description |
| :--- | ---: |
| /parafrase | Opens the menu to select style and input text. |
| /help | Shows the help menu and documentation. |

## Styles Explained
- Formal: Best for assignments, thesis (Skripsi), or formal reports.
- Santai: Best for chatting with friends.
- Jaksel: "Which is literally" style.
- Lucu: Adds jokes and humor to the text.
- Inggris: Paraphrases or translates text into natural English.