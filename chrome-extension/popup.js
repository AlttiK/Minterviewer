const API_BASE_URL = 'http://localhost:8000';

let sessionId = null;
let messages = [];

const settingsDiv = document.getElementById('settings');
const startBtn = document.getElementById('startBtn');
const chatContainer = document.getElementById('chatContainer');
const inputContainer = document.getElementById('inputContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const endBtn = document.getElementById('endBtn');

startBtn.addEventListener('click', startInterview);
sendBtn.addEventListener('click', sendMessage);
endBtn.addEventListener('click', endInterview);
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function startInterview() {
  const interviewType = document.getElementById('interviewType').value;
  const questionType = document.getElementById('questionType').value;

  startBtn.disabled = true;
  startBtn.textContent = 'Starting...';

  try {
    // Generate session ID
    sessionId = Date.now().toString();

    // Initial system message to set context
    const systemMessage = {
      role: 'system',
      content: `You are a technical interviewer for a SWE Intern position. Conduct a LeetCode-style DSA interview. Follow these rules:
1. Ask ONE question at a time
2. Wait for the candidate's approach before giving hints
3. Ask clarifying questions to understand their thought process
4. If they're stuck, provide small hints (not full solutions)
5. Track their problem-solving approach for end-of-session feedback
6. Be encouraging but professional
7. Start by introducing yourself and asking the first question`
    };

    messages = [systemMessage];

    chrome.runtime.sendMessage({ type: "random_problem" });

    // Get first question from AI
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages,
        session_id: sessionId
      })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    
    // Add assistant message
    messages.push({
      role: 'assistant',
      content: data.message
    });

    // Display the question
    displayMessage('assistant', data.message, data.audio_url);

    // Show chat interface
    settingsDiv.classList.add('hidden');
    inputContainer.classList.remove('hidden');

  } catch (error) {
    console.error('Error starting interview:', error);
    displayMessage('system', `Error: Could not connect to backend. Make sure FastAPI server is running on ${API_BASE_URL}`);
    startBtn.disabled = false;
    startBtn.textContent = 'Start Interview';
  }
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Disable input
  sendBtn.disabled = true;
  userInput.disabled = true;

  // Display user message
  displayMessage('user', message);

  // Add to messages
  messages.push({
    role: 'user',
    content: message
  });

  // Clear input
  userInput.value = '';

  // Show loading
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'loading';
  loadingDiv.id = 'loading';
  loadingDiv.textContent = 'AI is thinking...';
  chatContainer.appendChild(loadingDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages,
        session_id: sessionId
      })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    // Remove loading
    const loading = document.getElementById('loading');
    if (loading) loading.remove();

    // Add assistant message
    messages.push({
      role: 'assistant',
      content: data.message
    });

    // Display the response
    displayMessage('assistant', data.message, data.audio_url);

  } catch (error) {
    console.error('Error sending message:', error);
    
    const loading = document.getElementById('loading');
    if (loading) loading.remove();
    
    displayMessage('system', 'Error: Could not get response from AI. Please try again.');
  } finally {
    // Re-enable input
    sendBtn.disabled = false;
    userInput.disabled = false;
    userInput.focus();
  }
}

async function endInterview() {
  endBtn.disabled = true;
  endBtn.textContent = 'Generating feedback...';

  try {
    // Request feedback
    const response = await fetch(`${API_BASE_URL}/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages,
        session_id: sessionId
      })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    // Display feedback
    displayFeedback(data.feedback);

    // Hide input
    inputContainer.classList.add('hidden');

  } catch (error) {
    console.error('Error getting feedback:', error);
    displayMessage('system', 'Error: Could not generate feedback.');
    endBtn.disabled = false;
    endBtn.textContent = 'End Interview';
  }
}

function displayMessage(role, content, audioUrl = null) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;

  const textDiv = document.createElement('div');
  textDiv.textContent = content;
  messageDiv.appendChild(textDiv);

  // Add audio player if audio URL is provided
  if (audioUrl) {
    const audioDiv = document.createElement('div');
    audioDiv.className = 'audio-player';
    
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.autoplay = true;
    audio.src = `${API_BASE_URL}${audioUrl}`;
    
    audioDiv.appendChild(audio);
    messageDiv.appendChild(audioDiv);
  }

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function displayFeedback(feedback) {
  const feedbackDiv = document.createElement('div');
  feedbackDiv.className = 'feedback';
  
  feedbackDiv.innerHTML = `
    <h3>📊 Interview Feedback</h3>
    <p><strong>Strengths:</strong> ${feedback.strengths || 'N/A'}</p>
    <p><strong>Weaknesses:</strong> ${feedback.weaknesses || 'N/A'}</p>
    <p><strong>Actionable Improvement:</strong> ${feedback.improvement || 'N/A'}</p>
  `;
  
  chatContainer.appendChild(feedbackDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Show reset button
  const resetBtn = document.createElement('button');
  resetBtn.textContent = 'Start New Interview';
  resetBtn.style.margin = '16px';
  resetBtn.style.width = 'calc(100% - 32px)';
  resetBtn.style.padding = '10px';
  resetBtn.style.background = '#4285f4';
  resetBtn.style.color = 'white';
  resetBtn.style.border = 'none';
  resetBtn.style.borderRadius = '4px';
  resetBtn.style.fontSize = '14px';
  resetBtn.style.fontWeight = '500';
  resetBtn.style.cursor = 'pointer';
  resetBtn.addEventListener('click', () => {
    location.reload();
  });
  
  chatContainer.appendChild(resetBtn);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
