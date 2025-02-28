# Translator: hieroglyps to text and text to hieroglyphs

hieroglyph_map = {
    # Lower case
    "a": "𓏏", "b": "𓈬", "c": "𓋏", "d": "𓍷", "e": "𓆣", 
    "f": "𓀃", "g": "𓆑", "h": "𓎉", "i": "𓌮", "j": "𓊫",
    "k": "𓋖", "l": "𓍖", "m": "𓋫", "n": "𓌩", "o": "𓊿",
    "p": "𓍶", "q": "𓋔", "r": "𓍄", "s": "𓉡", "t": "𓎛",
    "u": "𓍓", "v": "𓋝", "w": "𓀠", "x": "𓀋", "y": "𓍵",
    "z": "𓃷", 
    # Special characters
    "_": "𓃟", 
    "{": "𓂀", 
    "}": "𓅡",
    "'": "𓎬",
    ".": "𓊢",
    ",": "𓆯",
    " ": "𓋪",
    # Numbers
    "0": "𓅿", "1": "𓊘", "2": "𓂆", "3": "𓎿", "4": "𓁹",
    "5": "𓉓", "6": "𓎜", "7": "𓋮", "8": "𓃺", "9": "𓌷",
    # Upper case
    "A": "𓏬", "B": "𓐍", "C": "𓇌", "D": "𓃜", "E": "𓂶", 
    "F": "𓆟", "G": "𓐧", "H": "𓈉", "I": "𓏵", "J": "𓅒",
    "K": "𓅴", "L": "𓂻", "M": "𓆡", "N": "𓀊", "O": "𓆺",
    "P": "𓃦", "Q": "𓆄", "R": "𓄀", "S": "𓄁", "T": "𓇁",
    "U": "𓀟", "V": "𓃙", "W": "𓋸", "X": "𓍪", "Y": "𓉬",
    "Z": "𓌎"
}

# Plain text to hieroglyphs
def text_to_hieroglyphs(text):
    return "".join(hieroglyph_map.get(char, "?") for char in text)

# Hieroglyphs to plain text
def hieroglyphs_to_text(hieroglyphs):
    reverse_map = {v: k for k, v in hieroglyph_map.items()}
    return "".join(reverse_map.get(char, "?") for char in hieroglyphs)
