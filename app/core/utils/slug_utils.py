from nanoid import generate

def generate_slug():
    """ Generate unique slug """
    return generate(size=6)