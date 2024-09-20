from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from .models import Post, Comment, Team, Player, Series, Lineup, Match, Round, PlayerTick, BombEvent, Grenade, WeaponFires, Kills, Stat, Strategy, StrategyType, Map, SeriesReview, SeriesReviewComment, Notification, UploadedDemo, UploadedDemoFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.urls import reverse,resolve
from .forms import CreateTeamForm
from django.core.exceptions import PermissionDenied
from django.test import SimpleTestCase
from . import views

#models testing

class PostModelTest(TestCase):
    def test_create_post(self):
        post = Post.objects.create(title="Test Post", content="Test content")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "Test content")

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Test Post', content='Test Content')
        
    def test_create_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, text="Test Comment")
        self.assertEqual(comment.text, "Test Comment")
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)

class TeamModelTest(TestCase):
    def test_create_team(self):
        team = Team.objects.create(name="Test Team")
        self.assertEqual(team.name, "Test Team")

class PlayerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="playeruser")
    
    def test_create_player(self):
        player = Player.objects.create(user=self.user, nick_name="Player1", real_name="Real Name")
        self.assertEqual(player.nick_name, "Player1")
        self.assertEqual(player.real_name, "Real Name")
        self.assertEqual(player.user.username, "playeruser")

class MatchModelTest(TestCase):
    def setUp(self):
        self.team_a = Team.objects.create(name="Team A")
        self.team_b = Team.objects.create(name="Team B")
        self.lineup_a = Lineup.objects.create(clanName="Lineup A", team=self.team_a)
        self.lineup_b = Lineup.objects.create(clanName="Lineup B", team=self.team_b)
        self.series = Series.objects.create(title="Test Series")

    def test_create_match(self):
        match = Match.objects.create(
            date=timezone.now(),
            team_a_lineup=self.lineup_a,
            team_b_lineup=self.lineup_b,
            map="Test Map",
            series=self.series,
            tick_rate=128
        )
        self.assertEqual(str(match), "Test Map : Lineup A vs Lineup B")

class RoundModelTest(TestCase):
    def setUp(self):
        self.match = Match.objects.create(date=timezone.now())
        self.lineup = Lineup.objects.create(clanName="Lineup A")

    def test_create_round(self):
        round_instance = Round.objects.create(
            match_id=self.match,
            round_num=1,
            isWarmup=False,
            winningSide="CT",
            winningTeam=self.lineup,
            roundEndReason="T victory"
        )
        self.assertEqual(round_instance.round_num, 1)
        self.assertEqual(round_instance.winningSide, "CT")
        self.assertEqual(str(round_instance), f"{round_instance.id}")

class PlayerTickModelTest(TestCase):
    def setUp(self):
        self.player = Player.objects.create(nick_name="iM", steam_id="76561198050250233")
        self.round = Round.objects.create()

    def test_create_player_tick(self):
        player_tick = PlayerTick.objects.create(
            round=self.round,
            player=self.player,
            name="Player1",
            side="T",
            tick=100,
            health=100.0
        )
        self.assertEqual(player_tick.side, "T")
        self.assertEqual(player_tick.health, 100.0)
        self.assertEqual(str(player_tick), f"{self.player.steam_id} : {player_tick.tick}")


class BombEventModelTest(TestCase):
    def setUp(self):
        self.round = Round.objects.create(round_num=1)
        self.player = Player.objects.create(nick_name="Player1")

    def test_create_bomb_event(self):
        bomb_event = BombEvent.objects.create(
            round=self.round,
            event="Plant",
            site="A",
            tick=120,
            player=self.player
        )
        self.assertEqual(bomb_event.event, "Plant")
        self.assertEqual(bomb_event.site, "A")
        self.assertEqual(str(bomb_event), f"{bomb_event.id}")

class GrenadeModelTest(TestCase):
    def setUp(self):
        self.round = Round.objects.create(round_num=1)
        self.player = Player.objects.create(nick_name="Player1")

    def test_create_grenade(self):
        grenade = Grenade.objects.create(
            round=self.round,
            thrower=self.player,
            thrower_name="Player1",
            grenade_type="Flash",
            tick=200
        )
        self.assertEqual(grenade.grenade_type, "Flash")
        self.assertEqual(grenade.thrower_name, "Player1")

class WeaponFiresModelTest(TestCase):
    def setUp(self):
        self.round = Round.objects.create(round_num=1)
        self.player = Player.objects.create(nick_name="Player1")

    def test_create_weapon_fires(self):
        weapon_fire = WeaponFires.objects.create(
            round=self.round,
            player=self.player,
            name="Player1",
            side="T",
            weapon="AK-47"
        )
        self.assertEqual(weapon_fire.weapon, "AK-47")

