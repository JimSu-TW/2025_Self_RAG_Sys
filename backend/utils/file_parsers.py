from PyPDF2 import PdfReader
import docx
import markdown
import pandas as pd
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


def parse_uploaded_files(uploaded_files):
    documents = []
    logger.info(f"Starting to parse {len(uploaded_files)} files")

    for file in uploaded_files:
        file.seek(0)

        content_type = file.content_type
        logger.info(f"Processing file with content type: {content_type}")

        try:
            if content_type == "application/pdf":
                logger.info("Parsing PDF file")
                reader = PdfReader(file.file)
                text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
            elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                logger.info("Parsing DOCX file")
                doc = docx.Document(file.file)
                text = "\n".join([para.text for para in doc.paragraphs])
            elif content_type == "text/markdown":
                logger.info("Parsing Markdown file")
                text = markdown.markdown(file.file.read().decode("utf-8"))
            elif content_type == "text/csv":
                logger.info("Parsing CSV file")
                df = pd.read_csv(file.file)
                text = df.to_string(index=False)
            else:
                logger.info("Parsing as plain text")
                text = file.file.read().decode("utf-8")

            documents.append({"filename": file.filename, "content": text})
            logger.info("File successfully parsed")

        except Exception as e:
            logger.error(f"Error parsing file: {str(e)}")
            raise

    logger.info(f"Successfully parsed {len(documents)} documents")

    return documents
