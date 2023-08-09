message = 'Whiskey Hotel Four Tango Dash Alpha Romeo Three Dash Yankee Oscar Uniform Dash Sierra One November Kilo India November Golf Dash Four Bravo Zero Uniform Seven'

word_to_digit = {
    'Zero': '0',
    'One': '1',
    'Two': '2',
    'Three': '3',
    'Four': '4',
    'Five': '5',
    'Six': '6',
    'Seven': '7',
    'Eight': '8',
    'Nine': '9',
    'Dash':'-'
}

def split (text):
    return text.split()

def decode (message):
    answer=''
    words  = split(message)
    for word in words :
        
        answer += word_to_digit.get(word,word[0])
        
    return answer



print (decode(message))