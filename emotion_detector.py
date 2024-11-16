import cv2
from deepface import DeepFace

# Funcție pentru alegerea unui quote pe baza emoției
def get_quote(emotion):
    quotes = {
        "happy": "Keep smiling, life is beautiful! 😊",
        "sad": "Every day may not be good, but there's something good in every day. 🌟",
        "angry": "Take a deep breath. Let it go. 💪",
        "surprise": "Life is full of surprises! 🎉",
        "fear": "Courage is not the absence of fear. 🌈",
        "neutral": "Stay calm and carry on. ✨",
        "unknown": "Embrace your emotions—they make you human! 💖"
    }
    return quotes.get(emotion, "You are amazing!")

# Funcția principală
def main():
    # Pornește camera
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Emotion Detector")
    print("Press 's' to scan your emotion and 'q' to quit.")

    while True:
        # Capturează frame-ul
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Afișează frame-ul în fereastră
        cv2.imshow("Emotion Detector", frame)

        # Așteaptă input de la utilizator
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):  # Detectează emoția când se apasă 's'
            cv2.imwrite("capture.jpg", frame)
            print("Image captured. Analyzing emotion...")
            try:
                # Analizează emoția cu DeepFace
                analysis = DeepFace.analyze(img_path="capture.jpg", actions=['emotion'], enforce_detection=False)
                print(f"Analysis result: {analysis}")  # Debugging: Afișează datele brute returnate

                # Accesează primul element din lista returnată
                if isinstance(analysis, list):
                    analysis = analysis[0]

                # Verificăm dacă există cheia 'dominant_emotion'
                if 'dominant_emotion' in analysis:
                    dominant_emotion = analysis['dominant_emotion']
                    print(f"Detected Emotion: {dominant_emotion}")

                    # Obține quote-ul pentru emoția detectată
                    quote = get_quote(dominant_emotion)

                    # Adaugă emoția și quote-ul pe imagine
                    cv2.putText(frame, f"Emotion: {dominant_emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(frame, quote, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

                else:
                    print("Error: 'dominant_emotion' key not found in analysis result.")
                    cv2.putText(frame, "Error detecting emotion", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Afișează imaginea actualizată
                cv2.imshow("Emotion Detector", frame)
                cv2.waitKey(3000)  # Afișează rezultatul timp de 3 secunde

            except Exception as e:
                print(f"Error detecting emotion: {e}")
                cv2.putText(frame, "Error detecting emotion", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.imshow("Emotion Detector", frame)
                cv2.waitKey(3000)

        elif key == ord('q'):  # Închide aplicația când se apasă 'q'
            print("Exiting...")
            break

    # Eliberează resursele
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
