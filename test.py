"""
import flet as ft
import speech_recognition as sr
import threading
from langdetect import detect
import pyttsx3
import queue
import yfinance as yf

engine = pyttsx3.init()
recognizer = sr.Recognizer()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)
listening = True

message_queue = queue.Queue()

def main(page):
    RecognizedTextLabel = ft.Text("Recognized Text: N/A")
    DetectedLanguageLabel = ft.Text("Detected Language: N/A")

    def listen_for_speech():
        global listening
        while listening:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                #audio = recognizer.listen(source, timeout=10)
                try:
                    spoken_text = "bombay" #recognizer.recognize_google(audio)
                    detected_language = detect(spoken_text)
                    print(spoken_text)
                    print("Detected Language:", detected_language)

                    # Check if any of the specific keywords are present in the spoken text
                    keywords_to_detect = ["BSE", "NSE"]
                    for keyword in keywords_to_detect:
                        if keyword.lower() in spoken_text.lower():
                            message_queue.put(("update_ui", f"Keyword Detected: {keyword}", detected_language))
                            fetch_stock_closing_price(keyword)
                            break
                except sr.UnknownValueError:
                    print("Speech not recognized")
                except Exception as e:
                    print(f"An error occurred: {e}")

    def update_ui():
        while True:
            try:
                message_type, message_text, detected_language = message_queue.get(block=False)
                if message_type == "update_ui":
                    RecognizedTextLabel.value = f"Recognized Text: {message_text}"
                    DetectedLanguageLabel.value = f"Detected Language: {detected_language}"
                    page.update()
                    engine.say(f"Recognized Text: {message_text}")
                    engine.runAndWait()
            except queue.Empty:
                pass

    def fetch_stock_closing_price(keyword):
        try:
            # Use yfinance to fetch stock information based on the keyword
            stock_info = yf.Ticker(keyword)
            closing_price = stock_info.history(period="1d")["Close"][0]
            print(f"Closing Price of {keyword}: {closing_price:.2f}")
            # Display the closing price
            #message_queue.put(("update_ui", f"Closing Price of {keyword}: {closing_price:.2f}", ""))
        except Exception as e:
            print(f"Error fetching stock closing price: {e}")
            #message_queue.put(("update_ui", "Stock not found or data not available", ""))

    # Start the listening and UI update threads
    speech_thread = threading.Thread(target=listen_for_speech)
    speech_thread.daemon = True
    speech_thread.start()

    ui_thread = threading.Thread(target=update_ui)
    ui_thread.daemon = True
    ui_thread.start()

    page.add(RecognizedTextLabel, DetectedLanguageLabel)

    # Wait for user to exit the program
    input("Press Enter to stop listening...\n")
    listening = False  # Signal threads to stop

# Run the application
ft.app(target=main)
"""
import yfinance as yf
from yahooquery import search
from googletrans import Translator

def find_stock_symbol(company_name):
    try:
        # Use yahooquery to search for the company name and find the stock symbol
        result = search(company_name)
        if result:
            symbol = result['quotes'][0]['symbol']
            return symbol
        else:
            return None  # Company not found
    except Exception as e:
        return None  # Error finding stock symbol

def search_stock_price(company_name):
    try:
        symbol = find_stock_symbol(company_name)
        if symbol:
            stock = yf.Ticker(symbol)
            share_info = stock.history(period="1d")
            return symbol, share_info
        else:
            return None, f"Stock symbol not found for {company_name}."
    except Exception as e:
        return None, f"Error fetching share price: {e}"

def main():
    translator = Translator()
    
    while True:
        user_input = input("Enter a company name to search for its share price or 'exit' to quit: ")
        if user_input.lower() == "exit":
            break
        
        try:
            # Translate the user input to a target language (e.g., English)
            translation = translator.translate(user_input, src='auto', dest='en')
            
            # Check if the translation is successful
            if translation and translation.text:
                translated_input = translation.text
                symbol, share_info = search_stock_price(translated_input)
                if symbol:
                    print(f"Stock Symbol: {symbol}")
                if isinstance(share_info, str):
                    print(share_info)
                else:
                    print(f"Share Price for {translated_input}:")
                    print(share_info)
            else:
                print("Translation failed.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Welcome to the Stock Symbol Search Engine!")
    main()
