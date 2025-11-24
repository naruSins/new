# my simple calculaotr on github

import tkinter 
import re
import math
import tkinter.font as tkfont

#A+B, A-B, A*B, A/B
#A = "0"
#operator = None
#B = None

# show full
expr = ""
trig_degrees = False  # False = radians, True = degrees

def clear_all():
    global expr
    expr = ""

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def evaluate_expression(s):
    """
    Safe-ish evaluator:
    - maps display chars to python equivalents
    - allows a limited set of math functions/constants via 'allowed' mapping
    - uses eval with restricted globals
    """
    global trig_degrees

    # map display operators / symbols to python
    s = s.replace("×", "*").replace("÷", "/").replace("^", "**").replace("π", "pi")
    # remove accidental double spaces
    s = s.strip()

    # allow only safe characters (digits, operators, letters, parentheses, dot)
    if not re.match(r'^[0-9\.\+\-\*\/\(\)\s,a-zA-Z\^π]+$', s):
        raise ValueError("Invalid characters in expression")

    # wrappers for trig that respect DEG/RAD mode
    def _wrap_forward(func):
        if trig_degrees:
            return lambda x: func(math.radians(x))
        return func

    def _wrap_inverse(func):
        if trig_degrees:
            return lambda x: math.degrees(func(x))
        return func

    allowed = {
        # trig
        "sin": _wrap_forward(math.sin),
        "cos": _wrap_forward(math.cos),
        "tan": _wrap_forward(math.tan),
        "asin": _wrap_inverse(math.asin),
        "acos": _wrap_inverse(math.acos),
        "atan": _wrap_inverse(math.atan),
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        # logs / expo / sqrt / misc
        "ln": math.log,          # natural log
        "log": math.log10,       # log base 10
        "sqrt": math.sqrt,
        "exp": math.exp,
        "pow": pow,
        "abs": abs,
        "pi": math.pi,
        "e": math.e,
    }

    # Evaluate using only 'allowed' names and no builtins
    return eval(s, {"__builtins__": None}, allowed)

# -- replace the button layout so "white" top buttons are only in the first row --
button_values = [
    ["AC",   "+/-",  "%",    "DEG"],   # top (light) row
    ["sin",  "cos",  "tan",  "ln"],
    ["asin", "acos", "atan", "log"],
    ["sinh", "cosh", "tanh", "exp"],
    ["π",    "e",    "^",    "√"],
    ["7",    "8",    "9",    "÷"],
    ["4",    "5",    "6",    "×"],
    ["1",    "2",    "3",    "-"],
    ["0",    ".",    "(",    ")"],
    ["",     "",     "",     "="]   # empty cells allowed
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%", "DEG"]

row_count = len(button_values) #5
column_count = len(button_values[0]) #4

color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

#hover colors
color_light_gray_hover = "#EDEDED"
color_dark_gray_hover = "#6E6E6E"
color_orange_hover = "#FFB84D"

#window setup
window = tkinter.Tk() #create the window
window.title("DiddyBlud Calculator")
# allow free resizing
window.resizable(True, True)

# scalable fonts - prefer Digital-7, fallback if not installed
preferred_font = "Digital-7"
if preferred_font in tkfont.families():
    label_font = tkfont.Font(family=preferred_font, size=45)
    button_font = tkfont.Font(family=preferred_font, size=30)
else:
    # fallback to a monospaced font if Digital-7 is not available
    label_font = tkfont.Font(family="Courier New", size=45)
    button_font = tkfont.Font(family="Courier New", size=30)

frame = tkinter.Frame(window)

# use the scalable label font here
label = tkinter.Label(frame, text="", font=label_font, background=color_black,
                      foreground=color_white, anchor="e", width=column_count)

label.grid(row=0, column=0, columnspan=column_count, sticky="nsew")

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=button_font,
                                command=lambda value=value: button_clicked(value))
        
        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_gray)
            hover_bg = color_light_gray_hover
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
            hover_bg = color_orange_hover
        else:
            button.config(foreground=color_white, background=color_dark_gray)
            hover_bg = color_dark_gray_hover

        # set hand cursor and save original bg for restore on leave
        orig_bg = button.cget("background")
        button.config(cursor="hand2")
        button.bind("<Enter>", lambda e, b=button, h=hover_bg: b.config(background=h))
        button.bind("<Leave>", lambda e, b=button, o=orig_bg: b.config(background=o))
        
        # make every button expand to fill its grid cell
        button.grid(row=row+1, column=column, sticky="nsew")

