def marketPricePrompt():
    return (
        "Given the following data or update, extract and list the latest mandi and retail prices "
        "for only tomatoes and mangoes in nearby locations of Mandya except Mandya"
        "Mention crop name, mandi price, and retail price clearly. "
        "Dont reason about price drop just give price comparison of different districts"
        "Response must be in Kannada, short, simple, and suitable for rural farmers using a mobile chatbot. "
        "Avoid any reasons or extra information—only show prices and location."
    )
