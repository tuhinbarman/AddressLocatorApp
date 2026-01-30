from math import cos,radians
from fastapi import APIRouter,Depends, Query,WebSocket,WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import func,String,cast
from fastapi.responses import JSONResponse
from starlette import status
from database import *
from models import Address
from schemas import AddressRequest
from datetime import datetime

router = APIRouter(prefix='',tags=['rooms'])

@router.get('/address')
async def get_addresses(db : Session = Depends(get_db)):

    try:
        data = db.query(Address).all()
        response = []
        for address in data:
            response.append(
                {
                    'name' : address.name,
                    'city' : address.city,
                    'state' : address.state,
                    'country' : address.country,
                    'latitude' : address.latitude,
                    'longitude' : address.longitude

                }
            )
        return JSONResponse(content={'data' : response,'message' : 'Success'},status_code=200)


    except Exception as err:
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)
    
@router.post("/address")
def create(request: AddressRequest, db: Session = Depends(get_db)):
    try:
        request_data = request.model_dump()
        address = Address(
            name = request_data['name'],
            city = request_data['city'],
            state = request_data['state'],
            country = request_data['country'],
            latitude = request_data['latitude'],
            longitude = request_data['longitude'],    
        )
        db.add(address)
        db.commit()
        db.refresh(address)

        return JSONResponse(content={'data' : 'Address is created successfully','message' : 'Success'},status_code=200)

    except Exception as err:
        db.rollback()
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)

@router.put("/address")    
async def update_address(request : AddressRequest,db : Session =  Depends(get_db)):

    try:
        request_data = request.model_dump()
        address = db.query(Address).filter(Address.id == request_data['id']).first()

        if not address:
            return JSONResponse(content={'data' : 'No address found!!','message' : 'Fail'},status_code=404)
        
        address.city = request_data['city']
        address.state = request_data['state']
        address.country = request_data['country']
        address.latitude = request_data['latitude']
        address.longitude = request_data['longitude']
        address.name = request_data['name']


        db.commit()
        db.refresh(address)

        return JSONResponse(content={'data' : 'Data updated successfully','message' : 'Success'},status_code=200)

    except Exception as err:
        db.rollback()
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)
    
@router.delete("/address")    
async def update_address(request : AddressRequest,db : Session =  Depends(get_db)):

    try:
        request_data = request.model_dump()
        address = db.query(Address).filter(Address.id == request_data['id']).first()

        if not address:
            return JSONResponse(content={'data' : 'No address found!!','message' : 'Fail'},status_code=404)
        
        db.delete(address)
        db.commit()

        return JSONResponse(content={'data' : 'Address deletion successful','message' : 'Success'},status_code=200)

    except Exception as err:
        db.rollback()
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)

@router.get('/address/near-by') 
def get_nearby_places(user_lat: float = Query(ge=-90, le=90),user_long: float = Query(ge=-180, le=180),
                      distance_km : int = Query( gt=0),db: Session = Depends(get_db)):
    try:
        import pdb;pdb.set_trace()
        if user_lat is None or user_long is None or distance_km is None:
            return JSONResponse(
                status_code=400,
                detail="user_lat, user_long and distance_km are required"
            )

        lat_delta = distance_km / 111
        lon_delta = distance_km / (111 * cos(radians(user_lat)))

        # Bounding box filter
        addresses = (
            db.query(Address)
            .filter(
                Address.latitude.between(user_lat - lat_delta, user_lat + lat_delta),
                Address.longitude.between(user_long - lon_delta, user_long + lon_delta)
            )
            .all()
        )

        result = [{'name' : address.name,
                   'city' : address.city,
                   'state' : address.state,
                   'country' : address.country,
                    'latitude' : address.latitude,
                    'longitude' : address.longitude   
                   } for address in addresses]
        
        return JSONResponse(content = {'data' : result,'message' : 'Fail'},
                                       status_code=200)

    except Exception as err:
        print(err)
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)





                            
