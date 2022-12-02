from django.contrib import admin

from .admins import EventAdmin
from .admins import InscriptionAdmin
from .admins import CompetitorAdmin
from .admins import SectionAdmin
from .admins import SectionTimeAdmin
from .models import EventModel
from .models import InscriptionModel
from .models import CompetitorModel
from .models import SectionModel
from .models import SectionTimeModel

admin.site.register(EventModel, EventAdmin)
admin.site.register(InscriptionModel, InscriptionAdmin)
admin.site.register(CompetitorModel, CompetitorAdmin)
admin.site.register(SectionModel, SectionAdmin)
admin.site.register(SectionTimeModel, SectionTimeAdmin)
