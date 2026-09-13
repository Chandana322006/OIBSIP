# OIBSIP Python Projects

A collection of Python projects completed as part of the OIBSIP (Oasis Infobyte Summer Internship Program).

## 📁 Project Structure

```
OIBSIP/
├── Python-Task1-VoiceAssistant/
│   └── Chandana_task1.py
├── Python-Task2-BMICalculator/
│   └── Chandana_task2.py
├── PPython-Task3-RandomPasswordGenerator/
│   └── Chandana_task3.py
├── Chandana_task5/
│   ├── client.py
│   └── server.py
└── README.md
```

## 📋 Projects Overview

### 1. Voice Assistant (Task 1)
**File:** `OIBSIP/Python-Task1-VoiceAssistant/Chandana_task1.py`

A speech-enabled voice assistant that responds to voice commands.

**Features:**
- Speech recognition using Google's speech API
- Text-to-speech responses
- Commands for:
  - Greeting ("hello")
  - Time queries
  - Date queries
  - Opening websites (Google, YouTube)
  - YouTube search functionality
  - And more...

**Requirements:**
- `speech_recognition`
- `pyttsx3`
- Microphone access

**Usage:**
```bash
python Chandana_task1.py
```

---

### 2. BMI Calculator (Task 2)
**File:** `OIBSIP/Python-Task2-BMICalculator/Chandana_task2.py`

A graphical BMI (Body Mass Index) calculator with data persistence and visualization.

**Features:**
- User-friendly GUI using Tkinter
- BMI calculation based on weight (kg) and height (cm)
- BMI category classification
- SQLite database for storing records
- Data visualization using Matplotlib
- View BMI history and trends

**Requirements:**
- `tkinter` (usually included with Python)
- `sqlite3` (usually included with Python)
- `matplotlib`

**Usage:**
```bash
python Chandana_task2.py
```

---

### 3. Random Password Generator (Task 3)
**File:** `OIBSIP/PPython-Task3-RandomPasswordGenerator/Chandana_task3.py`

A secure random password generator with customizable options.

**Features:**
- GUI-based password generation using Tkinter
- Customizable password length (minimum 8 characters)
- Options to include:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special symbols
- Password history tracking
- Copy to clipboard functionality
- Password strength validation

**Requirements:**
- `tkinter` (usually included with Python)
- `pyperclip`
- `secrets` (usually included with Python)
- `string` (usually included with Python)

**Usage:**
```bash
python Chandana_task3.py
```

---

### 4. Client-Server Application (Task 5)
**Files:** 
- `Chandana_task5/server.py`
- `Chandana_task5/client.py`

A basic client-server communication application.

**Usage:**

Start the server:
```bash
python server.py
```

In another terminal, run the client:
```bash
python client.py
```

---

## 🚀 Installation

### Prerequisites
- Python 3.6+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Chandana322006/OIBSIP.git
cd OIBSIP
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

3. Activate virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install required dependencies:
```bash
pip install pyttsx3 SpeechRecognition matplotlib pyperclip
```

---

## 📝 Notes

- The BMI Calculator creates a `bmi_records.db` SQLite database file in its directory
- Voice Assistant requires a working microphone for speech input
- Password Generator includes validation to ensure secure passwords (minimum 8 characters)
- All projects use Tkinter for GUI (Task 1 is CLI-based with speech input)

---

## 👤 Author

Chandana

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements!

---

## ❓ Support

For issues or questions, please open an issue on the GitHub repository.