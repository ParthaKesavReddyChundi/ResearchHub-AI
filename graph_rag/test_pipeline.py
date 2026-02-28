"""
Quick test pipeline — processes only 3 chunks to verify the full flow:
PDF → Groq LLM (entity extraction) → Neo4j (knowledge graph)
"""
import os
import time
import logging
import dotenv
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

logging.info('=== QUICK TEST PIPELINE (3 chunks only) ===')

# 1) Load and split PDF
from langchain_text_splitters import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader

splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
pdf_loader = PyPDFLoader(file_path='files/sample.pdf', extract_images=False)
all_documents = pdf_loader.load_and_split(text_splitter=splitter)
logging.info(f'Total chunks in PDF: {len(all_documents)}')

# Only take 3 chunks for testing
documents = all_documents[:3]
logging.info(f'Using {len(documents)} chunks for this test')

# 2) Set up Groq LLM
from langchain_groq import ChatGroq
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

# 3) Set up the prompt and transformer (same as pipeline.py)
from langchain_experimental.graph_transformers.llm import SystemMessage
system_prompt = """
You are a data scientist working for the police and you are building a knowledge graph database. 
Your task is to extract information from data and convert it into a knowledge graph database.
Provide a set of Nodes in the form [head, head_type, relation, tail, tail_type].
It is important that the head and tail exists as nodes that are related by the relation.
If you can't pair a relationship with a pair of nodes don't add it.
When you find a node or relationship you want to add try to create a generic TYPE for it that describes the entity you can also think of it as a label.
You must generate the output in a JSON format containing a list with JSON objects. Each object should have the keys: "head", "head_type", "relation", "tail", and "tail_type".
"""
system_message = SystemMessage(content=system_prompt)

from pydantic import BaseModel, Field

class UnstructuredRelation(BaseModel):
    head: str = Field(description="extracted head entity like Person, Crime, Object, Vehicle, Location, etc. Must use human-readable unique identifier.")
    head_type: str = Field(description="type of the extracted head entity like Person, Crime, Object, Vehicle, etc")
    relation: str = Field(description="relation between the head and the tail entities")
    tail: str = Field(description="extracted tail entity like Person, Crime, Object, Vehicle, Location, etc. Must use human-readable unique identifier.")
    tail_type: str = Field(description="type of the extracted tail entity like Person, Crime, Object, Vehicle, etc")

from langchain_experimental.graph_transformers.llm import JsonOutputParser, PromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
parser = JsonOutputParser(pydantic_object=UnstructuredRelation)

examples = [
    {"text": "Michael Johnson was mugged at knife-point by two assailants on 5th Avenue.", "head": "Michael Johnson", "head_type": "Person", "relation": "VICTIM_OF", "tail": "Mugging", "tail_type": "Crime"},
    {"text": "John Doe was caught selling illegal drugs in Central Park.", "head": "John Doe", "head_type": "Person", "relation": "SUSPECT_IN", "tail": "Drug Trafficking", "tail_type": "Crime"},
]

human_prompt = PromptTemplate(
    template="""
Examples:
{examples}

For the following text, extract entities and relations as in the provided example.
{format_instructions}\nText: {input}""",
    input_variables=["input"],
    partial_variables={
        "format_instructions": parser.get_format_instructions(),
        "node_labels": None,
        "rel_types": None,
        "examples": examples,
    },
)
human_message_prompt = HumanMessagePromptTemplate(prompt=human_prompt)
chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message_prompt])

from langchain_experimental.graph_transformers import LLMGraphTransformer
llm_transformer = LLMGraphTransformer(llm=llm, prompt=chat_prompt)

# 4) Process documents one at a time with rate limiting
graph_documents = []
for i, doc in enumerate(documents):
    logging.info(f'Processing chunk {i+1}/{len(documents)}...')
    retries = 0
    while retries < 5:
        try:
            result = llm_transformer.convert_to_graph_documents([doc])
            graph_documents.extend(result)
            logging.info(f'  ✓ Extracted {len(result[0].nodes)} nodes and {len(result[0].relationships)} relationships')
            break
        except Exception as e:
            if '429' in str(e) or 'rate_limit' in str(e).lower():
                wait_time = 30 * (retries + 1)
                logging.warning(f'  Rate limited! Waiting {wait_time}s...')
                time.sleep(wait_time)
                retries += 1
            else:
                logging.error(f'  Error: {e}')
                break
    if i < len(documents) - 1:
        logging.info('  Waiting 20s for rate limits...')
        time.sleep(20)

# 5) Insert into Neo4j
logging.info('Inserting into Neo4j...')
from langchain_neo4j import Neo4jGraph
graph = Neo4jGraph()
graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)

# 6) Verify
logging.info('Verifying data in Neo4j...')
result = graph.query("MATCH (n) RETURN count(n) as node_count")
logging.info(f'Total nodes in Neo4j: {result}')
result = graph.query("MATCH ()-[r]->() RETURN count(r) as rel_count")
logging.info(f'Total relationships in Neo4j: {result}')

logging.info('=== TEST COMPLETE! ===')
logging.info('You can now run: python graph_rag.py')
