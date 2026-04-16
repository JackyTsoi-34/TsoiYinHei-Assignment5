# AI Agent Dashboard

## System Overview

**Problem:** Create an interactive web-based interface for users to communicate with an AI agent, providing a real-time conversation experience with configuration options.

**Workflow:**
1. User configures agent settings (model, temperature) in the sidebar
2. User initializes the agent with the "Initialize Agent" button
3. User enters a query in the main text area
4. Agent processes the query using OpenAI's API
5. Response is displayed in the dashboard and added to conversation history
6. User can continue the conversation or clear history as needed

**Key Components:**
- **agent.py**: LLM-based agent module that handles API calls to OpenAI
- **app.py**: Streamlit dashboard application with UI components
- **requirements.txt**: Python package dependencies
- **.env**: Environment variables (API key storage)

## How to Run the App

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (from https://platform.openai.com/api-keys)

### Setup Steps

1. **Clone or download the project files** to your local machine

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**:
   - Copy `.env.example` to `.env`
   - Open `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-actual-key-here
     ```

5. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

6. **Access the dashboard**: The app will open in your default browser at `http://localhost:8501`

## Features Implemented

✅ **Dashboard Layout**
- Clean, organized page layout with sidebar and main area
- Page title and descriptive header
- Professional styling with custom CSS

✅ **Sidebar Configuration**
- Model selection (gpt-3.5-turbo, gpt-4)
- Temperature slider (0.0-2.0) with help text
- Agent initialization button
- Conversation history management (clear button)
- About section with instructions

✅ **User Input**
- Text area for multi-line queries
- Submit button with visual feedback
- Input validation (checks for empty inputs)
- Placeholder text for guidance

✅ **Agent Integration**
- LLM-based agent using OpenAI's chat API
- Configurable model and temperature
- Conversation history tracking
- Error handling for API issues
- Loading indicator during processing

✅ **User Experience**
- Success/error/warning messages with icons
- Conversation history display
- Chat-style message formatting
- Clear initialization status feedback
- Responsive button sizes and layouts

## Design Decisions

1. **Session State Management**: Used Streamlit's `st.session_state` to persist agent instance and conversation history across reruns, preventing unnecessary reinitializations.

2. **Agent Architecture**: Created a simple `AIAgent` class with methods for processing input and managing conversation history, making it reusable and testable.

3. **Error Handling**: Wrapped API calls in try-except blocks with user-friendly error messages to handle network issues, invalid keys, or API errors gracefully.

4. **Temperature Clamping**: Temperature values are clamped to valid ranges (0.0-2.0) to prevent API errors while allowing user flexibility.

5. **Conversation History**: Maintained in session state to allow users to see context of previous exchanges without making repeated API calls.

6. **Custom Styling**: Used HTML/CSS for enhanced visual layout with color-coded message boxes for better UX.

7. **API Key Security**: Used `python-dotenv` to load sensitive credentials from environment files, keeping them out of source code.

## Testing Recommendations

- Test with various prompt types (questions, creative requests, code generation)
- Try different temperature values to observe response variation
- Test conversation continuity across multiple exchanges
- Verify error handling by providing invalid API key
- Check UI responsiveness on different screen sizes

---
**Assignment**: Mini-Assignment 5 - Dashboard Development (IIMT3688)
