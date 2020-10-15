"""CSC108 A3 recommender starter code."""

from typing import TextIO, List, Dict

from recommender_constants import (MovieDict, Rating, UserRatingDict, 
                                   MovieUserDict)
from recommender_constants import (MOVIE_FILE_STR, RATING_FILE_STR,
                                   MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL,
                                   MOVIE_USER_DICT_SMALL)

############## HELPER FUNCTIONS

def get_similarity(user1: Rating, user2: Rating) -> float:
    """Return the a similarity score between user1 and user2 based on their
    movie ratings. The returned similarity score is a number between 0 and 1
    inclusive. The higher the number, the more similar user1 and user2 are.

    For those who are curious, this type of similarity measure is called the
    "cosine similarity".

    >>> r1 = {1: 4.5, 2: 3.0, 3: 1.0}
    >>> r2 = {2: 4.5, 3: 3.5, 4: 1.5, 5: 5.0}
    >>> s1 = get_similarity(r1, r1)
    >>> abs(s1 - 1.0) < 0.0001 # s1 is close to 1.0
    True
    >>> s2 = get_similarity(r1, {6: 4.5})
    >>> abs(s2 - 0.0) < 0.0001 # s2 is close to 0.0
    True
    >>> round(get_similarity(r1, r2), 2)
    0.16
    """
    shared = 0.0
    for m_id in user1:
        if m_id in user2:
            shared += user1[m_id] * user2[m_id]
    norm1 = 0.0
    for m_id in user1:
        norm1 = norm1 + user1[m_id] ** 2
    norm2 = 0.0
    for m_id in user2:
        norm2 = norm2 + user2[m_id] ** 2
    return (shared * shared) / (norm1 * norm2)


############## STUDENT CONSTANTS

# write constants here


############## STUDENT HELPER FUNCTIONS

# write helper functions here

def comma_finder(line: str) -> Dict[int, int]:
    r"""Return the indexs of every commas in the line.
    >>> comma_finder('68735,Warcraft,2016-05-25,123.0,Action,Adventure,Fantasy\n')
    {1: 5, 2: 14, 3: 25, 4: 31, 5: 38, 6: 48}
    >>> comma_finder('302156,Criminal,2016-04-14,113.0,Action\n')
    {1: 6, 2: 15, 3: 26, 4: 32}
    """
    index_dic = {}
    j = 1
    i = 0
    while i < len(line):
        if line[i] == ',':
            index_dic[j] = i
            j = j + 1
        i = i + 1
    return index_dic

def get_movie_genres(line: str) -> List[str]:
    r"""Retuen the list of movie genres
    
    >>> get_movie_genres('68735,Warcraft,2016-05-25,123.0,Action,Adventure,Fantasy\n')
    ['Action', 'Adventure', 'Fantasy']
    >>> get_movie_genres('302156,Criminal,2016-04-14,113.0,Action\n')
    ['Action']
    >>> get_movie_genres('302156,Criminal,2016-04-14,113.0')
    []
    """
    movie_gen = []
    commas = comma_finder(line)
    i = 4 ## genres start at forth comma
    last_comma = len(commas)
    while i < last_comma:
        movie_gen.append(line[commas[i] + 1: commas[i + 1]])
        i = i + 1
    if i == last_comma:
        movie_gen.append(line[commas[i] + 1:].strip())
    return movie_gen
    
def sort_score_list(movie_score: Dict[int, float]) -> List[int]:
    """Return the sorted list of movie. Movies with higher scores appear before
    those with lower scores. If two movies have the same score, the movie with
    the smaller id appear first.
    
    This is the forth step of recommend_movies
    
    >>> sort_score_list({10:3.0,11:3.5,12:4.5,13:3.0,14:4.0,15:3.5})
    [12, 14, 11, 15, 10, 13]
    >>> sort_score_list({23423:7.64,12342:5.456,32123:7.64,1234:3.44,75634:6.77,12342:3.44})
    [23423, 32123, 75634, 1234, 12342]
    """
    sorted_list = []
    score_list = []
    score_movie = {}
    for mov in movie_score:
        score_list.append(movie_score[mov])
    score_list.sort()
    score_list.reverse()
    
    for sco in score_list:
        score_movie[sco] = []
        for mov in movie_score:
            if movie_score[mov] == sco:
                score_movie[sco].append(mov)
    for sco in score_movie:
        score_movie[sco].sort()
        for mov in score_movie[sco]:
            sorted_list.append(mov)
    return sorted_list   
                    
