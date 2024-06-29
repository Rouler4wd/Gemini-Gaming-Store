import os
import random
import google.generativeai as genai
import gradio as gr

# Set your Google API key here
GOOGLE_API_KEY = "ENTER_YOUR_API_KEY_HERE"

# Configure the API key
genai.configure(api_key=GOOGLE_API_KEY)

# List available models
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

# Choose the model
model = genai.GenerativeModel(model_name="gemini-pro")

# Initialize the order
order = []

# Generate a random discount between 10% and 90%
discount_percentage = random.randint(10, 90)
print(f"Today's Discount: {discount_percentage}% off")

# Base prices for items (example prices)
prices = {
    "Xbox Controller": 60,
    "PlayStation Controller": 60,
    "Nintendo Switch Pro Controller": 70,
    "Wired Gaming Headset": 50,
    "Wireless Gaming Headset": 80,
    "VR Headset": 300,
    "Mechanical Keyboard": 100,
    "Membrane Keyboard": 40,
    "Gaming Mouse": 30,
    "Ergonomic Mouse": 50,
    "Mouse Pad": 20,
    "Charging Dock": 25,
    "Headset Stand": 30
}

additional_discount = 0

def apply_discount(price):
    total_discount = discount_percentage + additional_discount
    return price * (1 - total_discount / 100)

def add_to_order(item, color, connection, features):
    modifiers = {
        "Color options": color,
        "Connection types": connection,
        "Additional features": features
    }
    if item in prices:
        price = apply_discount(prices[item])
        order.append((item, modifiers, price))
    else:
        return f"Item '{item}' is not on the menu."
    return get_order()

def remove_item(item):
    global order
    order = [i for i in order if i[0] != item]
    return f"Removed '{item}' from the order. Current order: {get_order()}"

def clear_order():
    global order
    order = []
    return "Order cleared."

def get_order():
    return order

def confirm_order():
    return order

def place_order():
    global order
    placed_order = order.copy()
    clear_order()
    return placed_order

def apply_promo_code(code):
    global additional_discount
    promo_codes = {
        "123": 10,
        "hello": 5,
        "arcade": 15,
        "hack": 20,
        "python": 8,
        "gaming": 12
    }
    if code in promo_codes:
        additional_discount = promo_codes[code]
        return f"Promo code '{code}' applied! Additional {promo_codes[code]}% off. Total discount is now {discount_percentage + additional_discount}%."
    else:
        return "Invalid promo code. Please enter a valid promo code."
# Define Gradio interface functions
def add_item_interface(item, color, connection, features):
    return add_to_order(item, color, connection, features)

def remove_item_interface(item):
    return remove_item(item)

def clear_order_interface():
    return clear_order()

def confirm_order_interface():
    return confirm_order()

def place_order_interface():
    return place_order()

def apply_promo_code_interface(code):
    return apply_promo_code(code)

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Gaming Accessories Store")
    gr.Markdown("## Hours: Monday, Wednesday, and Friday from 12pm to 5pm")
    gr.Markdown(f"### Today's Discount: {discount_percentage}% off")
    gr.Markdown("### Enter a 3-digit promo code for an additional discount!")

    gr.Markdown("""
    ### MENU:
    **Controllers:**
    - Xbox Controller
    - PlayStation Controller
    - Nintendo Switch Pro Controller

    **Headsets:**
    - Wired Gaming Headset
    - Wireless Gaming Headset
    - VR Headset

    **Keyboards:**
    - Mechanical Keyboard
    - Membrane Keyboard

    **Mice:**
    - Gaming Mouse
    - Ergonomic Mouse

    **Accessories:**
    - Mouse Pad
    - Charging Dock
    - Headset Stand

    **Modifiers:**

    **Color Options:**
    - Default: Black
    - Other Options: White, Red, Blue, Green

    **Connection Types:**
    - Default: Wired
    - Other Options: Wireless

    **Additional Features:**
    - RGB Lighting
    - Extra Buttons
    - Adjustable DPI
    - Noise Cancellation
    - Microphone
    - VR Compatibility

    *Please note that Yellow color options are not available today.*
    """)

    item = gr.Dropdown(label="Item", choices=list(prices.keys()))
    color = gr.Dropdown(label="Color", choices=["Black", "White", "Red", "Blue", "Green"])
    connection = gr.Dropdown(label="Connection Type", choices=["Wired", "Wireless"])
    features = gr.CheckboxGroup(label="Additional Features", choices=["RGB Lighting", "Extra Buttons", "Adjustable DPI", "Noise Cancellation", "Microphone", "VR Compatibility"])

    order_display = gr.Textbox(label="Current Order")

    add_button = gr.Button("Add to Order")
    add_button.click(add_item_interface, inputs=[item, color, connection, features], outputs=order_display)

    remove_item_input = gr.Textbox(label="Remove Item")
    remove_button = gr.Button("Remove Item")
    remove_button.click(remove_item_interface, inputs=remove_item_input, outputs=order_display)

    clear_button = gr.Button("Clear Order")
    clear_button.click(clear_order_interface, outputs=order_display)

    confirm_button = gr.Button("Confirm Order")
    confirm_button.click(confirm_order_interface, outputs=order_display)

    place_button = gr.Button("Place Order")
    place_button.click(place_order_interface, outputs=order_display)

    promo_code_input = gr.Textbox(label="Enter Promo Code")
    promo_code_button = gr.Button("Apply Promo Code")
    promo_code_button.click(apply_promo_code_interface, inputs=promo_code_input, outputs=order_display)

# Launch the Gradio app with sharing enabled
demo.launch(share=True)
