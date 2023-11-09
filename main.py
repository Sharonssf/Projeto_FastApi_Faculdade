from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Definindo o modelo de dados para personagens de Invincible
class Character(BaseModel):
    name: str
    alias: str
    superpower: str

# Lista de personagens de Invincible (simulando uma "base de dados")
characters_db = []

#Só as boas vindas mesmo
@app.get("/")
def ola():
    return "Seja bem vindo, a nossa API de personagens de invencivel. Vá até o /docs e liste seus personagens."

# Operação CREATE (POST) para adicionar um novo personagem
@app.post("/characters/", response_model=Character)
def create_character(character: Character):
    characters_db.append(character)
    return character

# Operação READ (GET) para listar todos os personagens
@app.get("/characters/", response_model=List[Character])
def read_characters():
    return characters_db

# Operação READ (GET) para obter detalhes de um personagem específico
@app.get("/characters/{character_id}", response_model=Character)
def read_character(character_id: int):
    if character_id < len(characters_db):
        return characters_db[character_id]
    raise HTTPException(status_code=404, detail="Personagem não encontrado")

# Operação UPDATE (PUT) para atualizar os detalhes de um personagem
@app.put("/characters/{character_id}", response_model=Character)
def update_character(character_id: int, updated_character: Character):
    if character_id < len(characters_db):
        characters_db[character_id] = updated_character
        return updated_character
    raise HTTPException(status_code=404, detail="Personagem não encontrado")

# Operação DELETE (DELETE) para excluir um personagem
@app.delete("/characters/{character_id}", response_model=Character)
def delete_character(character_id: int):
    if character_id < len(characters_db):
        deleted_character = characters_db.pop(character_id)
        return deleted_character
    raise HTTPException(status_code=404, detail="Personagem não encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
