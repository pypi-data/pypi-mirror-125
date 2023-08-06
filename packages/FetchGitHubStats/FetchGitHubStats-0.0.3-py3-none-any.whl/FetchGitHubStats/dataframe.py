import requests
import pandas as pd
def ReturnDataFrame(url):
          response = requests.get(url)
          data = response.json()
          name = []
          urls = []
          stars = []
          forks = []
          description = []
          language = []
          for item in data:
            for key, value in item.items():
              if key == 'html_url':
                  urls.append(value)
              if key == 'name':
                  name.append(value)
              if key == 'stargazers_count':
                  stars.append(value)
              if key == 'forks':
                forks.append(value)
              if key == 'language':
                  language.append(value)
              if key == 'description':
                  description.append(value)

          df = pd.DataFrame(list(zip(name,description,language,stars,forks,urls)),columns =['Name Of Project', 'Description','Language','Stars','Forks','Link to Repo'])
          df = df.sort_values(by='Stars',ascending=False)
          return df
