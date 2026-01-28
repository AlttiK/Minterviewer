const API_BASE_URL = 'http://localhost:8000';

let sessionId = null;
let messages = [];
let interviewActive = false;

const chatContainer = document.getElementById('chatContainer');
const inputContainer = document.getElementById('inputContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const endBtn = document.getElementById('endBtn');

loadInterviewState();

sendBtn.addEventListener('click', sendMessage);
endBtn.addEventListener('click', endInterview);
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Function to save interview state
async function saveInterviewState() {
  const state = {
    sessionId,
    messages,
    interviewActive,
    timestamp: Date.now()
  };
  await chrome.storage.local.set({ interviewState: state });
}

// Function to load interview state
async function loadInterviewState() {
  try {
    const result = await chrome.storage.local.get('interviewState');
    if (result.interviewState && result.interviewState.interviewActive) {
      const state = result.interviewState;
      sessionId = state.sessionId;
      messages = state.messages || [];
      interviewActive = state.interviewActive;
      
      // Restore UI state
      settingsDiv.classList.add('hidden');
      inputContainer.classList.remove('hidden');
      
      // Redisplay all messages
      chatContainer.innerHTML = '';
      messages.forEach(msg => {
        if (msg.role !== 'system') {
          displayMessage(msg.role, msg.content);
        }
      });
      
      // Focus on input
      userInput.focus();
    }
  } catch (error) {
    console.error('Error loading interview state:', error);
  }
}



