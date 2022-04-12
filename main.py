import requests
import urlshortner as urlsh


def get_movie_details(movies_json, movie_position=0):
    # Movie name, movie synopsis, movie rating,run time,genres
    movie_details = ''
    movie_title = movies_json['data']['movies'][movie_position]['title_long']
    movie_rating = 'Movie rating : '+str(movies_json['data']['movies'][movie_position]['rating'])
    movie_runtime = 'Run Time: '+str(movies_json['data']['movies'][movie_position]['runtime'])+'mins'
    movie_genres = movies_json['data']['movies'][movie_position]['genres']
    movie_genres = " ".join(movie_genres)
    movie_genres = movie_genres.replace(" ",',')
    movie_genres = "Movie Genres : "+movie_genres
    movie_summary = movies_json['data']['movies'][movie_position]['summary']
    blah_tuple = (movie_title,movie_summary,movie_runtime,movie_rating,movie_genres)
    for item in blah_tuple:
        movie_details += item+'\n\n'
    return movie_details
    
    
''' DRIVER CODE TO GET THE TORREN INFORMATION'''
def get_torrent(movies_json,movie_position=0):
    movie_title = movies_json['data']['movies'][movie_position]['title_long']
    print("\nGetting Torrent Information about : "+movie_title)
    size_ls = [];quality_ls = [];torrent_link_ls = []
    movie_hash_ls = [];movie_type_ls = []
    
    torrents = movies_json['data']['movies'][movie_position]['torrents']
    
    for i in range(len(torrents)):
        size_ls.append(torrents[i]['size'])
        quality_ls.append(torrents[i]['quality'])
        torrent_link_ls.append(torrents[i]['url'])
        movie_hash_ls.append(torrents[i]['hash'])
        movie_type_ls.append(torrents[i]['type'])
    
    for i in range(len(size_ls)):
        print(i+1,quality_ls[i]+' --> '+size_ls[i])
    
    user_quality_choice = int(input("\nEnter Your Quality choice to download: "))
    print("\nWhat Would you like to download : ")
    user_torrent_type_choice  = int(input("\n1.Direct Torrent\n2.Magnet Link\n\nSelect your choice : "))
    if user_torrent_type_choice==1:
        print("\nGetting requested torrent....")
        torrent_link = urlsh.get_shorturl(torrent_link_ls[user_quality_choice-1])
        return torrent_link
    else:
        torrent_link = torrent_link_ls[user_quality_choice-1]
        magnet_url = f'magnet:?xt=urn:btih:{movie_hash_ls[user_quality_choice-1]}&dn={movie_title}+{quality_ls[user_quality_choice-1]}+{movie_type_ls[user_quality_choice-1]}+YTS.MX&tr=http://track.one:1234/announce&tr=udp://track.two:80&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://glotorrents.pw:6969/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://torrent.gresille.org:80/announce&tr=udp://p4p.arenabg.com:1337&tr=udp://tracker.leechers-paradise.org:6969'
        return magnet_url
    
    
''' DRIVER CODE TO GET THE NAMES OF MOVIE TITLES REQUESTED BY THE USER '''
def title_extraction(movies_json):
    
    if movies_json['data']['movie_count']!=1:
        movie_title_ls = [];movie_id_ls = []
        movie_title_json = movies_json['data']['movies']
        
        for i in range(len(movie_title_json)):
            movie_title_ls.append(movie_title_json[i]['title_long'])   
            movie_id_ls.append(movie_title_json[i]['id'])      
    else:
        return movies_json['data']['movies'][0]['title_long'],movies_json['data']['movies'][0]['id']
    
    return movie_title_ls,movie_id_ls
    

''' MAIN DRIVER CODE '''
def main(movie_name,user_option_of_app_use):
    
    intial_response = requests.get(f'https://yts.torrentbay.to/api/v2/list_movies.json?query_term={movie_name}')
    movies_json = intial_response.json()
    movie_title_ls,movie_id_ls = title_extraction(movies_json)
    
    if isinstance(movie_title_ls, list):
        print("I found a couple of movies matching the movie you entered, select your choice\n")
        for sno,movie in enumerate(movie_title_ls):
                print(sno+1,movie)
        user_movie_choice = int(input("\nEnter the number of the movie : "))
        if user_option_of_app_use == 1:
            torrent_link = get_torrent(movies_json, user_movie_choice-1)
            print(torrent_link)
        
        elif user_option_of_app_use == 2:
            movie_details = get_movie_details(movies_json, user_movie_choice-1)
            print(movie_details)
    
    else:
        print("Did you mean "+movie_title_ls+" ?")
        user_choice = str(input("\nEnter y for yes , n for no: "))
        if user_choice == 'y':
            if user_option_of_app_use==1:
                torrent_link = get_torrent(movies_json)
                print(torrent_link)
            elif user_option_of_app_use == 2:
                movie_details = get_movie_details(movies_json)
                print(movie_details)
        else:
            print("Try again form Start, enter the movie correctly")
                

if __name__=='__main__':
    #movie_name = str(input("Enter Movie Name: "))
    print("1.Download Movie\n2.Get Movie Details\n3.Get Similar Movie Recommendations\n4.Latest Releases\n5.Search Movies By Genre")
    user_option_of_app_use = int(input("\nEnter your choice: "))
    movie_name = 'Inception'
    main(movie_name,user_option_of_app_use)




        

