$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        // Button that triggered the modal
        const button = $(event.relatedTarget)
        // Extract info from data-* attributes
        const taskID = button.data('source') // could be item id or 'New Task'
        const task = button.data('task')
        const priority = button.data('priority')
        const duration = button.data('duration')

        const modal = $(this)
        if (taskID === 'New Task') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (task) {
            modal.find('.form-control').val(task);
        } else {
            modal.find('.form-control').val('');
        }

        if (priority) {
            $('#priority-select').val(priority);
        } else {
            $('#priority-select').val('');
        }

        if (duration) {
            $('#duration-input').val(duration);
        } else {
            $('#duration-input').val('');
        }
    })


    $('#submit-task').click(function () {
        const task = $('#task-modal').find('.form-control').val()
        const priority = $('#priority-select').val()
        const duration = $('#duration-input').val()
        console.log(task, priority, duration)
        // accounts for number only inputs
        if (!task || !priority || !duration) {
            alert('All fields must be filled out correctly.');
            return;
        }
        const tID = $('#task-form-display').attr('taskID');
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'task': $('#task-modal').find('.form-control').val(),
                'priority': $('#priority-select').val(),
                'duration': $('#duration-input').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#generate-report').click(function () {
        const priority = $('#prioritySelect').val()
        console.log(priority)
        $.ajax({
            type: 'POST',
            url: '/generate-report',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'priority': priority
            }),
            success: function (res) {
                console.log(res.response)
                // Redirect to /report
                window.location.href = '/report';
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.state').click(function () {
        const state = $(this)
        const tID = state.data('source')
        let new_state = "Todo"
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});