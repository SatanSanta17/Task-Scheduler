from flask import Flask, Blueprint, json, render_template, send_from_directory, request, redirect, url_for, jsonify
from datetime import datetime
# Create a Blueprint instance
bp = Blueprint('main', __name__)



# Route to serve CSS file


@bp.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('../static/css', path)

# Route to serve JavaScript file


@bp.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('../static/js', path)

# Route to serve index.html


@bp.route('/')
def index():
    from .models.task import Task
    # Fetch tasks from the database
    
    tasks_cursor = Task.find_all()
    tasks = list(tasks_cursor)  # Convert Cursor to list
    
    if tasks:
        # Apply combined sorting: deadline > intensity > name
        tasks = sorted(tasks, key=lambda x: (
            datetime.strptime(x['deadline'], '%Y-%m-%d'), 
            -int(x['intensity']), 
            x['title'].lower()
        ))
    
    for task in tasks:
        # Convert ObjectId to string
        task['_id'] = str(task['_id'])

        # Update tasks' status if the deadline has passed
        if task['status'] == "pending" and datetime.strptime(task['deadline'], '%Y-%m-%d').date() < datetime.now().date():
            task['status'] = "incomplete"  # Incompletez
            Task.update(task['_id'], status="incomplete")
            
        #update the intensity
        if task['intensity'] == "0":
            task['intensity'] = "low"
        elif task['intensity'] == "1":
            task['intensity'] = "medium"
        elif task['intensity'] == "2":
            task['intensity'] = "high"
    
    return render_template('index.html', tasks=tasks)

# Route to handle form submission
@bp.route('/create', methods=['POST'])
def create_task():
    from .models.task import Task
    title = request.form.get('taskName')
    intensity = request.form.get('intensity')
    deadline = request.form.get('deadline')
    # You may need to handle form validation here

    # Create a new Task object with the form data
    task = Task(title=title, intensity=intensity,
                status="pending", deadline=deadline)
    # Save the task to the database
    task_id = task.save()

    # Redirect back to the index page
    return redirect(url_for('main.index'))


@bp.route('/edit_task', methods=['POST'])
def edit_task():
    from .models.task import Task
    task_id = request.form.get('task_id')
    edited_task_name = request.form.get('editTaskName')
    edited_intensity = request.form.get('editIntensity')
    edited_status = request.form.get('editStatus')
    edited_deadline = request.form.get('editDeadline')

    # Update the task with the edited information
    Task.update(task_id, title=edited_task_name, intensity=edited_intensity, status=edited_status, deadline=edited_deadline)

    # Redirect the user back to the homepage or wherever you want
    return redirect(url_for('main.index'))

@bp.route('/delete', methods=['POST'])
def delete_entry():
    from .models.task import Task
    task_id = request.form.get('taskId')
    if task_id:
        Task.delete(task_id)
        return 'Entry deleted successfully', 200
    else:
        return 'Task ID not provided', 400
