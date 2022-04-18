import requests
import telebot
import os
import sys
import time

import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

try:
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
                  #time.sleep(0.2)
                  payload = {'api_key': '2402386ac7b63b99cd029e035bb5a7bd', 'url': torrent_link_ls[user_quality_choicee-1]}
                  torrent_response = requests.get('http://api.scraperapi.com', params=payload)
                  open(f'torrents/{movie_title}.torrent', "wb").write(torrent_response.content)
                  bot.send_message(message.chat.id,"Obtaining Metadata...")                        
                  time.sleep(0.2)
                  bot.send_message(message.chat.id,"Calculating seeds and peers....")
                
                  time.sleep(0.2)                
                  bot.send_message(message.chat.id,"Here is Your Requested Torrent, Enjoy your movie...")
                  
                  
                  torrent_file = open(f'torrents/{movie_title}.torrent', 'rb')
                  bot.send_document(message.from_user.id, torrent_file)
              
              except:
                  bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from /Download_Movie")
              
          user_quality_choice = bot.send_message(message.chat.id,"Enter Your Quality choice to download: ")
          bot.register_next_step_handler(user_quality_choice, get_torrent_util_1)
          
      
      def downmovie_util_2(user_movie_choice):
          user_movie_choicee = user_movie_choice.text
          user_movie_choicee = int(user_movie_choicee)
          try: 
              get_torrent(movies_json, user_movie_choicee-1)
          except:
              bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from /Download_Movie")
              
      def downmovie_util(movie_name):
          
          movie_namee = movie_name.text
          movie_namee = movie_namee.title()
          bot.send_message(message.chat.id,"Searching for the query....Please Be Patient we are low on server power...")
          payload = {'api_key': '2402386ac7b63b99cd029e035bb5a7bd', 'url': f'https://yts.torrentbay.to/api/v2/list_movies.json?query_term={movie_namee}'}
          intial_response = requests.get('http://api.scraperapi.com', params=payload)
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
  
  
  
  
  def get_movie_details(movies_json, movie_position=0,summary=True):
      # Returns Movie name, movie synopsis, movie rating,run time,genres
      movie_details = '\n'
      movie_title = movies_json['data']['movies'][movie_position]['title_long']
      movie_rating = 'Movie rating : '+str(movies_json['data']['movies'][movie_position]['rating'])
      movie_runtime = 'Run Time: '+str(movies_json['data']['movies'][movie_position]['runtime'])+'mins'
      movie_genres = movies_json['data']['movies'][movie_position]['genres']
      movie_genres = " ".join(movie_genres)
      movie_genres = movie_genres.replace(" ",',')
      movie_genres = "Movie Genres : "+movie_genres
      if summary:
          movie_summary = movies_json['data']['movies'][movie_position]['summary']
          blah_tuple = (movie_title,movie_summary,movie_runtime,movie_rating,movie_genres)
      else:
          blah_tuple = (movie_title,movie_runtime,movie_rating,movie_genres)
      for item in blah_tuple:
          movie_details += item+'\n\n'
      return movie_details
  
  
  
  @bot.message_handler(commands=['Get_Movie_Details'])
  def Get_Movie_Details(message):
      
      def gmd_util_3(confirmation):
          if confirmation.text == 'y' or confirmation.text == 'Y':
              movie_details = get_movie_details(movies_json)
              bot.send_message(message.chat.id,movie_details)
          else:
              bot.send_message(message.chat.id,"Oops ! I couldn't find movie matching your query request, please try again from /Get_Movie_Details with IMDb name")
      
  
      def gmd_util_2(user_movie_choice):
          user_movie_choicee = user_movie_choice.text
          user_movie_choicee = int(user_movie_choicee)
          try: 
              movie_details = get_movie_details(movies_json, user_movie_choicee-1)
              bot.send_message(message.chat.id,movie_details)
          except:
              bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from /Get_Movie_Details")
      
      
      
      def gmd_util_1(movie_name):
          
          movie_namee = movie_name.text
          movie_namee = movie_namee.title()
          bot.send_message(message.chat.id,"Searching for the query....Please Be Patient we are low on server power...")
          payload = {'api_key': '2402386ac7b63b99cd029e035bb5a7bd', 'url': f'https://yts.torrentbay.to/api/v2/list_movies.json?query_term={movie_namee}'}
          intial_response = requests.get('http://api.scraperapi.com', params=payload)
          global movies_json
          movies_json = intial_response.json()
          
          try:
              global movie_title_ls
              movie_title_ls,movie_id_ls = title_extraction(movies_json)
              
              
              if isinstance(movie_title_ls, list):
                  print_1 = """I found a couple of movies matching the movie you entered, select your choice"""
                  bot.send_message(message.chat.id, print_1)
                  for sno,movie in enumerate(movie_title_ls):
                          movie_name_string = ""
                          movie_name_string = str(sno+1)+". "+str(movie)
                          bot.send_message(message.chat.id,movie_name_string)
                  user_movie_choice = bot.send_message(message.chat.id,"Select the number of the movie : ")
                  bot.register_next_step_handler(user_movie_choice, gmd_util_2)
              
              else:
                  confirmation = bot.send_message(message.chat.id,"Did you mean "+movie_title_ls+" ? y or n")
                  bot.register_next_step_handler(confirmation, gmd_util_3)
          except:
              bot.send_message(message.chat.id,"Oops ! An error occured I couldn't find movie matching your query request, please try again from /Get_Movie_Details with IMDb name")
          
      movie_name = bot.send_message(message.chat.id,"Enter Movie Name: ")
      
      bot.register_next_step_handler(movie_name, gmd_util_1)
      
     
  
  
  @bot.message_handler(commands=['Get_Latest_Movie_Releases_By_Genre'])
  def Get_Latest_Movie_Releases_By_Genre(message):
      
      def glmrbg_util_2(user_genres_choicee):
          try:
              bot.send_message(message.chat.id,"Searching for the query....Please Be Patient we are low on server power...")
              genre = genres_tuple[user_genres_choicee-1]
              genre_movie_query = f'https://yts.torrentbay.to/api/v2/list_movies.json?minimum_rating=6&genre={genre}&sort_by=year&quality=1080p&limit=15'
              payload = {'api_key': '2402386ac7b63b99cd029e035bb5a7bd', 'url': genre_movie_query}
              latest_15_movies = requests.get('http://api.scraperapi.com', params=payload).json()
              
              latest_15_moviess = latest_15_movies['data']['movies']
              time.sleep(0.3)
              bot.send_message(message.chat.id,"Fetching Requested data...please be patient....")
              latest_movies_string = ''
              for i in range(len(latest_15_moviess)):
                  latest_movies_string += get_movie_details(latest_15_movies, movie_position=i,summary=False)+'\n=======================\n'
              bot.send_message(message.chat.id,latest_movies_string)
          except:
              bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from /Get_Latest_Movie_Releases_By_Genre")
      
      
      def glmrbg_util_1(user_genres_choice):
          user_genres_choicee = user_genres_choice.text
          user_genres_choicee = int(user_genres_choicee)
          glmrbg_util_2(user_genres_choicee)
          
      
      bot.send_message(message.chat.id,"Avaialble Genres:")
      genres_tuple = ('Action','Adventure','Animation','Biography','Comedy','Crime','Drame','Fantasy','History','Horror','Mystery','Romance','Sci-Fi','Thriller','War','Western')
      genre_string = ''
      for i,genre in enumerate(genres_tuple):
          genre_string+= (str(i+1)+'. '+genre)+'\n'
      bot.send_message(message.chat.id,genre_string)
      user_genres_choice = bot.send_message(message.chat.id,"Choose one: ")
      bot.register_next_step_handler(user_genres_choice, glmrbg_util_1)
      
  
  @bot.message_handler(commands=['Get_Highest_Rated_Movie_Releases_By_Genre'])
  def Get_Highest_Rated_Movie_Releases_By_Genre(message):
      
      def ghrmrbg_util_2(user_genres_choicee):
          try:
              bot.send_message(message.chat.id,"Searching for the query....Please Be Patient we are low on server power...")
              genre = genres_tuple[user_genres_choicee-1]
              genre_movie_query = f'https://yts.torrentbay.to/api/v2/list_movies.json?minimum_rating=6&genre={genre}&sort_by=rating&quality=1080p&limit=15'
              payload = {'api_key': '2402386ac7b63b99cd029e035bb5a7bd', 'url': genre_movie_query}
              latest_15_movies = requests.get('http://api.scraperapi.com', params=payload).json()
              latest_15_moviess = latest_15_movies['data']['movies']
              time.sleep(0.3)
              bot.send_message(message.chat.id,"Fetching Rerquested data...please be patient....")
              latest_movies_string = ''
              for i in range(len(latest_15_moviess)):
                  latest_movies_string += get_movie_details(latest_15_movies, movie_position=i,summary=False)+'\n======================\n'
              bot.send_message(message.chat.id,latest_movies_string)
          except:
              bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from /Get_Highest_Rated_Movie_Releases_By_Genre")
      
      
      def ghrmrbg_util_1(user_genres_choice):
          user_genres_choicee = user_genres_choice.text
          user_genres_choicee = int(user_genres_choicee)
          ghrmrbg_util_2(user_genres_choicee)
          
      
      bot.send_message(message.chat.id,"Avaialble Genres:")
      genres_tuple = ('Action','Adventure','Animation','Biography','Comedy','Crime','Drame','Fantasy','History','Horror','Mystery','Romance','Sci-Fi','Thriller','War','Western')
      genre_string = ''
      for i,genre in enumerate(genres_tuple):
          genre_string+= (str(i+1)+'. '+genre)+'\n'
      bot.send_message(message.chat.id,genre_string)
      user_genres_choice = bot.send_message(message.chat.id,"Choose one: ")
      bot.register_next_step_handler(user_genres_choice, ghrmrbg_util_1)
  
  @bot.message_handler(commands=['Get_Similar_Movie_Recommendation'])
  def Get_Similar_Movie_Recommendation(message):
      bot.send_message(message.chat.id,'My Boss is still working on this feature, it will be added soon')
  
  
  @bot.message_handler(commands=['start'])
  def welcome_message(message):
    greet_message = """
  Hey there! Welcome to CineMatrixxx Bot!
  
  Available Functtions :
  
  /Download_Movie -- returns a torrent link 
  
  /Get_Movie_Details -- retrieves movie data
  
  /Get_Similar_Movie_Recommendation -- recommends similar movies
  
  /Get_Latest_Movie_Releases_By_Genre -- returns latest movies in specified genre
  
  /Get_Highest_Rated_Movie_Releases_By_Genre -- returns highest rated movies in specified genre
    
    """
    bot.send_message(message.chat.id, greet_message)
  
  
  
  bot.polling(none_stop=True)
except Exception as ee:
    api_id = '9996836'
    api_hash = '373e9aa46c20e103167c5016d46a29a2'
    token = '5263589450:AAHwqvfkwmuhQZzoxaUsNM6SdTwETYcIgDc'
    #message = "donot reply"

    phone = '+1 917 397 5310'
    client = TelegramClient('session', api_id, api_hash)

    client.connect()
    client.is_user_authorized()

    if not client.is_user_authorized():
        client.send_code_request(phone)  
        client.sign_in(phone, input('Enter the code: '))
    try:
        message = "An error occured please restart the bot\n\n occured error: "+ str(ee)
        receiver = client.get_input_entity('https://t.me/Sasivatsal')
        client.send_message(receiver, message, parse_mode='html')
    except Exception as e:	
        print(e);

    client.disconnect()