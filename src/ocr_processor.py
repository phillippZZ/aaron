import json
import os
import pdf2image
import pytesseract
import re
from logging_config import setup_logging

logger = setup_logging()

class OCRProcessor:
    def __init__(self):
        pass

    @staticmethod
    def clean_text(text):
        # Remove special characters but keep spaces and alphanumeric characters
        return re.sub(r'[^a-zA-Z0-9\s\.]', '', text)

    @staticmethod
    def parse_line(line):
        try:
            # Clean the line before splitting
            cleaned_line = OCRProcessor.clean_text(line)
            parts = cleaned_line.strip().split()
            
            # Ensure we have all required fields (9 columns)
            if len(parts) >= 9:
                try:
                    # Extract numbers and convert with proper error handling
                    cones = int(float(parts[-4]))     # # OF CONES
                    gross = float(parts[-3])          # GROSS WEIGHT
                    tare = int(float(parts[-2]))      # TARE WEIGHT
                    net = float(parts[-1])            # NET WEIGHT LBS
                except ValueError as e:
                    logger.error(f"Number conversion error in line: {line} - {str(e)}")
                    return None

                result = {
                    "case_number": parts[0],          # CASE #
                    "lot_number": parts[1],           # LOT #
                    "yarn_id": parts[2],              # YARN L D
                    "description": " ".join(parts[3:len(parts)-5]),  # DESCRIPTION (variable length)
                    "color": parts[-5],               # COLOR
                    "cones": cones,                   # # OF CONES
                    "gross_weight": gross,            # GROSS WEIGHT
                    "tare_weight": tare,              # TARE WEIGHT
                    "net_weight": net                 # NET WEIGHT LBS
                }
                logger.info(f"Parsed line: {result}")
                return result
        except (ValueError, IndexError) as e:
            logger.info(f"Skipping invalid line: {line}")  # Changed to info since some lines might be headers
            return None
        return None

    def process_pdf(self, pdf_path):
        try:
            logger.info(f"Processing PDF: {pdf_path}")
            
            images = pdf2image.convert_from_path(
                pdf_path,
                dpi=300,
                fmt='jpeg'
            )
            
            parsed_data = []
            for i, image in enumerate(images):
                logger.info(f"Processing page {i+1}")
                page_text = pytesseract.image_to_string(image)
                
                logger.info(f"Page text: {page_text}")
                for line in page_text.split('\n'):
                    if line.strip():
                        parsed_line = OCRProcessor.parse_line(line)
                        if parsed_line:
                            parsed_data.append(parsed_line)
            
            result = {
                "status": "success",
                "data": parsed_data
            }

            return result
        except Exception as e:
            error_msg = f"Error processing PDF: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            return {
                "status": "error",
                "message": error_msg
            }

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        logger.error("Usage: python ocr_processor.py <pdf_file_path> <output_json_path>")
        sys.exit(1)
    
    processor = OCRProcessor()
    processor.process_pdf(sys.argv[1], sys.argv[2])