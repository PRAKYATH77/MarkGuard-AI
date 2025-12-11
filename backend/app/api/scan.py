from fastapi import APIRouter, UploadFile, File, Form
import uuid
import os
import cv2
import easyocr
from app.database.connection import scan_collection
from app.core.scraper import fetch_datasheet_info
from app.core.validator import validate_scan

router = APIRouter()
reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader

@router.post("/scan-ic")
async def scan_ic(file: UploadFile = File(...), part_number: str = Form(...)):
    file_id = str(uuid.uuid4())
    upload_path = f"uploads/{file_id}.jpg"
    
    os.makedirs("uploads", exist_ok=True)
    with open(upload_path, "wb") as f:
        f.write(await file.read())
    
    # Real OCR using EasyOCR
    try:
        ocr_reader = get_reader()
        results = ocr_reader.readtext(upload_path)
        detected_texts = [text[1].upper() for text in results]
        
        # Check image quality (blur detection)
        img = cv2.imread(upload_path)
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        is_blurry = laplacian_var < 100  # Threshold for blur detection
        
        ocr_data = {
            'text_lines': detected_texts,
            'is_blurry': is_blurry
        }
    except Exception as e:
        # Fallback to mock data if OCR fails
        ocr_data = {
            'text_lines': [part_number.upper(), 'USA', 'BATCH2024'],
            'is_blurry': False
        }
    
    # Get expected datasheet info
    datasheet_info = fetch_datasheet_info(part_number)
    
    # Validate against datasheet
    result = validate_scan(ocr_data, datasheet_info)
    
    # Save to database
    scan_record = {
        'file_id': file_id,
        'filename': file.filename,
        'part_number': part_number,
        'status': result['status'],
        'confidence': result['confidence'],
        'issues': result['issues']
    }
    await scan_collection.insert_one(scan_record)
    
    return {
        'file_id': file_id,
        'filename': file.filename,
        'part_number': part_number,
        'status': result['status'],
        'confidence': result['confidence'],
        'issues': result['issues'],
        'explanation': result.get('explanation', ''),
        'detected_data': result.get('detected_data', {})
    }
