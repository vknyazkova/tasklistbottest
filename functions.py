

def markdownv2_ecran(text):
    allcharacters = ['_', '*', '[', ']', '(', ')', '`', '>',
                     '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for i in allcharacters:
        text = text.replace(i, f'\\{i}')
    return text
