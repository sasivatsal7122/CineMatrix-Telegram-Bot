import requests
import telebot
import os
import time
import urlshortner as urlsh


API_KEY = '5388409363:AAEMM6DE3XfilxJfzvpwZhsn5fAtGgEOfKg'
bot = telebot.TeleBot(API_KEY)


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


@bot.message_handler(commands=['Download_Movie'])
def  download_movie(message):
    dir = 'torrents/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
        
    def get_torrent(movies_json,movie_position=0):
        movie_title = movies_json['data']['movies'][movie_position]['title_long']
        bot.send_message(message.chat.id,"Getting Torrent Information about : \n\n"+movie_title)
        size_ls = [];quality_ls = [];torrent_link_ls = []
        movie_hash_ls = [];movie_type_ls = []
        
        torrents = movies_json['data']['movies'][movie_position]['torrents']
        
        for i in range(len(torrents)):
            size_ls.append(torrents[i]['size'])
            quality_ls.append(torrents[i]['quality'])
            torrent_link_ls.append(torrents[i]['url'])
            movie_hash_ls.append(torrents[i]['hash'])
            movie_type_ls.append(torrents[i]['type'])
        
        quality_string = ""        
        for i in range(len(size_ls)):
            quality_string+=(str(i+1)+". "+quality_ls[i]+' --> '+size_ls[i])+'\n\n'
        bot.send_message(message.chat.id,quality_string)
        
        def get_torrent_util_1(user_quality_choice):
            try:
                user_quality_choice = user_quality_choice.text
                user_quality_choicee = int(user_quality_choice)
                
                torrent_link_ls[user_quality_choicee-1]
                
                bot.send_message(message.chat.id,"Getting requested torrent....")
                time.sleep(0.2)
                bot.send_message(message.chat.id,"Obtaining Metadata...")                        
                time.sleep(0.2)
                bot.send_message(message.chat.id,"Calculating seeds and peers....")
                
                #torrent_link = urlsh.get_shorturl(torrent_link_ls[user_quality_choicee-1])
                #bot.send_message(message.chat.id,torrent_link)
                                
                bot.send_message(message.chat.id,"Here is Your Requested Torrent, Enjoy your movie night...")
                
                torrent_response = requests.get(torrent_link_ls[user_quality_choicee-1])
                open(f'torrents/{movie_title}.torrent', "wb").write(torrent_response.content)
                
                torrent_file = open(f'torrents/{movie_title}.torrent', 'rb')
                bot.send_document(message.from_user.id, torrent_file)
            
            except:
                bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from Start")
            
        user_quality_choice = bot.send_message(message.chat.id,"Enter Your Quality choice to download: ")
        bot.register_next_step_handler(user_quality_choice, get_torrent_util_1)
        
    
    def downmovie_util_2(user_movie_choice):
        user_movie_choicee = user_movie_choice.text
        user_movie_choicee = int(user_movie_choicee)
        try: 
            get_torrent(movies_json, user_movie_choicee-1)
        except:
            bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from Start")
            
    def downmovie_util(movie_name):

        movie_namee = movie_name.text
        movie_namee = movie_namee.title()
        intial_response = requests.get(f'https://yts.torrentbay.to/api/v2/list_movies.json?query_term={movie_namee}')
        global movies_json
        movies_json = intial_response.json()
        try:
            global movie_title_ls
            movie_title_ls,movie_id_ls = title_extraction(movies_json)
        
        
            def downmovie_util_3(confirmation):
                if confirmation.text == 'y' or confirmation.text == 'Y':
                    get_torrent(movies_json)
                else:
                    bot.send_message(message.chat.id,"Oops ! I couldn't find movie matching your query request, please try again from /Download_Movie with IMDb name")
                    
            if isinstance(movie_title_ls, list):
                    print_1 = """I found a couple of movies matching the movie you entered, select your choice"""
                    bot.send_message(message.chat.id, print_1)
                    for sno,movie in enumerate(movie_title_ls):
                            movie_name_string = ""
                            movie_name_string = str(sno+1)+". "+str(movie)
                            bot.send_message(message.chat.id,movie_name_string)
                    user_movie_choice = bot.send_message(message.chat.id,"Select the number of the movie : ")
                    bot.register_next_step_handler(user_movie_choice, downmovie_util_2)
            else:
                confirmation = bot.send_message(message.chat.id,"Did you mean "+movie_title_ls+" ? y or n")
                bot.register_next_step_handler(confirmation, downmovie_util_3)
        except:
            bot.send_message(message.chat.id,"Oops ! An error occured I couldn't find movie matching your query request, please try again from /Download_Movie with IMDb name")
               
    
    movie_name = bot.send_message(message.chat.id,"Enter Movie Name: ")
    bot.register_next_step_handler(movie_name, downmovie_util)



@bot.message_handler(commands=['Get_Movie_Details '])
def Get_Movie_Details():
    pass











      
  
@bot.message_handler(commands=['start'])
def welcome_message(message):
  greet_message = """
  Hey there! Welcome to CineMatrixxx Bot!

  Available Fucntions :

  /Download_Movie -- returns a torrent link 
  
  /Get_Movie_Details -- retrieves movie data
  
  /Get_Similar_Movie_Recommendation -- recommends similar movies
  
  /Get_Latest_Movie_Releases_By_Genre -- returns latest movies in specified genre
  
  /Get_Highest_Rated_Movie_Releases_By_Genre -- returns highest rated movies in specified genre
  
  """
  bot.send_message(message.chat.id, greet_message)


bot.polling()