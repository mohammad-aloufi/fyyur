#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from models import *
import json
import dateutil.parser
import babel
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#



# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    #Show venues

#Setup the things we need first

    data = []
    venues = Venue.query.all()

    places = Venue.query.distinct(Venue.city, Venue.state).all()

    for place in places:
        data.append({
            'city': place.city,
            'state': place.state,
            'venues': [{
                'id': venue.id,
                'name': venue.name,
            } for venue in venues if
                venue.city == place.city and venue.state == place.state]
        })

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    #search for venues
    search =Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))

    response ={'count': search.count(), 'data':search}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    
    #We setup the things we need first
    time =datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    venue =Venue.query.get(venue_id)
    past_shows =db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Show.start_time < time).all()
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Show.start_time > time).all()
    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'address': venue.address,
        'website': venue.website,
        'facebook_link': venue.facebook_link,
        'image_link': venue.image_link,
        'past_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in past_shows],
            'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in upcoming_shows],
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
    }
    

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm( )
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
#Add entry   to database
    form = VenueForm(request.form)
    try:
        new_venue =Venue()
        form.populate_obj(new_venue)
        db.session.add(new_venue)
        db.session.commit()
#            on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
#            Flash an error if couldn't add entry

        flash('Error: Could not add {} as a venue. {}'.format(request.form.keys, sys.exc_info()))
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    #Delete a venue
    try:
        Venue.query.filter_by(id =venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return None


#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    #View artists when clicking at the artists link in homepage
    data =[]
    artists =Artist.query.all()

    for artist in artists:
        data.append({'id': artist.id,'name': artist.name})

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    #Search artists
    search =Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))

    response ={'count': search.count(), 'data':search}
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    #Show artist by id
        #We setup the things we need first
    time =datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    show_artist =Artist.query.get(artist_id)
    venue =Venue.query.get(artist_id)
    past_shows =db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.artist_id == artist_id, Show.artist_id == Artist.id, Show.start_time < time).all()
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.artist_id == artist_id, Show.artist_id == Artist.id, Show.start_time > time).all()
    data = {
        'id': show_artist.id,
        'name': show_artist.name,
        'genres': show_artist.genres,
        'city': show_artist.city,
        'state': show_artist.state,
        'phone': show_artist.phone,
        'website': show_artist.website,
        'facebook_link': show_artist.facebook_link,
        'image_link': show_artist.image_link,
        'past_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in past_shows],
            'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in upcoming_shows],
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
    }
    

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    editing_artist = Artist.query.get(artist_id)

    artist ={'id': editing_artist.id, 'name': editing_artist.name, 'genres': editing_artist.genres, 'city': editing_artist.city, 'state': editing_artist.state, 'phone': editing_artist.phone, 'facebook_link': editing_artist.facebook_link, 'image_link': editing_artist.image_link, 'website': editing_artist.website, 'seeking_venue': editing_artist.seeking_venue, 'seeking_description': editing_artist.seeking_description}
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    #Edit artist
    form = ArtistForm()
    try:
        editing_artist = Artist.query.get(artist_id)
        editing_artist(name=request.form['name'], genres=request.form.getlist('genres'), city=request.form['city'], state=request.form['state'], phone=request.form['phone'], website=request.form['website'], facebook_link=request.form['facebook_link'], image_link=request.form['image_link'], seeking_venue=venue, seeking_description=request.form['seeking_description'])

        db.session.commit()
        #            on successful editing, insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully edited!')
    except:
        #            Flash an error if couldn't edit entry

        flash('Error: Could not edit {}. {}'.format(request.form['facebook_link'], sys.exc_info()))

    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    editing_venue = Venue.query.get(venue_id)

    venue ={'id': editing_venue.id, 'name': editing_venue.name, 'genres': editing_venue.genres, 'city': editing_venue.city, 'state': editing_venue.state, 'phone': editing_venue.phone, 'facebook_link': editing_venue.facebook_link, 'image_link': editing_venue.image_link, 'website': editing_venue.website, 'seeking_talent': editing_venue.seeking_talent, 'seeking_description': editing_venue.seeking_description}

    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    #Edit venue
    form = venueForm()
    try:
        editing_venue = Artist.query.get(venue_id)
        editing_venue (name=request.form['name'], genres=request.form.getlist('genres'), address=request.form['address'], city=request.form['city'], state=request.form['state'], phone=request.form['phone'], facebook_link=request.form['facebook_link'], image_link=request.form['image_link'], seeking_talent=talent, seeking_description=request.form['seeking_description'])
        db.session.commit()
#            on successful editing insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully edited!')
    except:
#            Flash an error if couldn't edit entry

        flash('Error: Could not edit {}. {}'.format(request.form.keys(), sys.exc_info()))


    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    #Create new artist
    form = ArtistForm(request.form)
    try:
        new_artist =Artist()
        form.populate_obj(new_artist)
        db.session.add(new_artist)
        db.session.commit()
#            on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
#            Flash an error if couldn't add entry

        flash('Error: Could not add {} as an artist. {}'.format(request.form['facebook_link'], sys.exc_info()))

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    #View shows when clicking at the shows link in homepage
    data =[]
    shows =Show.query.all()

    for show in shows:
        data.append({'venue_id': show.venue_id, 'venue_name': show.Venue.name, 'artist_id': show.artist_id, 'start_time': show.start_time})
    print (len(data))
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)
    try:
        new_show =Show()
        form.populate_obj(new_show)
        db.session.add(new_show)
        db.session.commit()
#            on successful db insert, flash success
        flash('Show was added')
    except:
#            Flash an error if couldn't add entry

        flash('Unable to add show {}'.format( sys.exc_info()))

    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
