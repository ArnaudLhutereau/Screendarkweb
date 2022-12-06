# ScreenDarkweb



## Description

ScreenDarkweb is a tool which helps you to :
- **Scrap** onion link to get source code
- **Analyse** **source code** to get links, emails and detect keywords
- **Capture screensho**t website


## Architecture

![Architecture of screendarkweb with 2 containers in a dedicated server](https://raw.githubusercontent.com/ArnaudLhutereau/Screendarkweb/main/architecture.png)

ScreenDarkweb works in two app :
- **App container** : a Flask app runs like a proxy to transform and analyze your requests to/from Tor network. It uses Selenium for scrapping action *(Firefox webdriver)*.
- **Tor container** : a tor proxy

==> All requests (onion/classical links) will be sent throught Tor.
  

## Deployment

ScreenDarkweb is fully dockerized. You can deploy it in few seconds.
You just need [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/).

Clone ScreenDarkweb repository :
```
# git clone REPO
# cd REPO
```

Build it with docker-compose

```
# docker-compose build
```

Run it 
```
# docker-compose up
```


Don't forget to open ports in your firewall policy :
- User <==> App container : port 8080

Inside Docker, it uses default proxy port :
- App container <==> Tor container : port 9050


## Commands

Examples use a *"file.json"* for parameters requests *(via cURL)* :

```
{
    "url": "http://mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion",
    "keywords": ["keyword1","keyword2"]
}
```

3 routes are available :
- /screenshot 
	- Input (JSON) : 
		- "url" parameter *(str)*
- /source
	- Input (JSON) :
		- "url" parameter *(str)*
	- Output (JSON) :
		- "sourceResult" *(str)*
- /analyze
	- Input (JSON) :
		- "url" parameter *(str)*
		- "keywords" parameter *(str list)*
	- Output (JSON) :
		- "sourceResult" *(str)*
		- "urlResult" *(str list)*
		- "emailsResult" *(str list)*
		- "keywordsResult" *(dict (string : int))*



#### I want to screenshot a website
```
# curl -X POST http://127.0.0.1:8080/screenshot -H "Content-Type: application/json" -d @file.json > screenshot.png
```
  
#### I want source code

```
# curl -X POST http://127.0.0.1:8080/source -H "Content-Type: application/json" -d @file.json
```
  

#### I want to analyze website
```
# curl -X POST http://127.0.0.1:8080/analyze -H "Content-Type: application/json" -d @file.json
```
  


## Roadmap

- Customize Selenium & Tor configurations
- Telegram bot
- Mattermost bot
