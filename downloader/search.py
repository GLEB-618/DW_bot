from shared import SP, similarity

def search_tracks(query: str, limit: int = 20) -> list[dict[str, str]]:
    track_res = SP.search(q=query, type='track', limit=50)
    items = track_res.get('tracks', {}).get('items', []) if track_res else []

    # 3. Сортировка по похожести
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
            'duration': track['duration_ms'] // 1000,
            'url': track['external_urls']['spotify']
        }
        for track in top_items
    ]