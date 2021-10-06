from fastapi import FastAPI
import sqlalchemy, uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

# Change the next line to suit your project.
engine = sqlalchemy.create_engine('mssql+pymssql://localhost/shipit') 
############################################

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/query/shipitsize")
async def root():
    with engine.connect() as conn:
        with open("shipitsize.sql", "r") as f:
            result = conn.execute(sqlalchemy.text(f.read()))

            results = result.all()

        return {"result":results[0]}  


@app.get("/query/configsize")
async def root():

    with engine.connect() as conn:
        with open("configsize.sql", "r") as f:
            result = conn.execute(sqlalchemy.text(f.read()))

            results = result.all()

        return {"result":results[0]}   

@app.get("/query/truncate")
async def root():
    try:
        with engine.connect() as conn:
            with open("truncate.sql", "r") as f:
                result = conn.execute(sqlalchemy.text(f.read()))

            return {"result":"Truncated successfully."}
    except:
        return {"result":"Internal Server Error"}

@app.get("/query/direct")
async def root(dbaction: str = "noaction"):
    if dbaction == "noaction":
        return {"error":"No DBaction specified. DBaction can be one of the following: 'shipit', 'config', or 'truncate'."}
    elif dbaction == "shipit":
        with engine.connect() as conn:
            with open("shipitsize.sql", "r") as f:
                result = conn.execute(sqlalchemy.text(f.read()))
                results = result.all()
            return results
    elif dbaction == "config":
        with engine.connect() as conn:
            with open("configsize.sql", "r") as f:
                result = conn.execute(sqlalchemy.text(f.read()))
                results = result.all()
            return results
    elif dbaction == "truncate":
        try:
            with engine.connect() as conn:
                with open("truncate.sql", "r") as f:
                    result = conn.execute(sqlalchemy.text(f.read()))
                return {"result":True}
        except:
            return {"result":False}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info")