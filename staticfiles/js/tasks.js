document.addEventListener('DOMContentLoaded', function() {
    // タスク編集領域でのキー入力を検知
    document.querySelectorAll('.editable').forEach(function(element) {
        element.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // フォームの自動送信を防止
                const taskId = this.dataset.taskId; // タスクIDを取得
                const newValue = this.innerText; // 編集された新しい値を取得
                updateTask(taskId, newValue); // 更新関数を呼び出し
            }
        });
    });
});

function updateTask(taskId, newTitle) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`/tasks/task/${taskId}/update/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ title: newTitle })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if(data.status === 'success') {
            // DOMを更新して変更を反映
            document.querySelector(`[data-task-id="${taskId}"]`).textContent = newTitle;
        }
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });
}
