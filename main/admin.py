
from django.contrib import admin
from .models import Award, Nominee, Vote, Winner


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0
    readonly_fields = ('user', 'nominee', 'award', 'voted_at')
    can_delete = False


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'vote_count')
    inlines = [VoteInline]

    def vote_count(self, obj):
        return obj.votes.count()

    vote_count.short_description = 'Голосов'


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram', 'vote_count')

    def vote_count(self, obj):
        return obj.votes.count()

    vote_count.short_description = 'Голосов'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'nominee', 'award', 'voted_at')
    list_filter = ('award', 'nominee')
    search_fields = ('user__username', 'nominee__name')

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('nominee', 'award')