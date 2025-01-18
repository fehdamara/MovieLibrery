import json
import os


class MovieNotFoundError(Exception):
    """
    Eccezione personalizzata da alzare quando
    non viene trovato nessun titolo del film desiderato.
    """
    pass


class MovieLibrary:
    """
    Classe che gestisce la collezione dei film memorizzati nel file JSON.
    """

    def __init__(self, json_file: str):
        """
        Inizializza la libreria dei film.
        
        @parametro@ json_file: percorso assoluto del file movies.json.
        @alsa@ FileNotFoundError: se il file non viene trovato.
        """
        if not os.path.isfile(json_file):
            # [[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]] #
            # Esercizio 17: alza FileNotFoundError con messaggio #
            # [[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]] #
            raise FileNotFoundError(f"File not found: {json_file}")

        self.json_file = json_file

        # Carica la collezione dei film dal file JSON
        with open(self.json_file, 'r', encoding='utf-8') as file:
            self.movies = json.load(file)

    def __update_json_file(self) -> None:
        """
        Metodo privato che aggiornerà il contenuto del file JSON
        con i dati presenti dentro self.movies.
        """
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file, indent=4, ensure_ascii=False)

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 1. get_movies che restituisce l’intera collezione di film #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_movies(self) -> list:
        """
        Restituirà tutta la collezione dei film.

        @riporta@ lista dei dizionari (ciascun caso rappresenta un film).
        """
        return self.movies

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 2. add_movie che ha i parametri title e director di tipo stringa #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def add_movie(self, title: str, director: str, year: int, genres: list) -> None:
        """
        Aggiunge un nuovo film alla collezione e aggiorna il file JSON.
        
        @parametro@ title: titolo del film.
        @parametro@ director: regista del film.
        @parametro@ year: anno di uscita del film.
        @parametro@ genres: lista di generi associati al film.
        """
        new_movie = {
            "title": title,
            "director": director,
            "year": year,
            "genres": genres
        }
        self.movies.append(new_movie)
        self.__update_json_file()

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 3. remove_movie ha il parametro title ed è il metodo per rimuove dalla collezione il filmc he ha titolo corrispondente (NON case sensitive) a title#
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def remove_movie(self, title: str) -> dict:
        """
        Rimuove il film con titolo corrispondente (NON case sensitive)
        e aggiorna il file JSON. Restituirà il film rimosso.
        
        @parametro@ title: titolo del film rimosso (case insensitive).
        @ritorna@ dizionario che contiene il film rimosso.
        @alsa@ MovieNotFoundError: se non esiste nessun film con il titolo desiderato.
        """
        title_lower = title.lower()
        for idx, movie in enumerate(self.movies):
            if movie["title"].lower() == title_lower:
                removed = self.movies.pop(idx)
                self.__update_json_file()
                return removed
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
        # Esercizio 18: se non trova nessun film alsa l'errore MovieNotFoundError   #
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
        raise MovieNotFoundError("Movie was not found")

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 4. update_movie ha il parametro titlee i parametri opzionali director #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def update_movie(self, title: str, director: str = None, year: int = None, genres: list = None) -> dict:
        """
        Modifica i campi del film corrispondente al titolo (NON case sensitive)
        con i valori passati come parametri. Solo i parametri non nulli 
        verranno applicati come aggiornamento.
        Aggiorna il file JSON e restituisce il film aggiornato.
        
        @parametro@ title: titolo (case insensitive) del film da aggiornare.
        @parametro@ director: *nuovo regista*.
        @parametro@ year: *nuovo anno di uscita*.
        @parametro@ genres: *nuova lista di generi*.
        @ritorna@ dizionario con i campi aggiornati del film.
        @alsa@ MovieNotFoundError: se non esiste nesun film con il titolo specificato.
        """
        title_lower = title.lower()
        for movie in self.movies:
            if movie["title"].lower() == title_lower:
                if director is not None:
                    movie["director"] = director
                if year is not None:
                    movie["year"] = year
                if genres is not None:
                    movie["genres"] = genres
                self.__update_json_file()
                return movie
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
        # Esercizio 18: se non trova nessun film alsa l'errore MovieNotFoundError   #
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
        raise MovieNotFoundError("Movie was not found")

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 5. get_movie_titles restituisce una lista contenente tutti i titoli dei film nella collezione #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_movie_titles(self) -> list:
        """
        Restituisce la lista di tutti i titoli dei film nella collezione.
        
        @ritorna@ lista di stringhe (titoli dei film).
        """
        return [movie["title"] for movie in self.movies]

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 6. countmovies restituisce il numero totale dei film nella collezione #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def countmovies(self) -> int:
        """
        Restituisce il numero totale di film nella collezione.
        
        @ritorna@ numero totale di film.
        """
        return len(self.movies)

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 7. get_movie_by_title Restituisce il film corrispondente al titolo (NON case sensitive) #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_movie_by_title(self, title: str) -> dict:
        """
        Restituisce il film corrispondente al titolo (NON case sensitive).
        Se non esiste, restituisce None.
        
        @parametro@ title: titolo del film (case insensitive).
        @ritorna@ dizionario rappresentante il film trovato, oppure None.
        """
        title_lower = title.lower()
        for movie in self.movies:
            if movie["title"].lower() == title_lower:
                return movie
        return None

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 8. get_movies_by_title_substring Restituisce la lista di tutti i film il cui titolo #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_movies_by_title_substring(self, substring: str) -> list:
        """
        Restituisce la lista di tutti i film il cui titolo 
        contiene (case sensitive) la sottostringa specificata.
        
        @parametro@ substring: sottostringa da cercare (case sensitive).
        @ritorna@ lista di dizionari (film che contengono la sottostringa).
        """
        return [
            movie for movie in self.movies
            if substring in movie["title"]
        ]

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 9. get_movies_by_year Restituisce la lista di tutti i film usciti nell'anno specificato #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_movies_by_year(self, year: int) -> list:
        """
        Restituisce la lista di tutti i film usciti nell'anno specificato.
        
        @parametro@ year: anno di uscita.
        @ritorna@ lista di dizionari (film usciti in quell'anno).
        """
        return [
            movie for movie in self.movies
            if movie["year"] == year
        ]

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 10. count_movies_by_director Restituisce il numero di film diretti da 'director' #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def count_movies_by_director(self, director: str) -> int:
        """
        Restituisce il numero di film diretti da 'director'.
        Il confronto col nome del regista è NON case sensitive.
        
        @parametro@ director: nome del regista (case insensitive).
        @ritorna@ numero di film diretti dal regista specificato.
        """
        director_lower = director.lower()
        count = 0
        for movie in self.movies:
            if movie["director"].lower() == director_lower:
                count += 1
        return count

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 11. get_movies_by_genre Restituisce la lista dei film che hanno tra i generi 'genre' #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_movies_by_genre(self, genre: str) -> list:
        """
        Restituisce la lista dei film che hanno tra i generi 'genre'.
        Il confronto del genere è NON case sensitive.
        
        @parametro@ genre: genere da cercare (case insensitive).
        @ritorna@ lista di dizionari (film che hanno il genere specificato).
        """
        genre_lower = genre.lower()
        return [
            movie for movie in self.movies
            if any(g.lower() == genre_lower for g in movie["genres"])
        ]

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 12. get_oldest_movie_title Restituisce il titolo del film più antico della collezione #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_oldest_movie_title(self) -> str:
        """
        Restituisce il titolo del film più antico della collezione.
        In caso di parità, restituisce il primo che compare nella lista.
        
        @ritorna@ riporta il titolo del film più vecchio.
        """
        if not self.movies:
            return None  # o gestisce in maniera differente se la lista è vuota
        oldest = min(self.movies, key=lambda m: m["year"])
        return oldest["title"]

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 13. get_average_release_year Restituisce la media aritmetica degli anni di uscita #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_average_release_year(self) -> float:
        """
        Restituisce la media aritmetica degli anni di uscita
        dei film della collezione.
        
        @ritorna@ riporta la float che rappresenta la media degli anni di uscita.
        """
        if not self.movies:
            return 0.0
        total_years = sum(movie["year"] for movie in self.movies)
        return total_years / len(self.movies)

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 14. get_longest_title Restituisce il titolo più lungo presente nella collezione #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_longest_title(self) -> str:
        """
        Restituisce il titolo più lungo presente nella collezione.
        In caso di parità, restituisce il primo che compare nella lista.
        
        @ritorna@ riporta titolo del film più lungo.
        """
        if not self.movies:
            return None
        longest = max(self.movies, key=lambda m: len(m["title"]))
        return longest["title"]

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 15. get_titles_between_years Restituisce la lista dei titoli dei film pubblicati #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_titles_between_years(self, start_year: int, end_year: int) -> list:
        """
        Restituisce la lista dei titoli dei film pubblicati
        tra start_year ed end_year (estremi inclusi).
        
        @parametro@ start_year: anno di inizio (incluso).
        @parametro@ end_year: anno di fine (incluso).
        @ritorna@ riporta lista di titoli di film pubblicati nell'intervallo specificato.
        """
        return [
            movie["title"] for movie in self.movies
            if start_year <= movie["year"] <= end_year
        ]

    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    # 16. get_most_common_year Restituisce l'anno più frequente nella collezione di film #
    # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° #
    def get_most_common_year(self) -> int:
        """
        Restituisce l'anno più frequente nella collezione di film.
        Non considera il caso di parità .
        
        @ritorna@ l'anno più comune .
        """
        if not self.movies:
            return None

        # Crea un dizionario con una frequenza dei film in un anno mappandole 
        frequency = {}
        for movie in self.movies:
            year = movie["year"]
            frequency[year] = frequency.get(year, 0) + 1
        
        # Trova l'anno con la frequenza piu alta
        most_common = max(frequency, key=frequency.get)
        return most_common

        # ================ #
        #       test       #
        # ================ #
if __name__ == "__main__":
    json_path = "C:\\Users\\Fehd\\Desktop\\Movie LiB\\movies.json"
    try:
        library = MovieLibrary(json_path)
    except FileNotFoundError as e:
        print(e)
    else:
        print("Film list:", library.get_movies())
        print("Film Title:", library.get_movie_titles())
        print("Film number:", library.countmovies())

        # Aggiunta di un film
        library.add_movie("Spaceballs", "Mel Brooks", 1987, ["science fiction"])

        # Rimozione di un film
        try:
            removed_film = library.remove_movie("New title")
            print("film removed:", removed_film)
        except MovieNotFoundError as e:
            print(e)

        # Aggiorna i dettagli di un film
        try:
            updated_film = library.update_movie(
                title="old Title",
                director="director Updated"
            )
            print("Film Updated:", updated_film)
        except MovieNotFoundError as e:
            print(e)

