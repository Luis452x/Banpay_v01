import requests
from fastapi.responses import JSONResponse

URLGhibli="https://ghibliapi.vercel.app"
Roles=['films', 'people', 'locations', 'species', 'vehicles']
def get_data_by_rol(rol):
    if rol not in Roles:
        return {'Error':"Rol invalido"}
    info= requests.get(f'{URLGhibli}//{rol}')
    if info.status_code == 200:
        return JSONResponse(status_code=200, content=info.json())
    else:
        return {'message': 'Failed'}