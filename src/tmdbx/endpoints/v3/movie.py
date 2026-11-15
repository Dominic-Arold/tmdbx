# GENERATED FILE — do not edit by hand.
# Re-generate with:
#   uv run python scripts/generate_v3_endpoints.py \
#       --spec   data/tmdb_v3_openapi_patched.json \
#       --models src/tmdbx/models/v3.py \
#       --out    src/tmdbx/endpoints/v3
from __future__ import annotations

from tmdbx.endpoints._def import EndpointDef, HTTPMethod, ParamDef, ParamKind

ENDPOINTS: list[EndpointDef] = [
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/changes',
        params         = [
            ParamDef(
                name        = 'end_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'start_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3MovieChangesGetResponse',
        description    = 'Get a list of all of the movie ids that have been changed in the past 24 hours.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/now_playing',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'ISO-3166-1 code',
            ),
        ],
        response_model = 'Field3MovieNowPlayingGetResponse',
        description    = 'Get a list of movies that are currently in theatres.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/popular',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'ISO-3166-1 code',
            ),
        ],
        response_model = 'Field3MoviePopularGetResponse',
        description    = 'Get a list of movies ordered by popularity.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/top_rated',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'ISO-3166-1 code',
            ),
        ],
        response_model = 'Field3MovieTopRatedGetResponse',
        description    = 'Get a list of movies ordered by rating.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/upcoming',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'ISO-3166-1 code',
            ),
        ],
        response_model = 'Field3MovieUpcomingGetResponse',
        description    = 'Get a list of movies that are being released soon.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'append_to_response',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'comma separated list of endpoints within this namespace, 20 items max',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
        ],
        response_model = 'Field3MovieMovieIdGetResponse',
        description    = 'Get the top level details of a movie by ID.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/account_states',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'guest_session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3MovieMovieIdAccountStatesGetResponse',
        description    = 'Get the rating, watchlist and favourite status of an account.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/alternative_titles',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'country',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'specify a ISO-3166-1 value to filter the results',
            ),
        ],
        response_model = 'Field3MovieMovieIdAlternativeTitlesGetResponse',
        description    = 'Get the alternative titles for a movie.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/changes',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'end_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'start_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3MovieMovieIdChangesGetResponse',
        description    = 'Get the recent changes for a movie.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/credits',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
        ],
        response_model = 'Field3MovieMovieIdCreditsGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/external_ids',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3MovieMovieIdExternalIdsGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/images',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'include_image_language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'specify a comma separated list of ISO-639-1 values to query, for example: `en-US,null`',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3MovieMovieIdImagesGetResponse',
        description    = 'Get the images that belong to a movie.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/keywords',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'str',
                required    = True,
            ),
        ],
        response_model = 'Field3MovieMovieIdKeywordsGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/latest',
        params         = [],
        response_model = 'Field3MovieLatestGetResponse',
        description    = 'Get the newest movie ID.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/lists',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
        ],
        response_model = 'Field3MovieMovieIdListsGetResponse',
        description    = 'Get the lists that a movie has been added to.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/recommendations',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
        ],
        response_model = 'Field3MovieMovieIdRecommendationsGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/release_dates',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3MovieMovieIdReleaseDatesGetResponse',
        description    = 'Get the release dates and certifications for a movie.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/reviews',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
        ],
        response_model = 'Field3MovieMovieIdReviewsGetResponse',
        description    = 'Get the user reviews for a movie.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/similar',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
        ],
        response_model = 'Field3MovieMovieIdSimilarGetResponse',
        description    = 'Get the similar movies based on genres and keywords.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/translations',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3MovieMovieIdTranslationsGetResponse',
        description    = 'Get the translations for a movie.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/videos',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
        ],
        response_model = 'Field3MovieMovieIdVideosGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/movie/{movie_id}/watch/providers',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3MovieMovieIdWatchProvidersGetResponse',
        description    = 'Get the list of streaming providers we have for a movie.',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/movie/{movie_id}/rating',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'guest_session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'Content-Type',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
                default     = 'application/json;charset=utf-8',
            ),
        ],
        response_model = 'Field3MovieMovieIdRatingPostResponse',
        request_model  = 'Field3MovieMovieIdRatingPostRequest',
        description    = 'Rate a movie and save it to your rated list.',
    ),
    EndpointDef(
        method         = HTTPMethod.DELETE,
        path_template  = '/3/movie/{movie_id}/rating',
        params         = [
            ParamDef(
                name        = 'movie_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'Content-Type',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'application/json;charset=utf-8',
            ),
            ParamDef(
                name        = 'guest_session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3MovieMovieIdRatingDeleteResponse',
        description    = 'Delete a user rating.',
    ),
]
