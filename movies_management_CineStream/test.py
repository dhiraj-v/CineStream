import json 

def get_cinestream_json(): 
    movies_dict = {}
    movies_file = open('movies_CineStream.json')
    movies_dict = json.load(movies_file)
    movies_file.close()
    return json.dumps(movies_dict)

print(get_cinestream_json())