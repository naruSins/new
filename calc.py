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

def clear_all():
    global expr
    expr = ""

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def evaluate_expression(s):
    # display operators 
    s = s.replace("×", "*").replace("÷", "/")
    # allowing digitaas and operatorz
    if not re.match(r'^[0-9\.\+\-\*\/\(\)\s]+$', s):
        raise ValueError("Invalid characters in expression")
    # evaluate basic
    return eval(s)

def button_clicked(value):
    global right_symbols, top_symbols, label, expr

    # operators and =
    if value in right_symbols:
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
        else:
            # keep display symbol
            if expr == "" and value in "+-×÷":
                # if starting with operator and it's -, allow negative start
                if value == "-":
                    expr += value
            else:
                expr += f" {value} "
            label["text"] = expr if expr != "" else "0"

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"

        elif value == "+/-":
            # toggle sign 
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

        elif value == "%":
            # apply percent 
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

    else: # digits, dot, or √
        if value == "√":
            try:
                if expr.strip() == "":
                    current = 0.0
                else:
                    current = evaluate_expression(expr)
                if current < 0:
                    raise ValueError("sqrt negative")
                current = math.sqrt(current)
                expr = remove_zero_decimal(float(current))
                label["text"] = expr
            except Exception:
                label["text"] = "Error"
                expr = ""
        elif value == ".":
            # allow only one dot in the last number token
            parts = re.split(r'[\s\+\-\×\÷\*\/]+', expr)
            last = parts[-1] if parts else ""
            if "." not in last:
                expr += value
            label["text"] = expr if expr != "" else "0"
        elif value in "0123456789":
            expr += value
            label["text"] = expr if expr != "" else "0"

button_values = [
    ["AC", "+/-", "%", "÷"], 
    ["7", "8", "9", "×"], 
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

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

# scalable fonts
label_font = tkfont.Font(family="Digital-7", size=45)
button_font = tkfont.Font(family="Digital-7", size=30)

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

def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator

    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                # extract the part after the operator from output
                display = label["text"]
                # split once on the operator symbol, take the right-hand side and strip spaces
                parts = display.split(operator, 1)
                b_str = parts[1].strip() if len(parts) > 1 else ""

                if b_str == "":
                    # no B entered — treat as using A
                    try:
                        label["text"] = remove_zero_decimal(float(A))
                    except Exception:
                        label["text"] = "Error"
                else:
                    try:
                        numA = float(A)
                        numB = float(b_str)
                        if operator == "+":
                            res = numA + numB
                        elif operator == "-":
                            res = numA - numB
                        elif operator == "×":
                            res = numA * numB
                        elif operator == "÷":
                            if numB == 0:
                                label["text"] = "Error"
                                clear_all()
                                # stop 
                                return
                            res = numA / numB
                        label["text"] = remove_zero_decimal(res)
                    except Exception:
                        label["text"] = "Error"
                clear_all()

        elif value in "+-×÷": #500 +, *
            if operator is None:
                A = label["text"]
                operator = value
                # show A and the chosen operator on output
                label["text"] = f"{A} {operator} "
                B = ""
            else:
                # switch operator if pressd a different operator
                operator = value
                if A != "":
                    label["text"] = f"{A} {operator} "

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = ""

        elif value == "+/-":
            result = float(label["text"]) * -1
            label["text"] = remove_zero_decimal(result)

        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_zero_decimal(result)           
        
    else: #digits or .
        if value == "√":
            # apply sqrt to current number
            display = label["text"].strip()
            try:
                if display == "":
                    current = 0.0
                elif operator is not None and operator in display:
                    parts = display.split(operator, 1)
                    b_str = parts[1].strip()
                    # choose target: B if present, otherwise A
                    if b_str == "":
                        current = float(A) if A != "" else 0.0
                        new_val = remove_zero_decimal(math.sqrt(current))
                        label["text"] = f"{A} {operator} {new_val}"
                        B = new_val
                    else:
                        current = float(b_str)
                        if current < 0:
                            raise ValueError("sqrt negative")
                        new_val = remove_zero_decimal(math.sqrt(current))
                        label["text"] = f"{parts[0].strip()} {operator} {new_val}"
                        B = new_val
                else:
                    current = float(display) if display != "" else 0.0
                    if current < 0:
                        raise ValueError("sqrt negative")
                    new_val = remove_zero_decimal(math.sqrt(current))
                    label["text"] = new_val
                    A = new_val
            except Exception:
                label["text"] = "Error"
        elif value == ".":
            # allow one dot in the current (last) number token
            last = re.split(r'[\s\+\-\×\÷\*\/]+', label["text"])[-1] if label["text"] else ""
            if "." not in last:
                label["text"] += "."
        elif value in "0123456789":
            # append digit to the current display; if operator shown it will follow
            if label["text"] == "":
                label["text"] = value
            else:
                label["text"] += value



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