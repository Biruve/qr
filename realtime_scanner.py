import cv2
import numpy as np
import time

def scan_qr_realtime():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = cv2.QRCodeDetector()

    if not cap.isOpened():
        print("❌ Webcam not accessible")
        return None

    print("\n📷 Camera ON")
    print("👉 Hold QR steady (20–30 cm)")
    print("👉 Increase phone brightness")
    print("👉 Works with GPay, PhonePe, Paytm, and UPI QR codes")
    print("👉 Press 'q' to exit\n")

    time.sleep(2)

    stable_data = None
    same_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 🔥 Slight sharpening improves dense QR detection
        kernel = np.array([[0,-1,0],
                           [-1,5,-1],
                           [0,-1,0]])
        sharpened = cv2.filter2D(frame, -1, kernel)

        # 🔥 Try upscaling for dense QR codes (GPay, PhonePe, etc.)
        resized = cv2.resize(sharpened, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

        # Try standard detection first
        data, bbox, _ = detector.detectAndDecode(resized)

        if not data:
            # Fallback multi-detection for complex QR codes
            retval, decoded_info, points, _ = detector.detectAndDecodeMulti(resized)
            if retval and decoded_info:
                data = decoded_info[0]
                bbox = points

        # 🔥 Additional attempt with grayscale for better contrast
        if not data:
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            data, bbox, _ = detector.detectAndDecode(gray)

        if data:
            if data == stable_data:
                same_count += 1
            else:
                stable_data = data
                same_count = 1

            if same_count >= 4:
                cap.release()
                cv2.destroyAllWindows()
                return stable_data

        else:
            stable_data = None
            same_count = 0

        cv2.imshow("Universal UPI QR Scanner", resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None