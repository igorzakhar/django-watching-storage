from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = [
        {
            'who_entered': visit.passcard,
            'entered_at': visit.entered_at,
            'duration': visit.format_duration(visit.get_duration())
        }
        for visit in visits
    ]

    context = {
        'non_closed_visits': non_closed_visits,
    }

    return render(request, 'storage_information.html', context)