# configure grid weights so label and buttons scale with window
for c in range(column_count):
    frame.grid_columnconfigure(c, weight=1)
for r in range(row_count + 1):  # +1 for the label row
    frame.grid_rowconfigure(r, weight=1)

# allow frame to expand inside the window
frame.pack(fill="both", expand=True)

# dynamically adjust font sizes when the window is resized
def _on_resize(event):
    # adapt button font to cell size and label font to available label width
    try:
        w, h = event.width, event.height
    except AttributeError:
        w = window.winfo_width()
        h = window.winfo_height()

    # compute approximate cell dimensions (including the label row)
    cell_w = max(1, w / column_count)
    cell_h = max(1, h / (row_count + 1))

    # button font size
    btn_size = max(8, int(min(cell_w / 4, cell_h / 2)))
    button_font.configure(size=btn_size)

    # label font
    available_width = max(10, int(w - 24))  # padding for safety
    text = label["text"] if label["text"] != "" else "0"

    # start size relative to cell height
    size = max(12, int(cell_h * 0.6))
    label_font.configure(size=size)

    # reduce size until   hit a minimum
    while label_font.measure(text) > available_width and size > 8:
        size -= 1
        label_font.configure(size=size)

#mdas
A = ""
operator = None
B = None

def clear_all():
    global A, B, operator
    A = ""
    operator = None
    B = None

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

# -- replace/overwrite button_clicked with expr-based handling (uses evaluate_expression) --
def button_clicked(value):
    global right_symbols, top_symbols, label, expr, trig_degrees, window

    # Evaluate
    if value == "=":
        if expr.strip() == "":
            return
        try:
            result = evaluate_expression(expr)
            label["text"] = remove_zero_decimal(float(result))
            expr = str(remove_zero_decimal(float(result)))
        except Exception:
            label["text"] = "Error"
            expr = ""
        return

    # Top row controls
    if value == "AC":
        expr = ""
        label["text"] = ""
        return

    if value == "+/-":
        # toggle sign of whole expression / last value: evaluate then negate
        try:
            if expr.strip() == "":
                current = 0.0
            else:
                current = evaluate_expression(expr)
            current = -current
            expr = remove_zero_decimal(float(current))
            label["text"] = expr
        except Exception:
            label["text"] = "Error"
            expr = ""
        return

    if value == "%":
        try:
            if expr.strip() == "":
                current = 0.0
            else:
                current = evaluate_expression(expr)
            current = current / 100.0
            expr = remove_zero_decimal(float(current))
            label["text"] = expr
        except Exception:
            label["text"] = "Error"
            expr = ""
        return

    if value == "DEG":
        trig_degrees = not trig_degrees
        # update title so user sees mode
        window.title(f"DiddyBlud Calculator — {'DEG' if trig_degrees else 'RAD'}")
        return

    # functions and π/e
    funcs = {"sin": "sin(", "cos": "cos(", "tan": "tan(", "asin": "asin(", "acos": "acos(", "atan": "atan(",
             "sinh": "sinh(", "cosh": "cosh(", "tanh": "tanh(", "ln": "ln(", "log": "log(", "sqrt": "sqrt(",
             "exp": "exp(", "pow": "pow("}
    if value in funcs:
        expr += funcs[value]
        label["text"] = expr
        return

    if value == "π" or value == "pi":
        # use 'pi' token for evaluation; display shows π (append π to display but expr uses 'pi')
        expr += "pi"
        label["text"] = expr
        return

    if value == "e":
        expr += "e"
        label["text"] = expr
        return

    # operators and parentheses/dot/digits
    if value in ["÷", "×", "-", "+", "^"]:
        # append operator with spaces for readability
        expr += f" {value} "
        label["text"] = expr
        return

    if value == "√":
        # sqrt shortcut: insert sqrt( so user can supply number or close paren
        expr += "sqrt("
        label["text"] = expr
        return

    if value in ("(", ")"):
        expr += value
        label["text"] = expr
        return

    if value == ".":
        expr += "."
        label["text"] = expr
        return

    if value in "0123456789":
        expr += value
        label["text"] = expr
        return

    # ignore empty cells
    return

#centering

window.update() #update window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

#format times widht somethin

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()