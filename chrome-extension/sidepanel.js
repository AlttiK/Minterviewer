const API_BASE_URL = 'http://localhost:8000';

let sessionId = null;
let messages = [];
let interviewActive = false;
let leetcodeProblemDescription = "";

const settingsDiv = document.getElementById('settings');
const startBtn = document.getElementById('startBtn');
const chatContainer = document.getElementById('chatContainer');
const inputContainer = document.getElementById('inputContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const endBtn = document.getElementById('endBtn');

loadInterviewState();

startBtn.addEventListener('click', startInterview);
sendBtn.addEventListener('click', sendMessage);
endBtn.addEventListener('click', endInterview);
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function saveInterviewState() {
  const state = {
    sessionId,
    messages,
    interviewActive,
    leetcodeProblemDescription,
    timestamp: Date.now()
  };
  await chrome.storage.local.set({ interviewState: state });
}

async function loadInterviewState() {
    try {
        const result = await chrome.storage.local.get('interviewState');
        if (result.interviewState && result.interviewState.interviewActive) {
        const state = result.interviewState;
        sessionId = state.sessionId;
        messages = state.messages || [];
        leetcodeProblemDescription = state.leetcodeProblemDescription || "";
        interviewActive = state.interviewActive;
        
        // Hide settings, show interview UI
        settingsDiv.classList.add('hidden');
        inputContainer.classList.remove('hidden');
        
        chatContainer.innerHTML = '';
        messages.forEach(msg => {
            if (msg.role !== 'system' && msg.content !== `Let's begin the interview. Start by introducing yourself and explaining the problem statement.`) {
                displayMessage(msg.role, msg.content);
            }
        });
        
        userInput.focus();
        }
    } 
    catch (error) {
        console.error('Error loading interview state:', error);
    }
}

async function clearInterviewState() {
    await chrome.storage.local.remove('interviewState');
}

async function startInterview() {
  startBtn.disabled = true;
  startBtn.innerHTML = '<span class="btn-icon">⏳</span> Opening LeetCode...';

  try {
    sessionId = Date.now().toString();
    
    // Step 1: Open LeetCode
    chrome.runtime.sendMessage({ type: "random_problem" });
    
    // Step 2: Listen for problem description from background script
    chrome.storage.onChanged.addListener(async function descriptionListener(changes, namespace) {
      if (changes.problemDescription && namespace === 'local') {
        chrome.storage.onChanged.removeListener(descriptionListener);
        
        leetcodeProblemDescription = changes.problemDescription.newValue || "";
        
        startBtn.innerHTML = '<span class="btn-icon">⏳</span> Getting AI greeting...';
        
        // Step 3: Create system message with problem description
        const systemMessage = {
          role: 'system',
          content: `Your name is Amy and you are a technical interviewer for a SWE Intern position. Conduct a LeetCode-style DSA interview. Follow these rules:
                    1. Ask ONE question at a time
                    2. Keep responses concise (under 100 words) unless your introducing yourself
                    3. Wait for the candidate's approach before giving hints
                    4. Ask clarifying questions to understand their thought process
                    5. If they're stuck, provide small hints (not full solutions)
                    6. Track their problem-solving approach for end-of-session feedback
                    7. Be encouraging but professional and pick a random personality
                    8. Start by introducing yourself and explaining the problem statement:
                    ${leetcodeProblemDescription}`
        };

        const initialMessage = {
          role: 'user',
            content: `Let's begin the interview. Start by introducing yourself and explaining the problem statement.`
        };

        // Step 3.5: Initialize messages in list
        messages = [systemMessage, initialMessage];

        // Step 4: Get first question from backend
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
        
        messages.push({
          role: 'assistant',
          content: data.message
        });

        // Step 4.5: Clear welcome and display first message
        chatContainer.innerHTML = '';
        displayMessage('assistant', data.message, data.audio_url);

        // Step 5: Show interview UI and save state
        settingsDiv.classList.add('hidden');
        inputContainer.classList.remove('hidden');
        interviewActive = true;
        await saveInterviewState();
        
        userInput.focus();
      }
    });

  } catch (error) {
    console.error('Error starting interview:', error);
    displayMessage('system', `Error: Could not connect to backend. Make sure FastAPI server is running on ${API_BASE_URL}`);
    startBtn.disabled = false;
    startBtn.innerHTML = '<span class="btn-icon"></span> Return to Home Page';
  }
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Step 1: Disable input and display user message
  sendBtn.disabled = true;
  userInput.disabled = true;

  displayMessage('user', message);

  messages.push({
    role: 'user',
    content: message
  });

  userInput.value = '';

  // Step 1.5: show loading indicator
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'loading';
  loadingDiv.id = 'loading';
  loadingDiv.textContent = 'AI is thinking...';
  chatContainer.appendChild(loadingDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Step 2: Send message to backend
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

    const loading = document.getElementById('loading');
    if (loading) loading.remove();

    // Step 3: Add and display assistant response from backend
    messages.push({
      role: 'assistant',
      content: data.message
    });

    displayMessage('assistant', data.message, data.audio_url);
    
    // Step 3.5: Save updated state
    await saveInterviewState();

  } catch (error) {
    console.error('Error sending message:', error);
    
    const loading = document.getElementById('loading');
    if (loading) loading.remove();
    
    displayMessage('system', 'Error: Could not get response from AI. Please try again.');
  } finally {
    // Step 4: Re-enable send message input
    sendBtn.disabled = false;
    userInput.disabled = false;
    userInput.focus();
  }
}


async function endInterview() {
  endBtn.disabled = true;
  endBtn.textContent = 'Generating feedback...';

  try {
    // Step 1: Request feedback
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

    // Step 2: Display feedback
    displayFeedback(data.feedback);

    // Step 3: Hide input
    inputContainer.classList.add('hidden');

  } catch (error) {
    console.error('Error getting feedback:', error);
    displayMessage('system', 'Error: Could not generate feedback.');
    endBtn.disabled = false;
    endBtn.textContent = 'End Interview';
  }
}


function displayMessage(role, content, audioUrl = null) {
  // Create new message and text div
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;

  const textDiv = document.createElement('div');
  textDiv.textContent = content;
  messageDiv.appendChild(textDiv);

  // create audio div and element
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

  // Append message to chat container and scroll to bottom
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function displayFeedback(feedback) {
  // create feedback div
  const feedbackDiv = document.createElement('div');
  feedbackDiv.className = 'feedback';
  
  feedbackDiv.innerHTML = `
    <h3>Interview Feedback</h3>
    <p><strong>Strengths:</strong> ${feedback.strengths || 'N/A'}</p>
    <p><strong>Weaknesses:</strong> ${feedback.weaknesses || 'N/A'}</p>
    <p><strong>Actionable Improvement:</strong> ${feedback.improvement || 'N/A'}</p>
  `;
  
  // Append feedback to chat container and scroll to bottom
  chatContainer.appendChild(feedbackDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Clear interview state
  interviewActive = false;
  clearInterviewState();
  
  // Show reset button
  const resetBtn = document.createElement('button');
  resetBtn.className = 'btn btn-reset';
  resetBtn.textContent = 'Return to Home Page';
  resetBtn.addEventListener('click', async () => {
    await clearInterviewState();
    location.reload();
  });
  
  chatContainer.appendChild(resetBtn);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
