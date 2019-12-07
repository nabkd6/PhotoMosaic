
#Helper functions to parse the JSONs returned from FB API requests
def album_parser(data):
    """Takes facebook me/albums query results and returns IDs of each album
    to assist in building next query for photos in that album."""
    album_ids = []
    for item in data['data']:
        album_ids.append(item['id'])
    return album_ids

def image_parser(album_data):
    """Takes facebook album, iterates over pictures to select
    the photo with the max quality, and returns a list of
    file locations of all images in the album. Uses photo dimension height as
    proxy for quality"""
    image_sources = []
    for image in album_data['data']:
        max_val = 0
        image_source = None
        for item in image['images']:
            if item['height'] > max_val:
                max_val = item['height']
                image_source = item['source']
            else:
                continue
            image_sources.append(image_source)
    return image_sources
