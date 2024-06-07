
import uuid
from agency_swarm import BaseTool
from pydantic import BaseModel, Field
from supabase import create_client, Client
import os
from openai import OpenAI
# import { pipeline } from '@xenova/transformers'
# const generateEmbedding = await pipeline('feature-extraction', 'Supabase/gte-small')

# const title = 'First post!'
# const body = 'Hello world!'

# // Generate a vector using Transformers.js
# const output = await generateEmbedding(body, {
#   pooling: 'mean',
#   normalize: true,
# })

# // Extract the embedding output
# const embedding = Array.from(output.data)

# // Store the vector in Postgres
# const { data, error } = await supabase.from('posts').insert({
#   title,
#   body,
#   embedding,
# })

# Initialize Supabase client
PUBLIC_SUPABASE_URL = os.getenv("PUBLIC_SUPABASE_URL")
PUBLIC_SUPABASE_ANON_KEY = os.getenv("PUBLIC_SUPABASE_ANON_KEY")

supabase: Client = create_client(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY)


client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding



class VectorTool(BaseTool, BaseModel):
    """
    Uses pgvector to store and query vectors.
    Has both a method to store new vectors and to query the nearest vectors.
    """
    async def ingest_vector(self, text: str, title: str, body: str):
        """
        Stores a vector in the database.
        """
        vector = get_embedding(text)
        
        
        vec = await supabase.table('vectors').insert({
            'title': str(uuid.uuid4()),
            'body': 'Hello world!',
            'embedding': vector
        })
        return vec
    
    async def semantic_search(self, text: str):
        """
        Queries the nearest vectors to the input text.
        """
        vector = get_embedding(text)
        vec = await supabase.table('vectors').select('embedding').order('embedding <->', vector)
        return vec