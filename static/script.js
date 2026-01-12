const API_BASE = 'http://127.0.0.1:5000';
const TASK_ID = 1;

// 1. READ
async function loadComments() {
    const response = await fetch(`${API_BASE}/tasks/${TASK_ID}/comments`);
    const comments = await response.json();
    
    const list = document.getElementById('comments-list');
    list.innerHTML = ''; 

    comments.forEach(comment => {
        const item = document.createElement('div');
        item.className = 'comment-box';
        item.innerHTML = `
            <div class="comment-header">
                <span>${comment.author} says:</span>
                <div>
                    <button class="btn btn-blue" onclick="editComment(${comment.id}, '${comment.text}')">Edit</button>
                    <button class="btn btn-red" onclick="deleteComment(${comment.id})">Delete</button>
                </div>
            </div>
            <p>${comment.text}</p>
        `;
        list.appendChild(item);
    });
}

// 2. CREATE
async function addComment() {
    const textInput = document.getElementById('new-comment-text');
    const text = textInput.value;

    if (!text) return alert("Please write something!");

    await fetch(`${API_BASE}/tasks/${TASK_ID}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, author: 'User' })
    });

    textInput.value = ''; 
    loadComments(); 
}

// 3. DELETE
async function deleteComment(id) {
    if(!confirm("Are you sure?")) return;

    await fetch(`${API_BASE}/comments/${id}`, {
        method: 'DELETE'
    });

    loadComments(); 
}

// 4. UPDATE
async function editComment(id, oldText) {
    const newText = prompt("Update your comment:", oldText);
    
    if (newText && newText !== oldText) {
        await fetch(`${API_BASE}/comments/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: newText })
        });
        loadComments(); 
    }
}

// Initial Load
loadComments();