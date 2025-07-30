from shared import SP, similarity, extract_spotify_track_id

async def search_tracks(query: str, limit: int = 20) -> list[dict[str, str]]:
    track_res = SP.search(q=query, type='track', limit=50)
    items = track_res.get('tracks', {}).get('items', []) if track_res else []

    sorted_items = sorted(
        items,
        key=lambda track: similarity(query, f"{track['artists'][0]['name']} {track['name']}"),
        reverse=True
    )

    top_items = sorted_items[:limit]

    return [
        {
            'title': track['name'],
            'artist': track['artists'][0]['name'],
            'cover': track['album']['images'][0]['url'],
            'duration': track['duration_ms'] // 1000
        }
        for track in top_items
    ]

async def search_spotify_url(url: str) -> dict[str, str] | None:
    try:
        track = SP.track(extract_spotify_track_id(url))
    except Exception as e:
        print(f"Ошибка при запросе трека: {e}")
        return None
    if track:
        return {
            'title': track['name'],
            'artist': track['artists'][0]['name'],
            'cover': track['album']['images'][0]['url'],
            'duration': track['duration_ms'] // 1000
        }
    return None