def get_mov_score(movie_id: int,                                  
                  user_ratings: UserRatingDict,
                  similar_user: Dict[int, float],
                  candidate_mov: List[int]) -> int:
    """Return the score of moive
    
    This is the third step of recommend_movies
    
    I have no idea how to creat examples for this one. It is just more clear for 
    me to work on this part as a helper function. 
    >>> 
    """
    score = 0
    movie_pouplarity = 0
    for p in user_ratings:
        if movie_id in user_ratings[p]:
            movie_pouplarity = movie_pouplarity + 1
    
    for p in similar_user:
        contribution = 0
        num_user_movie = 0
        if movie_id in user_ratings[p] and user_ratings[p][movie_id] >= 3.5:
            similarity = similar_user[p]
            for mov in candidate_mov:
                if mov in user_ratings[p] and user_ratings[p][mov] >= 3.5:
                    num_user_movie = num_user_movie + 1
            if num_user_movie * movie_pouplarity != 0:
                contribution = similarity / (num_user_movie * movie_pouplarity)
        score = score + contribution
    return score
    
    
def get_candidate_mov(similar_user: Dict[int, float],
                      user_ratings: UserRatingDict,
                      target_rating: Rating,) -> List[int]:
    """Return the list of movies that these similar users have rated 3.5 or 
    above. This will be list of candidate movies
    
    This is the second step of recommend_movies
    
    >>> get_candidate_mov({2: 0.8617021276595744}, USER_RATING_DICT_SMALL, {68735: 3.5, 302156: 4.0})
    [293660]
    """    
    candidate_mov = []
    for p in similar_user:
        for mov in user_ratings[p]:
            if (mov not in candidate_mov) and (mov not in target_rating):
                if user_ratings[p][mov] >= 3.5:
                    candidate_mov.append(mov)
    return candidate_mov

                
############## STUDENT FUNCTIONS

def read_movies(movie_file: TextIO) -> MovieDict:
    """Return a dictionary containing movie id to (movie name, movie genres)
    in the movie_file.

    >>> movfile = open('movies_tiny.csv')
    >>> movies = read_movies(movfile)
    >>> movfile.close()
    >>> 68735 in movies
    True
    >>> movies[124057]
    ('Kids of the Round Table', [])
    >>> len(movies)
    4
    >>> movies == MOVIE_DICT_SMALL
    True
    """

    # Your code here     
    
    movie_dict = {}
    data_line = movie_file.readline()
    data_line = movie_file.readline()
    while data_line != '':
        commas = comma_finder(data_line)
        movie_id = int(data_line[:commas[1]])
        movie_name = data_line[commas[1] + 1: commas[2]]
        movie_gen = get_movie_genres(data_line)
        movie_dict[movie_id] = (movie_name, movie_gen)
        data_line = movie_file.readline()
    return movie_dict


def read_ratings(rating_file: TextIO) -> UserRatingDict:
    """Return a dictionary containing user id to {movie id: ratings} for the
    collection of user movie ratings in rating_file.

    >>> rating_file = open('ratings_tiny.csv')
    >>> ratings = read_ratings(rating_file)
    >>> rating_file.close()
    >>> len(ratings)
    2
    >>> ratings[1]
    {2968: 1.0, 3671: 3.0}
    >>> ratings[2]
    {10: 4.0, 17: 5.0}
    """

    # Your code here
    rating_dict = {}
    data_line = rating_file.readline()
    data_line = rating_file.readline()
    while data_line != '':
        commas = comma_finder(data_line)
        user_id = int(data_line[:commas[1]])
        movie_id = int(data_line[commas[1] + 1: commas[2]])
        rating = float(data_line[commas[2] + 1: commas[3]])
        if user_id not in rating_dict:
            movie_rating = {}
            movie_rating[movie_id] = rating
            rating_dict[user_id] = movie_rating
        elif user_id in rating_dict:
            rating_dict[user_id][movie_id] = rating
        data_line = rating_file.readline()
    return rating_dict   


def remove_unknown_movies(user_ratings: UserRatingDict, 
                          movies: MovieDict) -> None:
    """Modify the user_ratings dictionary so that only movie ids that are in the
    movies dictionary is remaining. Remove any users in user_ratings that have
    no movies rated.

    >>> small_ratings = {1001: {68735: 5.0, 302156: 3.5, 10: 4.5}, 1002: {11: 3.0}}
    >>> remove_unknown_movies(small_ratings, MOVIE_DICT_SMALL)
    >>> len(small_ratings)
    1
    >>> small_ratings[1001]
    {68735: 5.0, 302156: 3.5}
    >>> 1002 in small_ratings
    False
    """

    # Your code here
    mov_to_remove = []
    people_to_remove = []
    for p in user_ratings:
        for mov in user_ratings[p]:
            if mov not in movies:
                mov_to_remove.append(mov)
    for mov in mov_to_remove:
        for p in user_ratings:
            if mov in user_ratings[p]:
                user_ratings[p].pop(mov)
            if user_ratings[p] == {} and (p not in people_to_remove):
                people_to_remove.append(p)
    for p in people_to_remove:
        user_ratings.pop(p)


