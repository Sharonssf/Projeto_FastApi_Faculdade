import json
import sqlite3
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Modelo de dados para personagens de Invincible
class Character(BaseModel):
    name: str
    alias: str
    superpower: str

# Função para criar a tabela no banco de dados
def create_table():
    connection = sqlite3.connect("characters.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            alias TEXT,
            superpower TEXT
        )
        """
    )
    connection.commit()
    connection.close()

# Função para carregar os personagens do banco de dados
def load_characters():
    connection = sqlite3.connect("characters.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM characters")
    characters = [{"id": row[0], "name": row[1], "alias": row[2], "superpower": row[3]} for row in cursor.fetchall()]
    connection.close()
    return characters

# Função para salvar os personagens no banco de dados
def save_characters(characters):
    connection = sqlite3.connect("characters.db")
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO characters (name, alias, superpower) VALUES (?, ?, ?)", [(c["name"], c["alias"], c["superpower"]) for c in characters])
    connection.commit()
    connection.close()

# Cria a tabela no banco de dados ao iniciar a aplicação
create_table()
# Lista de personagens de Invincible (simulando uma "base de dados")
characters_db = load_characters()

# 1) GET: Consulta geral sem parâmetros
@app.get("/")
def ola():
    return "Seja bem vindo, a nossa API de personagens de invencivel. Vá até o /docs e liste seus personagens."

# 2) GET: Consulta especifica com parâmetros (usar alguma propriedade do dados para fazer a filtragem)
@app.get("/characters/{property}/{value}", response_model=List[Character])
def filter_characters(property: str, value: str):
    filtered_characters = [character for character in characters_db if getattr(character, property) == value]
    return filtered_characters

# 3) POST: Inserção de novo elemento nos dados
@app.post("/characters/", response_model=Character)
def create_character(character: Character):
    characters_db.append(character)
    save_characters(characters_db)
    return character

# 4) PUT ou PATCH: Atualização dos dados
@app.put("/characters/{character_id}", response_model=Character)
def update_character(character_id: int, updated_character: Character):
    if character_id < len(characters_db):
        characters_db[character_id] = updated_character
        save_characters(characters_db)
        return updated_character
    raise HTTPException(status_code=404, detail="Personagem não encontrado")

# 5) DELETE: Deleção dos dados
@app.delete("/characters/{character_id}", response_model=Character)
def delete_character(character_id: int):
    if character_id < len(characters_db):
        deleted_character = characters_db.pop(character_id)
        save_characters(characters_db)
        return deleted_character
    raise HTTPException(status_code=404, detail="Personagem não encontrado")

# 6) GET: Renderiza a página home da sua API.
@app.get("/home", response_class=HTMLResponse)
def read_home():
    return templates.TemplateResponse("home.html", {"request": None})

# 7) POST: Receber informações em um formulário e redirecionar para outra página
@app.post("/form")
def form_post(character: Character = Form(...)):
    characters_db.append(character)
    save_characters(characters_db)
    return {"message": "Informações recebidas com sucesso!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