class KillsModelTest(TestCase):
    def setUp(self):
        self.attacker = Player.objects.create(nick_name="Attacker", steam_id="attacker123")
        self.victim = Player.objects.create(nick_name="Victim", steam_id="victim123")
        self.assister = Player.objects.create(nick_name="Assister", steam_id="assister123")
        self.round = Round.objects.create()

    def test_create_kill(self):
        kill = Kills.objects.create(
            round_ID=self.round,
            attacker_ID=self.attacker,
            victim_ID=self.victim,
            assister_ID=self.assister,
            isHeadshot=True,
            tick=12345,
            round_time="00:15"
        )
        self.assertIsNotNone(kill.id)
        self.assertEqual(kill.attacker_ID.nick_name, "Attacker")

class StatModelTest(TestCase):
    def setUp(self):
        self.player = Player.objects.create(nick_name="Player1")
        self.match = Match.objects.create(date=timezone.now())

    def test_create_stat(self):
        stat = Stat.objects.create(
            player=self.player,
            match=self.match,
            rating=1.25
        )
        self.assertEqual(stat.rating, 1.25)

class StrategyModelTest(TestCase):
    def setUp(self):
        self.player = Player.objects.create(nick_name="Tactician")
        self.map = Map.objects.create(name="Dust2")

    def test_create_strategy(self):
        strategy = Strategy.objects.create(
            name="Rush B",
            description="A fast push onto B site.",
            creator=self.player
        )
        strategy.maps.add(self.map)
        self.assertEqual(strategy.name, "Rush B")
        self.assertIn(self.map, strategy.maps.all())

class NotificationModelTest(TestCase):
    def setUp(self):
        self.player = Player.objects.create(nick_name="Player1")

    def test_create_notification(self):
        notification = Notification.objects.create(
            player=self.player,
            message="You have a new match!"
        )
        self.assertFalse(notification.is_read)
        self.assertEqual(notification.message, "You have a new match!")

class UploadedDemoFileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="DemoUploader")
        self.match = Match.objects.create(date=timezone.now())

    def test_create_uploaded_demo_file(self):
        uploaded_file = SimpleUploadedFile("test.dem", b"file_content", content_type="application/octet-stream")
        demo = UploadedDemo.objects.create(match=self.match, hash="demo_hash")
        demo_file = UploadedDemoFile.objects.create(
            demo=demo,
            uploaded_by=self.user,
            file=uploaded_file
        )
        # Check start "demos/test.dem" (to account for the unique string)
        self.assertTrue(demo_file.file.name.startswith("demos/test"))
        self.assertEqual(demo_file.uploaded_by, self.user)


