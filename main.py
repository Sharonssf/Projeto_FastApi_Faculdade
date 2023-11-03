from fastapi import FastAPI

app = FastAPI()

vendas = {
    1: {"produto" : "Acer Nitro 5", "preco_unitario" : "5000", "quantidade" : "10"}
    2: {"produto" : "Alienware", "preco_unitario" : "20000", "quantidade" : "2"}
    3: {"produto" : "Ideapad 3", "preco_unitario" : "4000", "quantidade" : "15"}
    4: {"produto" : "Ideapad 3i", "preco_unitario" : "3000", "quantidade" : "25"}
    5: {"produto" : "Dell  G15", "preco_unitario" : "10000", "quantidade" : "4"}
}

@app.get("/")
def home():
    return "Seja bem vindo a minha primeira API!!"

@app.get("/vendas")
def quantidade_de_vendas(vendas: dict):
    return {"Quantidade das vendas: ": len(vendas)}

@app.get("/vendas/{id_venda}")
def pegar_venda(id_venda: int):
    return vendas[id_venda]

