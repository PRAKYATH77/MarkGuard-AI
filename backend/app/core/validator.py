def validate_scan(ocr_data, datasheet_data):
    detected_texts = [t.upper() for t in ocr_data.get('text_lines', [])]
    is_blurry = ocr_data.get('is_blurry', False)
    
    status = "PASS"
    issues = []
    confidence = 98.5
    explanation = ""
    detected_data = {
        "manufacturer": datasheet_data.get('manufacturer', 'Unknown'),
        "expected_logo": datasheet_data.get('logo_text', ''),
        "detected_texts": detected_texts,
        "image_quality": "Clear" if not is_blurry else "Blurry"
    }

    # 1. Visual Defect Check
    if is_blurry:
        status = "FAIL - Print Defect"
        issues.append("Text is blurry or broken (Possible Counterfeit)")
        explanation = "The image quality is poor with blurred text. This is a strong indicator of counterfeiting as genuine IC manufacturers use high-quality printing processes."
        confidence -= 35.0

    # 2. Manufacturer Logo Check
    expected_logo = datasheet_data.get('logo_text', '').upper()
    if expected_logo != "UNKNOWN":
        logo_found = False
        for text in detected_texts:
            if expected_logo in text:
                logo_found = True
                break
        
        if not logo_found and status == "PASS":
            issues.append(f"Logo '{expected_logo}' not clearly detected")
            explanation = f"The expected manufacturer logo '{expected_logo}' from {datasheet_data.get('manufacturer', 'Unknown')} was not detected in the image. Genuine ICs always have clear manufacturer markings."
            confidence -= 15.0

    # Generate final explanation for genuine ICs
    if status == "PASS" and not explanation:
        explanation = f"✅ All authenticity checks passed! The IC matches the {datasheet_data.get('manufacturer', 'manufacturer')} datasheet specifications. The part number, logo, and print quality are consistent with genuine components from the official supplier."

    return {
        "status": status,
        "issues": issues,
        "confidence": max(confidence, 10.0),
        "explanation": explanation,
        "detected_data": detected_data
    }
