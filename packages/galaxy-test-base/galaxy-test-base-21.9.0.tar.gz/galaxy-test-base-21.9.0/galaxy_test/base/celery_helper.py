from functools import wraps


def rebind_container_to_task(app):
    import galaxy.app
    galaxy.app.app = app
    from galaxy.celery import tasks

    def magic_bind_dynamic(func):
        return wraps(func)(app.magic_partial(func, shared=None))

    for task in tasks.CELERY_TASKS:
        task_fn = getattr(tasks, task)
        task_fn = getattr(task_fn, '__wrapped__', task_fn)
        container_bound_task = magic_bind_dynamic(task_fn)
        setattr(tasks, task, container_bound_task)
