import customtkinter
import joblib
import string
import json
import os
import sys
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

HISTORY_FILENAME = 'email_history.json'


# Load the model and vectorizer
try:
    model = joblib.load('spam_classifier.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
except FileNotFoundError:
    print('Model or Vectorizer file not found. \n Maybe you haven\'t trained the model')
    sys.exit()

# Preprocessing function for the user's email's
def preprocess_text(text):

    stemmer = PorterStemmer()
    stopwords_set = set(stopwords.words('english'))

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation)).split()
    text = [stemmer.stem(word) for word in text if word not in stopwords_set]
    return ' '.join(text)



customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# General optimizations
app = customtkinter.CTk()
app.resizable(False,False)
app.title('Spam Email Classification')
app.geometry('650x400')


title_label = customtkinter.CTkLabel(app,
         text='Check if an email is spam or not',
         font=('Segoe UI',25)
)
title_label.pack(pady=10)

# A frame for the email Textbox and it's label
email_frame = customtkinter.CTkFrame(app,fg_color='transparent')
email_frame.pack(pady=30)

# "Enter an Email" label next to Textbox
enter_label = customtkinter.CTkLabel(email_frame,
            text='Enter an Email: ',
            text_color='#FFFFFF',
            font=('Segoe UI',13)
)
enter_label.pack(side='left', padx='10')

# Textbox for the user's email
email_entry = customtkinter.CTkTextbox(email_frame,
                   text_color='#FFFFFF',
                   height=100,
                   width=400,
                   wrap='word'
)
email_entry.pack(side='left')



# Whenever an email is classified, this function
# appends the email's content and result into a json file
def append_to_history(email,result):
   # The form which the data will be saved
   email_dict = {'email': email, 'result': result}

   # If the file exists or the json file isn't empty the file is loaded, else the list with the data will be created
   try:
       with open(HISTORY_FILENAME, 'r') as f:
           data = json.load(f)
   except (FileNotFoundError, json.JSONDecodeError):
       data = []

   data.append(email_dict)

   # Update or create json file if it doesn't exist
   with open(HISTORY_FILENAME, 'w') as f:
       json.dump(data,f, indent=2)





def clear_history(window):
    open(HISTORY_FILENAME, 'w').close()

    global open_history_window
    # Temporary fix
    open_history_window = False
    window.destroy()


# Used to prevent the user from opening second history window
open_history_window = False


# A pop up window for the display of the history of emails
def view_history():
    # Get access to the global variable
    global open_history_window

    # If it's already open the function will do nothing
    if open_history_window:
        return

    # Change the variable to true if it's not open
    open_history_window = True

    # General window optimizations
    history_window = customtkinter.CTkToplevel(app)
    history_window.title('Email History')
    history_window.geometry('550x400')
    history_window.resizable(False, False)

    def on_close():
        global open_history_window
        open_history_window = False
        history_window.destroy()

    history_window.protocol("WM_DELETE_WINDOW", on_close)

    # A scroll frame for the previous emails to be displayed
    scroll_frame = customtkinter.CTkScrollableFrame(history_window,
           width=400,
           height=200,
           label_text='Email History'
    )
    scroll_frame.pack(pady=25,padx=20)

    # If the file exists or the json file isn't empty the file is loaded, else the list with the data will be created
    try:
        with open(HISTORY_FILENAME, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # For every item in the data the email,result and email seperator labels are displayed inside the scroll frame
    for item in data:
        email_text = item.get('email').strip()
        result_text = item.get('result').strip()

        # The color of the result_text is changed based on the result
        if result_text == 'spam':
            result_text = 'This email is spam'
            result_color ='#FF1818'
        else:
            result_text = 'This email is normal'
            result_color = '#00FF00'

        # Result label displayed first for clarity, which contains the results(resultf because of outer scope variable)
        resultf_label = customtkinter.CTkLabel(scroll_frame,
                 text=f' {result_text}',
                 text_color=result_color,
                 anchor='w'
        )
        resultf_label.pack(anchor='w')

        # Email label which contains the content of the email
        email_label = customtkinter.CTkLabel(scroll_frame,
            text=email_text,
            anchor='w',
            justify='left',
            wraplength=390
        )
        email_label.pack(anchor='w')

        # Line seperator for clarity
        separator = customtkinter.CTkLabel(scroll_frame,
                    text='_________________________________________________________________________',
                    text_color='gray'
        )
        separator.pack(pady=5, anchor='w')

    # Clear history button that clears history lmao
    clear_history_button = customtkinter.CTkButton(history_window,
                    text='Clear History',
                    command=lambda: clear_history(history_window),
                    fg_color='#AA00C4',
                    hover_color='#E430FF',
                    corner_radius=15,
    )
    clear_history_button.pack(pady=20)





def classify_email():
    email = email_entry.get('0.0','end').strip()
    # If there is no text inside the Textbox a warning message is displayed
    if not email: # strip because there is apparently a \n  at the end
        result_label.configure(text='You have to enter an email', text_color='#FF1818')
    else:
        # Data preprocessing and vectorization
        clean_email = preprocess_text(email)
        vectorized_email = vectorizer.transform([clean_email])
        # Data prediction and results display
        prediction = model.predict(vectorized_email)
        # Based on the prediction the color of the text is changed
        if prediction[0] == 'spam':
            result_label.configure(text='This email is spam', text_color='#FF1818')
        else:
            result_label.configure(text='This email is normal', text_color='#00FF00')

        append_to_history(email, prediction[0])
        """In the next few lines, the state of the Textbox will be disabled and the color
          of the text inside the email_frame will be changed to something like gray,
          to give it a disabled-like look. Also the class_button text will 
          change to "Classify another Email". This happens because i want the user 
          to have a clear image of what he has to do in order to classify another email"""
        enter_label.configure(text_color='#656565')
        email_entry.configure(text_color='#656565', state='disabled')
        """The class button text is changed to 'Classify Another Email' and the assigned 
          command to the button is changed to the classify_another_email function.
          This happens so the entry,label and button functionality go back to normal"""
        class_button.configure(text='Classify Another Email', command=classify_another_email)

# All the previous changes go back to normal
def classify_another_email():
    enter_label.configure(text_color='#FFFFFF')
    email_entry.configure(text_color='#FFFFFF', state='normal')
    email_entry.delete("0.0", "end")
    class_button.configure(text='Classify Email', command=classify_email)
    result_label.configure(text='')

# Main button for functionality of this program
class_button = customtkinter.CTkButton(app,
                  text='Classify Email',
                  command=classify_email,
                  fg_color='#AA00C4',
                  hover_color='#E430FF',
                  corner_radius=15,
)
class_button.pack(pady=10)


history_button = customtkinter.CTkButton(app,
    text='View History',
    command=view_history,
    fg_color='#AA00C4',
    hover_color='#E430FF',
    corner_radius=15
)
history_button.pack(pady=2)
# Label that displays results or warnings to the user
result_label = customtkinter.CTkLabel(app, text='',font=('Segoe UI',15))
result_label.pack(pady=20)


app.mainloop()
