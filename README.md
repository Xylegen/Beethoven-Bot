# Beethoven-Bot
Music bot for discord which allows playing songs with keyword identification. Pause, resume, queue, stop and search features also included.

#Authorization
To authorize the bot on your server, use [this](https://discord.com/api/oauth2/authorize?client_id=889793325043945473&permissions=8&scope=bot) link. Grant permissions and the bot will be authorized on your server.

#Commands

!join - Request the bot to join your voice channel

!leave - Request the bot to leave your voice channel

!play song_name - Request the bot to play the song. If the command is used while a song is already playing, the requested song will be added to a queue, and the requests will be serviced after the current song finished playing. Max queue size is 20.

!pause - Request the bot to pause the current song

!resume - Request the bot to resume the paused song

!skip - Request the bot to skip the current song and move to the next one in the list

!search song_name- Request Top 5 search results from Youtube along with their urls (to be used in the play command)

!queue - Displays the current queue
