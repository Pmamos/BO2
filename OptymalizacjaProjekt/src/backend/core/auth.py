import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


SECRET_KEY = "moje-super-tajne-haslo-do-farmy"
ALGORITHM = "HS256"

# To informuje FastAPI, że będziemy szukać nagłówka "Authorization: Bearer ..."
security = HTTPBearer()

def create_access_token(data: dict):
    """Bierze dane (np. nazwę użytkownika), dodaje czas wygaśnięcia i tworzy Token JWT"""
    to_encode = data.copy()
    
    # Bilet jest ważny tylko przez 30 minut
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    # Serwer składa kryptograficzny podpis
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """To jest nasz Bramkarz. Stoi przed wejściem i sprawdza bilet (Token)"""
    token = credentials.credentials
    try:
        # Próba odkodowania i weryfikacji podpisu
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub") # Zwraca nazwę użytkownika zapisaną w tokenie
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Bilet wygasł! Zaloguj się ponownie.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Fałszywy bilet! Ochrona wezwana.")