from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Station(db.Model):
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    channels = db.relationship("Channel", back_populates="station")

    def __init__(self, name):
        self.name = name




class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))
    station = db.relationship("Station", back_populates="channels")

    songs = db.relationship("Song", back_populates="channel")

    def __init__(self, name, station_id):
        self.name = name
        self.station_id = station_id



class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True, nullable=False)
    album = db.Column(db.String(120))
    length = db.Column(db.Integer, nullable=False)

    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    channel = db.relationship("Channel", back_populates="songs")

    def __init__(self, name, album, length, channel_id):
        self.name = name
        self.album = album
        self.length = length
        self.channel_id = channel_id




meta = db.metadata
for table in reversed(meta.sorted_tables):               #drop_all_tables
    print ('Clear table %s' % table)
    db.session.execute(table.delete())
db.session.commit()


db.create_all()

myStation = Station('myStation')
myStation1 = Station('myStation1')
myStation2 = Station('myStation2')
myStation3 = Station('myStation3')

myChannel = Channel('myChannel', 1)
myChannel1 = Channel('myChannel1', 1)
myChannel2 = Channel('myChannel2', 1)
myChannel3 = Channel('myChannel3', 1)
myChannel4 = Channel('myChannel4', 2)
myChannel5 = Channel('myChannel5', 2)
myChannel6 = Channel('myChannel6', 2)
myChannel7 = Channel('myChannel7', 3)
myChannel8 = Channel('myChannel8', 4)

mySong = Song('mySong', 'Album', 180, 9)
mySong1 = Song('mySong1', 'Album', 180, 1)
mySong2 = Song('mySong2', 'Album', 180, 2)
mySong3 = Song('mySong3', 'Album', 180, 3)
mySong4 = Song('mySong4', 'Album', 180, 4)
mySong5 = Song('mySong5', 'Album', 180, 5)
mySong6 = Song('mySong6', 'Album', 180, 6)
mySong7 = Song('mySong7', 'Album', 180, 7)
mySong8 = Song('mySong8', 'Album', 180, 8)
mySong9 = Song('mySong9', 'Album', 180, 9)
mySong10 = Song('mySong10', 'Album', 180, 1)
mySong11 = Song('mySong11', 'Album', 180, 2)
mySong12 = Song('mySong12', 'Album', 180, 3)
mySong13 = Song('mySong13', 'Album', 180, 4)
mySong14 = Song('mySong14', 'Album', 180, 5)

db.session.add_all([myStation, myStation1, myStation2, myStation3, myChannel, myChannel1, myChannel2, myChannel3, myChannel4, myChannel5, myChannel6, myChannel7, myChannel8,
                    mySong, mySong1, mySong2, mySong3, mySong4, mySong5, mySong6, mySong7, mySong8, mySong9, mySong10, mySong11, mySong12, mySong13, mySong14])

db.session.commit()

print(Station.query.all())
print(Channel.query.all())
print(Song.query.all())


def getJsonFromClasslist(classlist, arrayName):
    array = []

    for u in classlist:
        array.append(u.__dict__['name'])

    data = {
        arrayName: str(array)
    }
    resp = jsonify(data)
    return resp


def getJsonItemsByKey(keyName, keyValue, sourceArray, responseArrayName):
    array = []

    kwargs = {keyName: keyValue}

    for u in sourceArray.query.filter_by(**kwargs).all():
        array.append(u.__dict__['name'])

    data = {
        responseArrayName: str(array)
    }
    resp = jsonify(data)
    return resp


@app.route('/')
def api_root():
    return 'Welcome to K-DST radio station'

@app.route('/stations')
def api_stations():
    response = getJsonFromClasslist(db.session.query(Station).all(), 'stations')
    return response

@app.route('/channels')
def api_channels():
    response = getJsonFromClasslist(db.session.query(Channel).all(), 'channels')
    return response

@app.route('/songs')
def api_songs():
    response = getJsonFromClasslist(db.session.query(Song).all(), 'songs')
    return response

@app.route('/<stationName>')
def api_channels_by_station(stationName):
    try:
        stationId = Station.query.filter_by(name=stationName).first().__dict__['id']
    except:
        response = "Seems like the station you entered doesn't excist!\n"
        return response


    response = getJsonItemsByKey('station_id', stationId, Channel, 'channels')
    return response


@app.route('/<channelName>/')
def api_songs_by_channel(channelName):
    try:
        channelId = Channel.query.filter_by(name=channelName).first().__dict__['id']
    except:
        response = "Seems like the channel you entered doesn't excist!\n"
        return response

    response = getJsonItemsByKey('channel_id', channelId, Song, 'songs')
    return response


if __name__ == '__main__':
    app.run()