def movies_to_users(user_ratings: UserRatingDict) -> MovieUserDict:
    """Return a dictionary of movie ids to list of users who rated the movie,
    using information from the user_ratings dictionary of users to movie
    ratings dictionaries.

    >>> result = movies_to_users(USER_RATING_DICT_SMALL)
    >>> result == MOVIE_USER_DICT_SMALL
    True
    """

    # Your code here
    mov_list = []
    mov_to_p = {}
    for p in user_ratings:
        for mov in user_ratings[p]:
            if mov not in mov_list:
                mov_list.append(mov)
    for mov in mov_list:
        mov_to_p[mov] = []
        for p in user_ratings:
            if mov in user_ratings[p]:
                mov_to_p[mov].append(p)
        mov_to_p[mov].sort()
    return mov_to_p

def get_users_who_watched(movie_ids: List[int],
                          movie_users: MovieUserDict) -> List[int]:
    """Return the list of user ids in moive_users who watched at least one
    movie in moive_ids.

    >>> get_users_who_watched([293660], MOVIE_USER_DICT_SMALL)
    [2]
    >>> lst = get_users_who_watched([68735, 302156], MOVIE_USER_DICT_SMALL)
    >>> len(lst)
    2
    """

    # Your code here
    p_watched = []
    for mov in movie_ids:
        if mov in movie_users:
            for p in movie_users[mov]:
                if p not in p_watched:
                    p_watched.append(p)
    return p_watched

def get_similar_users(target_rating: Rating,
                      user_ratings: UserRatingDict,
                      movie_users: MovieUserDict) -> Dict[int, float]:
    """Return a dictionary of similar user ids to similarity scores between the
    similar user's movie rating in user_ratings dictionary and the
    target_rating. Only return similarites for similar users who has at least
    one rating in movie_users dictionary that appears in target_Ratings.

    >>> sim = get_similar_users({293660: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL)
    >>> len(sim)
    1
    >>> round(sim[2], 2)
    0.86
    """

    # Your code here
    mov_list = []
    similar_p = {}
    for mov in target_rating:
        mov_list.append(mov)
    remove_unknown_movies(user_ratings, movie_users)
    p_watched = get_users_who_watched(mov_list, movie_users)
    for p in p_watched:
        if p in user_ratings:
            similarity = get_similarity(target_rating, user_ratings[p])
            similar_p[p] = similarity
    return similar_p
    


def recommend_movies(target_rating: Rating,
                     movies: MovieDict, 
                     user_ratings: UserRatingDict,
                     movie_users: MovieUserDict,
                     num_movies: int) -> List[int]:
    """Return a list of num_movies movie id recommendations for a target user 
    with target_rating of previous movies. The recommendations come from movies
    dictionary, and are based on movies that "similar users" data in
    user_ratings / movie_users dictionaries.

    >>> recommend_movies({302156: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [68735]
    >>> recommend_movies({68735: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [302156, 293660]
    """

    # Your code here
    
    movie_score = {}
    
    ## First step = 'we will need to find users similar'
    similar_user = get_similar_users(target_rating, user_ratings, movie_users) 
    
    ## Second step = 'This will be our list of candidate movies'
    ## get_candidate_mov created
    candidate_mov = get_candidate_mov(similar_user, user_ratings, target_rating)
    
    ## Third step = 'track a "score" for each movie'
    ## get_mov_score created
    for mov in candidate_mov:
        movie_score[mov] = get_mov_score(mov, 
                                         user_ratings,                                          
                                         similar_user, 
                                         candidate_mov)    
        
    ## Forth step = 'The return list should contain movie ids with the highest scores'
    ## sort_score_list created
    sorted_list = sort_score_list(movie_score)
    
    ## Last step = ' list should be no longer than the value of this parameter'
    final_list = sorted_list[:num_movies]
    
    return final_list
    


if __name__ == '__main__':
    """Uncomment to run doctest"""
    import doctest
    doctest.testmod()
    
