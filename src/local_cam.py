def run_local_camera():
    # Load OpenCV's built-in face classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Cloud Optimization: Pass a high-quality video clip pathway instead of a physical camera index
    # For a local file, drop a sample transit .mp4 into your workspace and change this path to "sample_transit.mp4"
    video_source = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/face-demographics-walking-and-pause.mp4"
    
    print(f"🎥 Ingesting Live Simulation Video Stream from: {video_source}")
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print("❌ Error: Could not read video feed source asset.")
        return

    while True:
        ret, frame = cap.read()
        
        # Loop video automatically when it reaches the end for continuous demo display
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            
        # Downscale for optimal cloud CPU frame processing speeds
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for i, (x, y, w, h) in enumerate(faces):
            x, y, w, h = x * 2, y * 2, w * 2, h * 2
            
            mock_id = (i % 3) + 1
            name, profile = match_face_id(mock_id)
            update_last_seen(mock_id)
            
            # Draw tracking boundary graphics
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name}", (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, profile, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
        # Display the live window grid mapping matrix
        cv2.imshow('UrbanPulse AI - Live Edge Tracking Node', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()