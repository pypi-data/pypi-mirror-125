from re import sub
from random import choice


owo_faces = [";;w;;", "owo", "UwU", ">w<", "^w^"]


def owoify(text: str) -> str:
    r = sub(r"r|l", "w", text)
    r = sub(r"R|L", "W", r)
    r = sub(r"n([aeiou])", r"ny\1", r)
    r = sub(r"N([aeiou])", r"Ny\1", r)
    r = sub(r"N([AEIOU])", r"NY\1", r)
    r = r.replace("ove", "uv")
    r = sub(r"!+", f" {choice(owo_faces)} ", r)
    r = r.replace("?", "?OwO")
    return r
