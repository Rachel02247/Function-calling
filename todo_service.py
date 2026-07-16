tasks = []
next_id = 1


def get_tasks(filters=None):
    """
    מחזיר את כל המשימות.
    בהמשך נוסיף סינון.
    """

    if filters is None:
        return tasks

    result = tasks

    if "status" in filters:
        result = [
            task for task in result
            if task["status"] == filters["status"]
        ]

    if "type" in filters:
        result = [
            task for task in result
            if task["type"] == filters["type"]
        ]

    return result


def add_task(
    title,
    description="",
    task_type="כללי",
    start_date="",
    end_date="",
    status="חדש"
):
    global next_id

    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "type": task_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": status
    }

    tasks.append(task)

    next_id += 1

    return task


def update_task(task_id, **updates):

    for task in tasks:

        if task["id"] == task_id:

            task.update(updates)

            return task

    return None


def delete_task(task_id):

    global tasks

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            return True

    return False