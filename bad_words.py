from nltk.tokenize import word_tokenize
import numpy as np
import speech_recognition as sr

# to load the list of bad words
data = np.loadtxt('./words.txt',dtype=str,delimiter="\n")
bad_words = []

for word in data:
	bad_words.append(word.lower())

check = 1

r  = sr.Recognizer()



#Uncomment the following code if you to choose which microphone you want to use

'''#enter your mike name here
mic_name = " "
#generate a list of all audio cards/microphones
mic_list = sr.Microphone.list_microphone_names()
 
#the following loop aims to set the device ID of the mic that we specifically want to use to avoid ambiguity.
for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name:
        device_id = i'''

mic = sr.Microphone()


while(check):
	with mic as source:
		r.adjust_for_ambient_noise(source) # takes a second to adjust to the background noise
		print("talk")
		audio = r.listen(source) # listens to the source

	try:
		speech = r.recognize_google(audio) # converts the suidio to speech
		final_sentence = ""
		words = word_tokenize(speech) # using word tokenizer in nltk to parse the sentence
		# if a bad word is found it changes it to sensered form
		for word in words:
			if word.lower() not in bad_words and word.lower() + "s" not in bad_words:
				final_sentence = final_sentence + word +" "
			else:
				word = word[0] + "*"*(len(word)-2) + word[len(word)-1]
				final_sentence = final_sentence + word + " "
		print("You spoke:")
		print(final_sentence)

		
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))

	print("\n Do you want to continue [y/n]?")
	choice = input()
	if choice == "y" or choice == "Y":
		check = 1
	else:
		check = 0
