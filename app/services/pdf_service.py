import os
import requests
class PDFService:
    def download_pdf(self,pdf_url,filename):
        os.makedirs("data/papers",exist_ok=True)
        filepath=os.path.join("data","papers",filename)
        response=requests.get(pdf_url)
        if response.status_code==200:
            with open(filepath,"wb") as file:
                file.write(response.content)
            return filepath
        raise Exception("Failed to download PDF.")