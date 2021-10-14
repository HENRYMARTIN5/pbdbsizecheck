
######################################################################################################
# Made by                                                                                            #
#                                                                                                    #
#  ██╗  ██╗███████╗███╗   ██╗██████╗ ██╗   ██╗    ███╗   ███╗ █████╗ ██████╗ ████████╗██╗███╗   ██╗  #
#  ██║  ██║██╔════╝████╗  ██║██╔══██╗╚██╗ ██╔╝    ████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██║████╗  ██║  #
#  ███████║█████╗  ██╔██╗ ██║██████╔╝ ╚████╔╝     ██╔████╔██║███████║██████╔╝   ██║   ██║██╔██╗ ██║  #
#  ██╔══██║██╔══╝  ██║╚██╗██║██╔══██╗  ╚██╔╝      ██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ██║██║╚██╗██║  #
#  ██║  ██║███████╗██║ ╚████║██║  ██║   ██║       ██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ██║██║ ╚████║  #
#  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝  #   
#                                                                                                    #
######################################################################################################

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi


from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

import sqlalchemy 
from sqlalchemy.engine import Engine
import uvicorn

# Change the next line to suit your project.
engine:Engine = sqlalchemy.create_engine('mssql+pymssql://sa:<brepacknho!d21>@localhost/shipit')
# engine:Engine = sqlalchemy.create_engine('mssql+pymssql://localhost/shipit')
############################################

API_KEY:str = 'ABC123'
API_KEY_NAME:str = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

templates = Jinja2Templates(directory="templates")

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header)
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@app.get('/')
async def root(request: Request, api_key: APIKey = Depends(get_api_key)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/query/shipitsize")
async def root(api_key: APIKey = Depends(get_api_key)):
    with engine.connect() as conn:
        with open("shipitsize.sql", "r") as f:
            
            sqlQuery = f.read()
            f.close()

            result = conn.execute(sqlQuery)
            resultObj = {}

            for row in result:
                resultObj["FILE_SIZE_MB"] = row["FILE_SIZE_MB"]
                resultObj["FREE_SPACE_MB"] = row["FREE_SPACE_MB"]
                resultObj["SPACE_USED_MB"] = row["SPACE_USED_MB"]
                resultObj["FILENAME"] = row["FILENAME"]
                resultObj["NAME"] = row["NAME"]

        return {"result":resultObj}


@app.get("/query/configsize")
async def root(api_key: APIKey = Depends(get_api_key)):

    with engine.connect() as conn:
        with open("configsize.sql", "r") as f:
            sqlQuery = f.read()
            f.close()

            result = conn.execute(sqlQuery)
            resultObj = {}

            for row in result:
                resultObj["FILE_SIZE_MB"] = row["FILE_SIZE_MB"]
                resultObj["FREE_SPACE_MB"] = row["FREE_SPACE_MB"]
                resultObj["SPACE_USED_MB"] = row["SPACE_USED_MB"]
                resultObj["FILENAME"] = row["FILENAME"]
                resultObj["NAME"] = row["NAME"]

        return {"result":resultObj} 




@app.get("/query/truncate")
async def root(api_key: APIKey = Depends(get_api_key)):
    try:
        with engine.connect().execution_options(autocommit=True) as conn:
            with open("truncate.sql", "r") as f:
                
                sqlQuery = f.read()
                f.close()

                result = conn.execute(sqlQuery)

            return {"result": "Truncated successfully!"}
    except Exception as e:
        print("Unexpected error: "+e)
        return {"result": "Internal Server Error"}



@app.get("/query/direct")
async def root(dbaction: str = "noaction", api_key: APIKey = Depends(get_api_key)):
    if dbaction == "noaction":
        return {"error":"No DBaction specified. DBaction can be one of the following: 'shipit', 'config', or 'truncate'."}
    elif dbaction == "shipit":
        with engine.connect() as conn:
            with open("shipitsize.sql", "r") as f:
                sqlQuery = f.read()
                f.close()

                result = conn.execute(sqlQuery)
                resultObj = {}

                for row in result:
                    resultObj["FILE_SIZE_MB"] = row["FILE_SIZE_MB"]
                    resultObj["FREE_SPACE_MB"] = row["FREE_SPACE_MB"]
                    resultObj["SPACE_USED_MB"] = row["SPACE_USED_MB"]
                    resultObj["FILENAME"] = row["FILENAME"]
                    resultObj["NAME"] = row["NAME"]

            return {"result":resultObj} 
    elif dbaction == "config":
        with engine.connect() as conn:
            with open("configsize.sql", "r") as f:
                sqlQuery = f.read()
                f.close()

                result = conn.execute(sqlQuery)
                resultObj = {}

                for row in result:
                    resultObj["FILE_SIZE_MB"] = row["FILE_SIZE_MB"]
                    resultObj["FREE_SPACE_MB"] = row["FREE_SPACE_MB"]
                    resultObj["SPACE_USED_MB"] = row["SPACE_USED_MB"]
                    resultObj["FILENAME"] = row["FILENAME"]
                    resultObj["NAME"] = row["NAME"]

            return {"result":resultObj} 
    elif dbaction == "truncate":
        try:
            with engine.connect() as conn:
                with open("truncate.sql", "r") as f:
                    result = conn.execute(f.read())
                return {"result":True}
        except:
            return {"result":False}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8888, log_level="info")