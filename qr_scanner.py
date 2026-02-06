import cv2
import numpy as np
import os

def scan_qr(image_path):
    """
    Silently scan QR code from image file.
    Returns QR data string if successful, None if failed.
    """
    # Check if file exists
    if not os.path.exists(image_path):
        return None
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    detector = cv2.QRCodeDetector()
    
    # Method 1: Original image
    data, _, _ = detector.detectAndDecode(image)
    if data:
        return data
    
    # Method 2: Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data, _, _ = detector.detectAndDecode(gray)
    if data:
        return data
    
    # Method 3: Sharpened
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    data, _, _ = detector.detectAndDecode(sharpened)
    if data:
        return data
    
    # Method 4: Upscaled 2x
    resized = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    data, _, _ = detector.detectAndDecode(resized)
    if data:
        return data
    
    # Method 5: Upscaled 3x
    resized3 = cv2.resize(image, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
    data, _, _ = detector.detectAndDecode(resized3)
    if data:
        return data
    
    # Method 6: Binary threshold
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    data, _, _ = detector.detectAndDecode(binary)
    if data:
        return data
    
    # Method 7: OTSU threshold
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    data, _, _ = detector.detectAndDecode(otsu)
    if data:
        return data
    
    # Method 8: Adaptive threshold
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    data, _, _ = detector.detectAndDecode(adaptive)
    if data:
        return data
    
    # Method 9: Multi-detection on original
    retval, decoded_info, _, _ = detector.detectAndDecodeMulti(image)
    if retval and decoded_info and decoded_info[0]:
        return decoded_info[0]
    
    # Method 10: Multi-detection on upscaled
    retval, decoded_info, _, _ = detector.detectAndDecodeMulti(resized)
    if retval and decoded_info and decoded_info[0]:
        return decoded_info[0]
    
    # Method 11: Try with pyzbar (if installed)
    try:
        from pyzbar.pyzbar import decode
        decoded_objects = decode(image)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
    except:
        pass
    
    # All methods failed
    return None


# ============ USAGE EXAMPLES ============

# Example 1: Simple usage
result = scan_qr("qr_code.png")
if result:
    print(result)  # Only print if successful

# Example 2: With error handling
result = scan_qr("phonepe_qr.png")
if result:
    # Do something with the data
    print(f"Payment UPI: {result}")
else:
    # Handle failure silently or log it
    pass

# Example 3: Batch processing multiple QR codes
qr_files = ["qr1.png", "qr2.jpg", "qr3.png"]
for qr_file in qr_files:
    data = scan_qr(qr_file)
    if data:
        print(f"{qr_file}: {data}")