# view testing

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.player = Player.objects.create(user=self.user, steam_id='123456789')
        self.team = Team.objects.create(name='Test Team')
        self.team.players.add(self.player)

        self.strategy = Strategy.objects.create(name='Test Strategy', creator=self.player)

        self.demo_file = UploadedDemoFile.objects.create(file="demos/test.dem", uploaded_by=self.user)

    def test_index_view(self):
        """Test the index view for rendering correct template and context."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats/index.html')
        self.assertIn('teams', response.context)

    def test_login_page_view(self):
        """Test the login view for anonymous users."""
        self.client.logout()  # Logout to test unauthenticated access
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_signup_page_view(self):
        """Test the signup view for anonymous users."""
        self.client.logout()
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_strategy_view(self):
        """Test the strategy view."""
        response = self.client.get(reverse('strategy', args=[self.strategy.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats/stratPage.html')
        self.assertIn('maps', response.context)
        self.assertIn('strat', response.context)

    def test_logout_view(self):
        """Test the logout view."""
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "You have been logged out.")

    def test_demo_view(self):
        """Test the demo view."""
        response = self.client.get(reverse('demo', args=[self.demo_file.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats/demo.html')
        self.assertIn('demoFile', response.context)



class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

        # Add user to the 'Player' group so they have access to the dashboard
        player_group, created = Group.objects.get_or_create(name='Player')
        self.user.groups.add(player_group)
        self.client.login(username='testuser', password='password')

        self.player = Player.objects.create(user=self.user, nick_name='TestPlayer', steam_id='teststeamid')
        self.team = Team.objects.create(name='Test Team')
        self.team.players.add(self.player)

        Series.objects.create(title='Test Series 1')
        Series.objects.create(title='Test Series 2')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats/dashboard.html')
        self.assertContains(response, 'Test Series 1')
        self.assertContains(response, 'Test Series 2')

#template testing

class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        player_group, created = Group.objects.get_or_create(name='Player')
        self.user.groups.add(player_group)
        self.client.login(username='testuser', password='password')

        self.player = Player.objects.create(user=self.user, nick_name='TestPlayer', steam_id='teststeamid')

    def test_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')



# Forms testing
class CreateTeamFormTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='password')
        self.player = Player.objects.create(user=self.user, nick_name='TestPlayer', steam_id='teststeamid')

    def test_form_valid(self):
        
        form_data = {
            'name': 'Test Team',
            'players': [self.player.steam_id],  
            'team_img_url': 'http://example.com/image.png'
        }
        form = CreateTeamForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_form_invalid(self):
        
        form_data = {
            'name': '',  
            'players': [],  
            'team_img_url': 'http://example.com/image.png'
        }
        form = CreateTeamForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

 
# decorator tests
class AllowedUsersDecoratorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.group = Group.objects.create(name='Player')
        self.user.groups.add(self.group)
        self.client.login(username='testuser', password='password')

        self.player = Player.objects.create(user=self.user, nick_name='TestPlayer', steam_id='teststeamid')
        self.team = Team.objects.create(name='Test Team')
        self.team.players.add(self.player)

        Series.objects.create(title='Test Series 1')
        Series.objects.create(title='Test Series 2')

    def test_allowed_role_access(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats/dashboard.html')

    def test_disallowed_role_access(self):
        self.user.groups.remove(self.group)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 403)

class UnauthenticatedUserDecoratorTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='password')
        self.group = Group.objects.create(name='Player')
        self.user.groups.add(self.group)
        self.player = Player.objects.create(user=self.user)

    def test_authenticated_user_redirect(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('signup'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_unauthenticated_user_access(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)


#URL testing


class URLTests(SimpleTestCase):

    def test_index_url(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signupPage)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout)

    def test_dashboard_url(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, views.dashboard)

    def test_player_detail_url(self):
        url = reverse('player_detail', args=['player1'])
        self.assertEqual(resolve(url).func, views.player_detail)

    def test_series_detail_url(self):
        url = reverse('series_detail', args=[1])
        self.assertEqual(resolve(url).func, views.series_detail)

    def test_match_detail_url(self):
        url = reverse('match_detail', args=[1])
        self.assertEqual(resolve(url).func, views.match_detail)

    def test_team_comms_url(self):
        url = reverse('team_comms', args=[1])
        self.assertEqual(resolve(url).func, views.team_comms)

    def test_teams_url(self):
        url = reverse('teams')
        self.assertEqual(resolve(url).func, views.teams)

    def test_d3_url(self):
        url = reverse('d3')
        self.assertEqual(resolve(url).func, views.d3)

    def test_d3_round_url(self):
        url = reverse('d3_round')
        self.assertEqual(resolve(url).func, views.d3_round)

    def test_create_team_url(self):
        url = reverse('create_team')
        self.assertEqual(resolve(url).func, views.create_team)

    def test_round_view_url(self):
        url = reverse('round_view', args=[1])
        self.assertEqual(resolve(url).func, views.round_view)

    def test_round_ticks_url(self):
        url = reverse('round_ticks', args=[1])
        self.assertEqual(resolve(url).func, views.round_ticks)

    def test_kills_url(self):
        url = reverse('kills', args=[1])
        self.assertEqual(resolve(url).func, views.kills)

    def test_stratPage_url(self):
        url = reverse('stratPage')
        self.assertEqual(resolve(url).func, views.stratPage)

    def test_strategies_url(self):
        url = reverse('strategies')
        self.assertEqual(resolve(url).func, views.strategies)

    def test_create_strategy_url(self):
        url = reverse('create_strategy')
        self.assertEqual(resolve(url).func, views.create_strategy)

    def test_add_strategy_url(self):
        url = reverse('add_strategy')
        self.assertEqual(resolve(url).func, views.add_strategy)

    def test_strategy_url(self):
        url = reverse('strategy', args=[1])
        self.assertEqual(resolve(url).func, views.strategy)

    def test_strategy_canvas_url(self):
        url = reverse('strategy_canvas', args=[1])
        self.assertEqual(resolve(url).func, views.strategy_canvas)

    def test_parsedemo_url(self):
        url = reverse('parsedemo', args=[1])
        self.assertEqual(resolve(url).func, views.parsedemo)

    def test_demo_url(self):
        url = reverse('demo', args=[1])
        self.assertEqual(resolve(url).func, views.demo)

    def test_demos_url(self):
        url = reverse('demos', args=[1])
        self.assertEqual(resolve(url).func, views.demos)

    def test_notifications_url(self):
        url = reverse('notifications')
        self.assertEqual(resolve(url).func, views.notifications)

    def test_read_notifications_url(self):
        url = reverse('read_notifications')
        self.assertEqual(resolve(url).func, views.read_notifications)

    def test_read_notification_url(self):
        url = reverse('read_notification')
        self.assertEqual(resolve(url).func, views.read_notification)

    def test_login_url(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  


