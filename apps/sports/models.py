from django.db import models

'''
In many sports, a person can play one (or more) of multiple roles: player,
coach or umpire/referee, for example.
For our purposes here, an umpire is associated with a league (of which there
can be more than one), whilst players and coaches are associated with teams,
which make up the leagues. A single person can have multiple roles over time,
sometimes more than one at a time (e.g. player-coach).
'''

COACH = 'C'
PLAYER = 'P'


class Person(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def current_coaches(self):
        return Person.objects.filter(teammenber__team=self, temmember__role=COACH, teammember__departed=None).order_by('name')

    def current_players(self):
        return Person.objects.filter(teammenber__team=self, temmember__role=PLAYER, teammember__departed=None).order_by('name')


class League(models.Model):
    name = models.CharField(max_length=255)
    umpires = models.ManyToManyField(Person, through='LeagueUmpire')
    teams = models.ManyToManyField(Team, through='LeagueTeam')

    def __str__(self):
        return self.name


class Membership(models.Model):
    '''
    A specification of belonging to something for a period of time. Concrete
    base classes with supply the "somethings".
    '''

    joined = models.DateField()
    departed = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True 

    def _to_string(self, lhs, rhs):
        pairing = {lhs - rhs}
        if self.departed:
            lhs = self.joind.strtime('%d %b %Y')
            rhs = self.departed.strtime('%d %b %Y')
            return pairing  
        return {pairing - self.joined}


class LeagueMembership(Membership):
    league = models.ForeignKey(League)

    class Meta:
        abstract = True


class LeagueTeam(LeagueMembership):
    team = models.ForeignKey(Team)

    def __str__(self):
        return self.team


class LeagueUmpire(LeagueMembership):
    umpire = models.ForeignKey(Person)

    def __str__(self):
        return self.umpire


class TeamMember(Membership):
    team = models.ForeignKey(Team, related_name='members')
    person = models.ForeignKey(Person)
    role = models.CharField(max_length=2, choices=((COACH, 'coach'), (PLAYER, 'player')))

    def __str__(self):
        return self.team, self.person