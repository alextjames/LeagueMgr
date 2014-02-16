import random
import string
import json
from flask import Blueprint, request, redirect, render_template, url_for, session, make_response
from flask.views import MethodView
from LeagueMgr.models import League, Participant
from flask.ext.mongoengine.wtf import model_form
from flask_peewee.utils import slugify
from LeagueMgr import clientId

pages = Blueprint('pages', __name__, template_folder='templates')

class ProfileInfo(MethodView):
    
    def get(self):
        userData = session.get('userData')
        
        data = {} 
        if userData is None:
            data['state'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
            session['state'] = data['state']
            response = make_response( json.dumps( data ), 200 ) 
            response.headers['Content-Type'] = 'application/json'
            return response  
        else:
            data['userId'] = userData.userId
            data['picture'] = userData.picture
            data['displayName'] = userData.displayName

            response = make_response( json.dumps( data ), 200 ) 
            response.headers['Content-Type'] = 'application/json'
            return response  

    def post(self):        
        if request.args.get('state', '') != session['state']:
            response = make_response(json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        data = request.get_json()
        session['userData'] = data 

        make_response( json.dumps('Stored user information' ) )
        response.headers['Content-Type'] = 'application/json'
        return response
 
class LeagueListView(MethodView):

    def get(self):
        leagues = League.objects.limit(10)
        return render_template('leagues/list.html', leagues=leagues)

class LeagueCreateView(MethodView):
    form = model_form( League, exclude=['created_at','slug','participants'] )

    def get(self):
        league_form = self.form(request.form)
        return render_template( 'leagues/create_league.html', form=league_form )

    def post(self):
        print( "Got the request" )
        form = self.form(request.form)

        if form.validate():
            league = League()
            form.populate_obj(league)
            
            league.slug = slugify( league.name )
            league.save()

            return redirect( url_for('pages.league_list') )
        
        return render_template( 'leagues/create_league.html', form=self.form )
             
class LeagueHomePage(MethodView):

    def get(self, slug):
        league = League.objects.get_or_404(slug=slug)       
        return render_template( 'leagues/league_home.html', league=league )

class LeagueManagePage(MethodView):
    form = model_form( Participant, exclude=['created_at','slug'] )

    def get(self, slug):
        league = League.objects.get_or_404(slug=slug)       

        participant_form = self.form(request.form) 
        return render_template( 'leagues/league_manage.html', league=league, participant_form=participant_form, slug=slug )

class LeagueCreateParticipantPage(MethodView):
    form = model_form( Participant, exclude=['created_at','slug'] )

    def post(self, slug):
        print( "Got post for ", slug )
        form = self.form(request.form)

        if form.validate():
            participant = Participant()
            form.populate_obj(participant)
            
            participant.slug = slugify( participant.name )

            league = League.objects.get_or_404(slug=slug)
            league.participants.append( participant )
            league.save()

            return ""
        
        return "" 
 
# Register the urls
pages.add_url_rule('/', view_func=LeagueListView.as_view('league_list'))
pages.add_url_rule('/create_league', view_func=LeagueCreateView.as_view('league_create'))
pages.add_url_rule('/league/<slug>/', view_func=LeagueHomePage.as_view('league_home'))
pages.add_url_rule('/league_manage/<slug>/', view_func=LeagueManagePage.as_view('league_manage'))
pages.add_url_rule('/league_manage/<slug>/create_participant', view_func=LeagueCreateParticipantPage.as_view('create_participant'))

pages.add_url_rule('/profileInfo', view_func=ProfileInfo.as_view('profile_info'))
