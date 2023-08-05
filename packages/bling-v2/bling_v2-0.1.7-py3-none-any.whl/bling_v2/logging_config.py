import logging

# Create handlers
f_handler = logging.FileHandler("bling.log")
f_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
f_handler.setFormatter(f_format)
