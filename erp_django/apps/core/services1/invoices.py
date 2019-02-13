from apps.core.models import DevelopersOnProject


def get_project_developers_and_cost(project):
    developers_on_project = [dev for dev in DevelopersOnProject.objects.filter(project=project).select_related('developer')]
    developers = list()
    total_cost = 0 if not project.basic_price else project.basic_price
    for info in developers_on_project:
        dev = info.developer
        cost = round(dev.hourly_rate * info.hours, 2)
        dev = dict(id=dev.id,
                   worked_hours=info.hours,
                   description=info.description,
                   hourly_rate=dev.hourly_rate,
                   cost=cost)
        if not project.basic_price:
            total_cost += cost
        developers.append(dev)

    return developers, total_cost
