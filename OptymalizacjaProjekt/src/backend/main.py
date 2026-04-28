from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from src.backend.models import FarmConfig
from src.backend.core.constants import PLANTS_DB
from src.backend.core.worker import run_heavy_simulation

# Importujemy nasze nowe narzędzia zabezpieczające
from src.backend.core.auth import create_access_token, verify_token

app = FastAPI(title="Symulator Gospodarstwa API")

# --------- NOWOŚĆ: Logowanie --------- #
class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    """
    Sprawdzamy hasło. Na razie "na sztywno" w kodzie. 
    W przyszłości dodamy tu połączenie z bazą danych PostgreSQL.
    """
    if data.username == "farmer" and data.password == "krowa123":
        # Hasło poprawne! Wystawiamy token dla tego użytkownika
        token = create_access_token({"sub": data.username})
        return {"access_token": token, "token_type": "bearer"}
    
    # Złe hasło? Kopa z lokalu.
    raise HTTPException(status_code=401, detail="Błędny login lub hasło")


# --------- ZMIANA: Zabezpieczony Endpoint --------- #

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/plants")
def get_all_plants():
    return PLANTS_DB

# MAGIA: Zauważ dodanie parametru "user_id: str = Depends(verify_token)"
@app.post("/simulate")
def start_simulation(config: FarmConfig, current_user: str = Depends(verify_token)):
    """
    Zanim ta funkcja w ogóle się uruchomi, FastAPI wywoła verify_token.
    Jeśli token będzie zły, kod nawet nie dotrze do tego miejsca!
    """
    task = run_heavy_simulation.delay(config.years_number, config.field_number)
    
    return {
        "message": f"Cześć {current_user}! Zadanie zostało przyjęte w tle.",
        "task_id": task.id
    }