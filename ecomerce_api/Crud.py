from fastapi import APIRouter, HTTPException
from connection.db import conection
from models.Cruds import comerce, ItemUpdate
from bson import ObjectId

crud = APIRouter()
crud_conection = conection()

@crud.post('/create')
async def crud_create(request: comerce):
   is_data = crud_conection['e-comerce'].find_one({'name': request.name})

   if is_data:
       raise HTTPException(status_code=400, detail="Data already exist")
   
   data = {
       'name': request.name,
       'price': request.price,
       'quantity': request.quantity,
       'description': request.description,
       'category': request.category,
       'image': request.image,  
       'rating': request.rating
   }
   try:
       crud_conection['e-comerce'].insert_one(data)
       return {"message": "Data created"}
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))
   
@crud.get('/read')
async def read_all():
    crud_collection = conection()['e-comerce']
    all_data = list(crud_collection.find())
    json_data = []
    for data in all_data:
        data['_id'] = str(data['_id'])
        json_data.append(data)
    return {"data": json_data}


@crud.put('/update')
async def update_data(item_id: str, updated_data: ItemUpdate):
    crud_collection = conection()['e-comerce']
    result = crud_collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_data.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"message": "Data updated successfully"}

@crud.delete('/delete')
async def delete_data(item_id: str):
    crud_collection = conection()['e-comerce']
    result = crud_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"message": "Data deleted successfully"}