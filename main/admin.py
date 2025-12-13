from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from .models import Award, Nominee, Vote, Winner


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0
    readonly_fields = ('user', 'nominee', 'award', 'voted_at')
    can_delete = False


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'vote_count', 'top_nominees', 'current_leader', 'is_major')
    inlines = [VoteInline]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('is_major',)
    search_fields = ('name', 'description')

    def vote_count(self, obj):
        return obj.votes.count()

    vote_count.short_description = 'Всего голосов'
    vote_count.admin_order_field = 'votes__count'

    def top_nominees(self, obj):
        """Показывает всех номинантов с количеством голосов в этой номинации"""
        nominees_stats = (
            Vote.objects
            .filter(award=obj)
            .values('nominee__name')
            .annotate(vote_count=Count('id'))
            .order_by('-vote_count')
        )
        
        if not nominees_stats:
            return "Нет голосов"
        
        result = []
        for idx, stat in enumerate(nominees_stats, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "•"
            result.append(f"{medal} {stat['nominee__name']}: {stat['vote_count']} голосов")
        
        return format_html("<br>".join(result))
    
    top_nominees.short_description = 'Результаты по номинации'

    def current_leader(self, obj):
        """Показывает текущего лидера по голосам"""
        top_vote = (
            Vote.objects
            .filter(award=obj)
            .values('nominee__name')
            .annotate(vote_count=Count('id'))
            .order_by('-vote_count')
            .first()
        )
        
        if top_vote:
            return format_html(
                '<strong style="color: #28a745;">🏆 {} ({} голосов)</strong>',
                top_vote['nominee__name'],
                top_vote['vote_count']
            )
        
        return "Нет голосов"
    
    current_leader.short_description = 'Текущий лидер'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(vote_count_agg=Count('votes'))


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram', 'vote_count', 'awards_list')
    search_fields = ('name', 'telegram')
    list_filter = ('awards',)

    def vote_count(self, obj):
        return obj.votes.count()

    vote_count.short_description = 'Всего голосов'
    vote_count.admin_order_field = 'votes__count'

    def awards_list(self, obj):
        """Показывает номинации и количество голосов в каждой"""
        awards_stats = (
            Vote.objects
            .filter(nominee=obj)
            .values('award__name')
            .annotate(vote_count=Count('id'))
            .order_by('-vote_count')
        )
        
        if not awards_stats:
            return "Нет голосов"
        
        result = []
        for stat in awards_stats:
            result.append(f"{stat['award__name']}: {stat['vote_count']}")
        
        return format_html("<br>".join(result))
    
    awards_list.short_description = 'Голоса по номинациям'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'nominee', 'award', 'voted_at')
    list_filter = ('award', 'nominee', 'voted_at')
    search_fields = ('user__username', 'nominee__name', 'award__name')
    readonly_fields = ('voted_at',)
    date_hierarchy = 'voted_at'

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('nominee', 'award')
    list_filter = ('award',)
    search_fields = ('nominee', 'award__name')