from .utils import SentimentAnalyzer
import sys

analyzer = SentimentAnalyzer()
trigger = analyzer.use_hf

def main():
	print(f"Demos:\n\n{demos()}")
	message()
	
	while True:
		try:
			text = input("\nEnter text to analyze:\n")
			if text:
				if trigger:
					output, sentiment = test_hf(text)
					print(f"\n\nRaw model output: {output}")
					print(f"\nHF sentiment: {sentiment}")
				else:
					print("\nHF failed to load")
			message()
		except KeyboardInterrupt:
			sys.exit("\nTerminated")

def test_hf(text):
	output = analyzer.hf_analyzer(text)[0]
	sentiment = analyzer.get_hf_sentiment_label(text)
	return output, sentiment

def demos():
	positive_text = "I am a good person"
	neutral_text = "I am a person"
	negative_text = "I am a bad person"
	if trigger:
		positive = f"Text 1: {positive_text}\nSentiment: {test_hf(positive_text)[1]}\n\n"
		neutral = f"Text 2: {neutral_text}\nSentiment: {test_hf(neutral_text)[1]}\n\n"
		negative = f"Text 3: {negative_text}\nSentiment: {test_hf(negative_text)[1]}"
		return positive + neutral + negative
	return "Sentiment demos unavailable because HF model failed to load"
	
def message():
	print("\n\nPress Ctrl + C to terminate\n")

if __name__ == "__main__":
	main()