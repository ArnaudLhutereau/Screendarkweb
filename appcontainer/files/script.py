from flask import Flask, request, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import requests
import os
import time
import re

# Flask app
app = Flask(__name__)
app.debug = True

# Proxy config (with tor container name and default port)
proxy = ("torcontainer", 9050)         

# Analyze route : source code will be analyzed to find : urls / emails / specific keywords
# INPUT :
# - Method : POST
# - Content-Type : JSON
# - Parameters : url (string) (mandatory), keywords (list) (optional)
# - Example : { "url"="https://google.com", "keywords"=["keyword1", "keyword2"] }
# OUTPUT :
# - Content-Type : JSON
# - Values : sourceResult (strings), urlResult (list), emailsResult (list), keywordsResult (dict (string : int))
# - Example : { sourceResult="<html>...</html>", urlResult=["http://one.com", "http://two.com"], emailsResult=["test@test.com"], keywordsResult={"keyword1"=1, "keyword2=56"} }
@app.route('/analyze', methods=['POST'])
def urlFunctionAnalyze():
    if request.method == 'POST':
        # POST method
        data = request.json
        if data["url"]:
            url = data["url"]
            # Check URL format
            try:
                if url[:4] != "http":
                    # Malformed URL (no http:// or https:// string). Try to add it
                    url = "http"+url
            except Exception as e:
                return("Error with URL parameter : "+str(e), 400)

            try:
                # Set parameters for webdriver
                options = Options()
                options.headless = True
                options.set_preference('intl.accept_languages', 'en-GB')
                options.set_preference('network.proxy.type', 1)
                options.set_preference('network.proxy.socks', proxy[0])
                options.set_preference('network.proxy.socks_port', proxy[1])
                options.set_preference('network.proxy.socks_remote_dns', True)

                # Request URL via Tor proxy
                driver = webdriver.Firefox(options=options)
                driver.get(url)
                source = driver.page_source

                # Find URLs in source
                aResults=driver.find_elements(By.TAG_NAME,"a")
                linksList = []
                for totals in aResults:
                    if totals.get_attribute('href') != None:
                        linksList.append(totals.get_attribute('href'))
                driver.close()

                # Find keywords in source
                keywordList  = {}
                try:
                    if data["keywords"]:
                        keywords = list(data["keywords"])
                        
                        for keyword in keywords:
                            pattern = r'('+keyword+')'
                            keywordList[keyword] = len(re.findall(pattern, source, re.IGNORECASE))
                        print(keywordList)
                except Exception as e:
                    print("Error during keywords detection process "+str(e))
                
                #Find emails in source
                emails = re.findall(r'([\w.-]+@[\w.-]+\.\w+)', source)
                
                # Return results
                return jsonify(sourceResult=source, urlResult=linksList, emailsResult=emails, keywordsResult=keywordList), 200
                
            except Exception as e:
                print(str(e))
                return("Error during execution : "+str(e), 400)
        else:
            return("Error, no data given", 400)
    else:
        return("Error, bad method", 400)


# Source route : Get website source code 
# INPUT :
# - Method : POST
# - Content-Type : JSON
# - Parameters : url (string) (mandatory)
# - Example : { "url"="https://google.com" }
# OUTPUT :
# - Content-Type : JSON
# - Values : sourceResult (strings)
# - Example : { sourceResult="<html>...</html>" }
@app.route('/source', methods=['POST'])
def urlFunctionSource():
    if request.method == 'POST':
        # POST method
        data = request.json
        if data["url"]:
            url = data["url"]
            # Check URL format
            try:
                if url[:4] != "http":
                    # Malformed URL (no http:// or https:// string). Try to add it
                    url = "http"+url
            except Exception as e:
                return("Error with URL parameter : "+str(e), 400)

            try:
                # Set parameters for webdriver
                options = Options()
                options.headless = True
                options.set_preference('intl.accept_languages', 'en-GB')
                options.set_preference('network.proxy.type', 1)
                options.set_preference('network.proxy.socks', proxy[0])
                options.set_preference('network.proxy.socks_port', proxy[1])
                options.set_preference('network.proxy.socks_remote_dns', True)

                # Request URL via Tor proxy
                driver = webdriver.Firefox(options=options)
                driver.get(url)
                resultRequest = driver.page_source
                driver.close()

                # Return result
                return jsonify(sourceResult=resultRequest), 200

            except Exception as e:
                print(str(e))
                return("Error during execution : "+str(e), 400)
        else:
            return("Error, no data given", 400)
    else:
        return("Error, bad method", 400)
    
# Screenshot route : Get website screenshot
# INPUT :
# - Method : POST
# - Content-Type : JSON
# - Parameters : url (string) (mandatory)
# - Example : { "url"="https://google.com" }
# OUTPUT :
# - Content-Type : image/png
# - Values : ?
# - Example : ?
@app.route('/screenshot', methods=['POST'])
def urlFunctionScreenshot():
    if request.method == 'POST':
        # POST method
        data = request.json
        if data["url"]:
            url = data["url"]
            # Check URL format
            try:
                if url[:4] != "http":
                    # Malformed URL (no http:// or https:// string). Try to add it
                    url = "http"+url
            except Exception as e:
                return("Error with URL parameter : "+str(e), 400)

            try:
                # Set parameters for webdriver
                options = Options()
                options.headless = True
                options.set_preference('intl.accept_languages', 'en-GB')
                options.set_preference('network.proxy.type', 1)
                options.set_preference('network.proxy.socks', proxy[0])
                options.set_preference('network.proxy.socks_port', proxy[1])
                options.set_preference('network.proxy.socks_remote_dns', True)

                # Request URL via Tor proxy
                print("DEBUG : Get URL page")
                driver = webdriver.Firefox(options=options)
                driver.get(url)
                resultRequest = driver.page_source
                
                # Save screenshot
                ts = int(time.time())
                driver.save_screenshot('/home/data/'+str(ts)+".png")
                driver.close()

                return send_file('/home/data/'+str(ts)+".png", mimetype="image/png"), 200


            except Exception as e:
                print(str(e))
                return("Error during execution : "+str(e), 400)

        else:
            return("Error, no data given", 400)
    else:
        return("Error, bad method", 400)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)