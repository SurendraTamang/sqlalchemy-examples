# Many to Many relationship in SQLALchemy


# Example showing and how to do it

This is the working example how how I was able to make the m2m relations working. Will explain more in future

#TODO - Work on explanation

```python
  from sqlalchemy import create_engine, Integer, String, ForeignKey, Table, JSON, Column
  from sqlalchemy.orm import DeclarativeBase, relationship, Session
  from enums import WatchList # For Yes or No
  
  
  class Base(DeclarativeBase):
      pass
  
  
  class PlaylistTracks(Base):
      __tablename__ = "playlist_tracks"
      playlist_id = Column(Integer, ForeignKey("spotify_playlists.id"), primary_key=True)
      track_id = Column(Integer, ForeignKey("spotify_tracks.id"), primary_key=True)
      playlist = relationship("SpotifyPlaylists", back_populates="tracks")
      track = relationship("SpotifyTracks", back_populates="playlists")
  
  
  class TracksArtists(Base):
      __tablename__ = "tracks_artists"
      track_id = Column(Integer, ForeignKey("spotify_tracks.id"), primary_key=True)
      artist_id = Column(Integer, ForeignKey("spotify_artists.id"), primary_key=True)
      track = relationship("SpotifyTracks", back_populates="artists")
      artist = relationship("SpotifyArtists", back_populates="tracks")
  
  
  class SpotifyArtists(Base):
      __tablename__ = "spotify_artists"
      id = Column(Integer, primary_key=True)
      name = Column(String(200), name="Name")
      uri = Column(String(200), name="URI", unique=True)
      popularity_score = Column(Integer, name="Popularity Score")
      details = Column(JSON, name="Details")
      genres = Column(JSON, name="Genres")
      followers = Column(Integer, name="Followers")
      tracks = relationship("TracksArtists", back_populates="artist")
  
  
  class SpotifyTracks(Base):
      __tablename__ = "spotify_tracks"
      id = Column(Integer, primary_key=True)
      name = Column(String(200), name="Name")
      uri = Column(String(200), name="URI", unique=True)
      popularity_score = Column(Integer, name="Popularity Score")
      album = Column(JSON, name="Album")
      external_ids = Column(JSON, name="External IDs")
      external_url = Column(JSON, name="External URL")
      href = Column(String(200), name="Href")
      playlists = relationship("PlaylistTracks", back_populates="track")
      artists = relationship("TracksArtists", back_populates="track")
  
  
  class SpotifyPlaylists(Base):
      __tablename__ = "spotify_playlists"
      id = Column(Integer, primary_key=True)
      name = Column(String(200), name="Name")
      uri = Column(String, unique=True, name="URI")
      cover_art = Column(String(150), name="Cover Art")
      details = Column(JSON, name="Details")
      watchlist = Column(String(3), default=WatchList.YES.value, name="Watchlist")
      tracks = relationship("PlaylistTracks", back_populates="playlist")
  

  if __name__ == "__main__":

      # making echo true will show our sql logs
      engine = create_engine(
          "postgresql://<username>:<password>@<host>/<db_name>", echo=True
      )
  
      # Base.metadata.drop_all(engine)  # Uncomment to drop tables
      # Base.metadata.create_all(engine)  # Uncomment to recreate tables
  
      session = Session(engine)
      playlist_ids = [
          "37i9dQZF1DXcBWIGoYBM5M",
          "4A01B3wh6uv7yOpzYdVLR3",
          "37i9dQZF1DX68H8ZujdnN7",
          "37i9dQZF1DX0H8hDpv38Ju",
      ]
      artist_ids = [
          "spotify:track:0Z7nGFVCLfixWctgePsRk9",
          "spotify:track:6tNQ70jh4OwmPGpYy6R2o9",
          "spotify:track:6Qb7YsAqH4wWFUMbGsCpap",
      ]
      # # Bulk insert artists
      tracks = list()
      query = (
          session.query(SpotifyPlaylists)
          .where(SpotifyPlaylists.uri == playlist_ids[1])
          .first()
      )
  
      for artist_id in artist_ids:
          artist = session.query(SpotifyTracks).filter_by(uri=artist_id).first()
          if artist:
              query.tracks.append(PlaylistTracks(track=artist, playlist=query))
          else:
              breakpoint()
  
      session.commit()
  
      # # Bulk insert playlists
      # for playlist_id in playlist_ids:
      #     playlist = SpotifyPlaylists(uri=playlist_id)
      #     session.add(playlist)
      # session.commit()
  
      # # Create a new track
  
      # query_tracks = session.query(SpotifyTracks).filter_by(name="My Track 1").first()
      # track = SpotifyTracks(
      #     name="My Track 1",
      #     uri="spotify:track:U",
      #     popularity_score=100,
      #     album={"name": "My Album 1"},
      #     external_ids={"isrc": "USAT29900643"},
      #     external_url={"spotify": "https://open.spotify.com/track/1"},
      #     href="https://api.spotify.com/v1/tracks/1",
      # )
      # session.add(track)
      # # Append the track to the playlist's tracks
      # query.tracks.append(PlaylistTracks(track=track, playlist=query))
  
      # # Create an artist and add them to the track
      # artist = SpotifyArtists(
      #     name="Artist 1",
      #     uri="spotify:artist:U",
      #     popularity_score=95,
      #     details={"detail_key": "detail_value"},
      #     genres=["pop", "dance"],
      #     followers=100000,
      # )
      # query_artists = session.query(SpotifyArtists).filter_by(name="Artist 1").first()
      # session.add(artist)
      # # Establish a many-to-many relationship between the track and the artist
      # track_artist = TracksArtists(track=query_tracks, artist=query_artists)
      # session.add(track_artist)
  
      # session.commit()
      # print("Database schema created successfully!")
```
