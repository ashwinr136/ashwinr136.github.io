document.addEventListener('DOMContentLoaded', function () {
    const taskInput = document.getElementById('task-input');
    const addTaskButton = document.getElementById('add-task-button');
    const taskList = document.getElementById('task-list');
    const completedTasksCount = document.getElementById('completed-count');
    const totalTasksCount = document.getElementById('total-count');
    const completionPercentage = document.getElementById('completion-percentage');
	var gauge = new JustGage({
    id: "g1", 
    value: 0,  
    min: 0,   
    max: 100,  
    title: "Completion Percentage", 
	label: "%",
	levelColors: ["#FF0000", "#FFFF00", "#00FF00"],
	titleFontColor: "#000000",
	labelFontColor: "#000000",
	
});

    let totalTasks = 0;
    let completedTasks = 0;
	
	function updateGauge() {
		const percentage = (completedTasks / totalTasks) * 100 || 0;
		gauge.refresh(percentage);
	}

    function updateCompletionStatistics() {
        completedTasksCount.textContent = completedTasks;
        totalTasksCount.textContent = totalTasks;
        const percentage = (completedTasks / totalTasks) * 100 || 0;
        completionPercentage.textContent = percentage.toFixed(2) + '%';
    }

    addTaskButton.addEventListener('click', function () {
        const taskText = taskInput.value.trim();
        if (taskText) {
            addTask(taskText);
            taskInput.value = '';
        }
    });

    taskInput.addEventListener('keyup', function (event) {
        if (event.key === 'Enter') {
            addTaskButton.click();
        }
    });

    function addTask(taskText) {
        totalTasks++;
        updateCompletionStatistics();

        const taskItem = document.createElement('li');
        const taskCheckbox = document.createElement('input');
        taskCheckbox.type = 'checkbox';

        const taskLabel = document.createElement('label');
        taskLabel.textContent = taskText;

        const removeButton = document.createElement('button');
        removeButton.textContent = '';
		removeButton.classList.add('remove-button');

        taskItem.appendChild(taskCheckbox);
        taskItem.appendChild(taskLabel);
        taskItem.appendChild(removeButton);
        taskList.appendChild(taskItem);

        taskCheckbox.addEventListener('change', function () {
            if (taskCheckbox.checked) {
                taskLabel.style.textDecoration = 'line-through';
                completedTasks++;
            } else {
                taskLabel.style.textDecoration = 'none';
                completedTasks--;
            }
            updateCompletionStatistics();
			updateGauge();
        });

        removeButton.addEventListener('click', function () {
            taskList.removeChild(taskItem);
            totalTasks--;
            if (taskCheckbox.checked) {
                completedTasks--;
            }
            updateCompletionStatistics();
			updateGauge();
        });
    }
});