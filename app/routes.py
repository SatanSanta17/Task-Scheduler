from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for
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
    tasks = Task.find_all()
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
                status="Pending", deadline=deadline)
    # Save the task to the database
    task_id = task.save()

    # Redirect back to the index page
    return redirect(url_for('main.index'))
