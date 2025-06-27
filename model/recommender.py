import pandas as pd
from difflib import get_close_matches


class MusicRecommender:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        # Add lowercase versions for matching
        self.data['SongTitleLower'] = self.data['SongTitle'].str.lower()
        self.data['GenreLower'] = self.data['Genre'].str.lower()
        self.data['MusicianLower'] = self.data['Musician'].str.lower()

    def recommend(self, query):
        query = query.strip().lower()

        # Match by song title
        if query in self.data['SongTitleLower'].values:
            return self._recommend_by_song_title(query)

        # Match by genre
        if query in self.data['GenreLower'].values:
            return self._filter_by_genre(query)

        # Match by musician
        if query in self.data['MusicianLower'].values:
            return self._filter_by_musician(query)

        # Match by rating (numerical)
        if query.isdigit():
            return self._filter_by_rating(int(query))

        # Suggest similar matches
        return self._suggest_close_matches(query)

    def _recommend_by_song_title(self, song_title):
        # Get reference row
        row = self.data[self.data['SongTitleLower'] == song_title].iloc[0]
        genre = row['GenreLower']
        musician = row['MusicianLower']
        rating = row['Rating']

        # Filter similar songs
        results = self.data[
            (self.data['GenreLower'] == genre) |
            (self.data['MusicianLower'] == musician) |
            (self.data['Rating'] >= rating)
        ]

        # Exclude the same song from results
        results = results[results['SongTitleLower'] != song_title]

        return self._format_results(results)

    def _filter_by_genre(self, genre):
        results = self.data[self.data['GenreLower'] == genre]
        return self._format_results(results)

    def _filter_by_musician(self, musician):
        results = self.data[self.data['MusicianLower'] == musician]
        return self._format_results(results)

    def _filter_by_rating(self, rating):
        results = self.data[self.data['Rating'] >= rating]
        return self._format_results(results)

    def _format_results(self, results):
        if results.empty:
            return ["No matches found."]
        return results[['SongTitle', 'Musician', 'Genre', 'Rating']] \
            .drop_duplicates() \
            .head(10) \
            .apply(
                lambda row: f"{row['SongTitle']} by {row['Musician']} ({row['Genre']}, Rating: {row['Rating']})",
                axis=1
            ).tolist()

    def _suggest_close_matches(self, query):
        matches = get_close_matches(query, self.data['SongTitle'].unique(), n=5, cutoff=0.5)
        return [f"Did you mean: {match}?" for match in matches] if matches else ["No close matches found."]
