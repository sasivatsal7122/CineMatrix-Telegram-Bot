import requests
import urlshortner as urlsh

''' DRIVER CODE TO GET THE TORREN INFORMATION'''
def get_torrent(movies_json,movie_position=0):
    print("\nGetting Torrent Information about : "+movies_json['data']['movies'][movie_position]['title_long'])
    size_ls = [];quality_ls = [];torrent_link_ls = []
    torrents = movies_json['data']['movies'][movie_position]['torrents']
    for i in range(len(torrents)):
        size_ls.append(torrents[i]['size'])
        quality_ls.append(torrents[i]['quality'])
        torrent_link_ls.append(torrents[i]['url'])
    for i in range(len(size_ls)):
        print(i+1,quality_ls[i]+' --> '+size_ls[i])
    user_quality_choice = int(input("\nEnter Your Quality choice to download: "))
    print("\nGetting requested torrent....")
    torrent_link = urlsh.get_shorturl(torrent_link_ls[user_quality_choice-1])
    return torrent_link


''' DRIVER CODE TO GET THE NAMES OF MOVIE TITLES REQUESTED BY THE USER '''
def title_extraction(movies_json):
    if movies_json['data']['movie_count']!=1:
        movie_title_ls = []
        movie_title_json = movies_json['data']['movies']
        for i in range(len(movie_title_json)):
            movie_title_ls.append(movie_title_json[i]['title_long'])         
    else:
        return movies_json['data']['movies'][0]['title_long']
    return movie_title_ls
    

''' MAIN DRIVER CODE '''
def main(movie_name):
    
    intial_response = requests.get(f'https://yts.torrentbay.to/api/v2/list_movies.json?query_term={movie_name}')
    movies_json = intial_response.json()
    movie_title_ls = title_extraction(movies_json)
    
    if isinstance(movie_title_ls, list):
        print("I found a couple of movies matching the movie you entered, select your choice\n")
        for sno,movie in enumerate(movie_title_ls):
                print(sno+1,movie)
        user_movie_choice = int(input("\nEnter the number of the movie : "))
        torrent_link = get_torrent(movies_json, user_movie_choice-1)
        print(torrent_link)
    
    else:
        print("Did you mean "+movie_title_ls+" ?")
        user_choice = str(input("\nEnter y for yes , n for no: "))
        if user_choice == 'y':
            torrent_link = get_torrent(movies_json)
            print(torrent_link)

if __name__=='__main__':
    #movie_name = str(input("Enter Movie Name: "))
    movie_name = 'Avengers'
    main(movie_name)




        

