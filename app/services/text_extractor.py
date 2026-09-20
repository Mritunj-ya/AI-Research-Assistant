import fitz
class TextExtractor:
    def extract_text(self,pdf_path):
        document=fitz.open(pdf_path)
        text=""
        for page_number in range(document.page_count):
            page=document.load_page(page_number)
            text=text+page.get_text()
        document.close()
        return text

