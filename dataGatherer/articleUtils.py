import sys
import unirest

def analizeArticle( url ):
	response = unirest.get("https://joanfihu-article-analysis-v1.p.mashape.com/link?link="+url,
  		headers={
   			"X-Mashape-Key": "Us8edcjH55mshS0NlCRe3r03d5SCp1CGl55jsnPi9AcijPx8wE"
 		}
	)
	return response.body

def getsentiment( text ):
	response = unirest.post("https://text-sentiment.p.mashape.com/analyze",
  		headers={
    		"X-Mashape-Key": "Us8edcjH55mshS0NlCRe3r03d5SCp1CGl55jsnPi9AcijPx8wE",
    		"Content-Type": "application/x-www-form-urlencoded"
  		},
  		params={
    		"text": text
  		}
	)
	return response.body

def main():
    analizeArticle(sys.argv[1])

if __name__ == "__main__":
    main()