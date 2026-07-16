from todo_service import *

print(add_task("לקנות חלב"))

print(add_task("להגיש עבודה"))

print(get_tasks())

update_task(
    1,
    status="בוצע"
)

print(get_tasks())

delete_task(2)

print(get_tasks())