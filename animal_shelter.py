from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):


    def __init__(self):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'Jesus27'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31134
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        
    def getNextRecordNum(self):
            last_record = self.collection.find_one(sort=[("rec_num", -1)])
            return (last_record["rec_num"] + 1) if last_record else 1

# create method to implement the C in CRUD.
    def create(self, data):
        if data and isinstance (data, list): #data is a list
            for record in data:
                if not isinstance(record, dict): #validates items
                    raise Exception("Each item in the data list must be a dictionary")
                
                # Assign a unique record number
                index_num = self.getNextRecordNum()
                record["rec_num"] = self.getNextRecordNum() #update record number
                
                # Insert
                ret = self.database.animals.insert_one(record)
                
                #Validate Id
                if not ObjectId.is_valid(ret.inserted_id):
                    return False # Return false in insertion fails
                
            return True # If insertion succeeds
        else:
            raise Exception("Nothing to save, because data parameter is empty")
                
                
       
            

            
# Create method to implement the R in CRUD.

    def read(self, data): #ensure data is provided
        if data is not None:
            cursor = self.database.animals.find(data)
            out = [doc for doc in cursor]
        else:
            out = self.database.animals.find_one()
        return out
        
# Update method to implement the U in CRUD
    def update(self, query, new_values, multiple=False):
        if query is None or new_values is None:
            raise Exception("Query and new values can not be empty")
            
        update_data = {"$set": new_values}
        try:
            if multiple:
                result = self.collection.update_many(query, update_data)
            else:
                result = self.collection.update_one(query, update_data)
            return result.modified_count
        except:
            return 0 # Return 0 if update fails
        
    
# Delete method to implement the D in CRUD
    def delete(self, query, multiple=False):
        if query is None:
            raise Exception("Query can not be empty")
            
        try:
            if multiple:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        
        except:
            return 0 # Returns 0 if no deletion


        

        
    
    
    