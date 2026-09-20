import requests
import xml.etree.ElementTree as ET
class PaperService:
    BASE_URL="https://arxiv.org/api/query"
    def search_papers(self,query,max_results=5):
        params={
            "search_query":f"all:{query}",
            "start":0,
            "max_results":max_results
        }
        headers={"User-Agent":"AI-Research-Assistant/1.0"}
        response=requests.get(self.BASE_URL,params=params,headers=headers,timeout=60)
        if response.status_code==429:
            raise Exception("arXiv API rate limit reached. Please wait and try again Later.")
        if response.status_code!=200:
            print("Status Code:",response.status_code)
            print("Response:",response.text[:500])
            raise Exception("Failed to fetch papers.")
        root=ET.fromstring(response.text)
        namespace={
            "atom":"http://www.w3.org/2005/Atom"
        }
        entries=root.findall("atom:entry",namespace)
        papers=[]
        for entry in entries:
            pdf_url=None
            for link in entry.findall("atom:link",namespace):
                if link.get("title")=="pdf":
                    pdf_url=link.get("href")
                    break 

            paper={
                "title":entry.find("atom:title",namespace).text.strip(),
                "summary":entry.find("atom:summary",namespace).text.strip(),
                "published":entry.find("atom:published",namespace).text,
                "pdf_url":pdf_url
            }
            papers.append(paper)
        return papers