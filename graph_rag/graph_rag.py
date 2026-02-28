import os
import logging
import dotenv
dotenv.load_dotenv()
logging.basicConfig(level=logging.WARNING)

print("\n" + "="*60)
print("  🧠 Knowledge Graph RAG — Q&A System")
print("="*60)
print("Loading...")

# Instantiate the Neo4J connector
from langchain_community.graphs import Neo4jGraph
graph = Neo4jGraph()

# Instantiate LLM
from langchain_groq import ChatGroq
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

# Get the graph schema to help the LLM understand the data
schema = graph.schema
print(f"\n📊 Graph Schema:\n{schema}")

# Create a custom Cypher generation prompt that understands natural language better
from langchain_core.prompts import ChatPromptTemplate

CYPHER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Neo4j Cypher query generator. Your task is to convert natural language questions into valid Cypher queries.

IMPORTANT RULES:
1. Always generate VALID Cypher syntax. Never use shortestPath with multiple relationship patterns.
2. Use simple MATCH patterns — avoid complex path functions unless necessary.
3. Use case-insensitive matching with toLower() for better results.
4. Return meaningful properties, not just node references.
5. Use OPTIONAL MATCH when relationships might not exist.
6. Limit results to 25 unless the user asks for more.
7. When looking for connections between concepts, use variable-length paths like -[*1..3]-> instead of shortestPath.

The graph schema is:
{schema}

Examples of GOOD Cypher queries:
- To find all entities: MATCH (n) RETURN n.id, labels(n) LIMIT 25
- To find relationships: MATCH (a)-[r]->(b) RETURN a.id, type(r), b.id LIMIT 25
- To find connections between two things: MATCH path=(a)-[*1..3]-(b) WHERE toLower(a.id) CONTAINS 'lte' AND toLower(b.id) CONTAINS '5g' RETURN path LIMIT 10
- To find all about a topic: MATCH (n)-[r]-(m) WHERE toLower(n.id) CONTAINS 'keyword' RETURN n.id, type(r), m.id LIMIT 25

Generate ONLY the Cypher query, nothing else."""),
    ("human", "{question}")
])

# Create a custom answer prompt for nicely formatted responses
ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions based on knowledge graph data.
Given the user's question and the data retrieved from the knowledge graph, provide a clear, well-formatted answer.

FORMATTING RULES:
1. Use clear headings and bullet points for readability.
2. If the data contains relationships, explain them in plain English.
3. If data is empty or insufficient, say so honestly and suggest what the user could ask instead.
4. Keep the answer concise but informative.
5. Format technical terms in a readable way."""),
    ("human", """Question: {question}

Data from Knowledge Graph:
{context}

Please provide a clear, well-formatted answer:""")
])

cypher_chain = CYPHER_PROMPT | llm
answer_chain = ANSWER_PROMPT | llm


def ask_question(question):
    """Process a question through the knowledge graph RAG pipeline."""
    print(f"\n{'─'*50}")
    print(f"❓ Question: {question}")
    print(f"{'─'*50}")

    # Step 1: Generate Cypher query
    max_retries = 3
    context_data = None

    for attempt in range(max_retries):
        try:
            # Generate Cypher
            cypher_response = cypher_chain.invoke({"schema": schema, "question": question})
            cypher_query = cypher_response.content.strip()

            # Clean up the query (remove markdown code blocks if present)
            if cypher_query.startswith("```"):
                cypher_query = cypher_query.split("\n", 1)[1]  # Remove first line
                cypher_query = cypher_query.rsplit("```", 1)[0]  # Remove last ```
            cypher_query = cypher_query.strip()

            print(f"\n🔍 Generated Cypher (attempt {attempt+1}):")
            print(f"   {cypher_query}")

            # Execute the query
            context_data = graph.query(cypher_query)
            print(f"\n📦 Retrieved {len(context_data)} results from Neo4j")
            break

        except Exception as e:
            error_msg = str(e)
            print(f"\n⚠️  Query error (attempt {attempt+1}): {error_msg[:100]}...")

            if attempt < max_retries - 1:
                # Try a simpler fallback query
                print("   Retrying with a simpler approach...")
                # Add error context to help the LLM fix it
                question = f"{question} (IMPORTANT: Previous Cypher query failed with error: {error_msg[:200]}. Generate a simpler, valid query.)"
            else:
                # Final fallback: just get all related nodes
                print("   Using fallback query to search all nodes...")
                try:
                    # Search for any node matching keywords from the question
                    keywords = [w.lower() for w in question.split() if len(w) > 3][:5]
                    fallback_parts = " OR ".join([f"toLower(n.id) CONTAINS '{kw}'" for kw in keywords])
                    fallback_query = f"MATCH (n)-[r]-(m) WHERE {fallback_parts} RETURN n.id, type(r), m.id LIMIT 25"
                    print(f"   Fallback: {fallback_query}")
                    context_data = graph.query(fallback_query)
                except Exception:
                    context_data = []

    if not context_data:
        print("\n📭 No data found in the knowledge graph for this query.")
        print("   Try asking about specific entities that exist in the graph.")
        # Show what's available
        try:
            sample = graph.query("MATCH (n) RETURN DISTINCT labels(n) as type, n.id as name LIMIT 15")
            if sample:
                print("\n   📋 Available entities in the graph:")
                for item in sample:
                    print(f"      • {item.get('name', 'N/A')} ({item.get('type', 'N/A')})")
        except Exception:
            pass
        return

    # Step 2: Generate a nice answer
    try:
        context_str = "\n".join([str(item) for item in context_data])
        answer_response = answer_chain.invoke({
            "question": question,
            "context": context_str
        })

        print(f"\n{'━'*50}")
        print(f"💡 Answer:")
        print(f"{'━'*50}")
        print(answer_response.content)
        print(f"{'━'*50}")

    except Exception as e:
        print(f"\n⚠️  Error generating answer: {e}")
        print("\n📊 Raw data from knowledge graph:")
        for item in context_data[:10]:
            print(f"   • {item}")


def main():
    print("\n✅ Ready! Ask questions about your knowledge graph.")
    print("   Type 'exit' to quit, 'show' to see all entities\n")

    while True:
        question = input('\n🎤 Ask me a question: ').strip()

        if not question:
            continue
        if question.lower() == 'exit':
            print("\n👋 Goodbye!")
            break
        if question.lower() == 'show':
            try:
                nodes = graph.query("MATCH (n) RETURN labels(n) as type, n.id as name ORDER BY name LIMIT 50")
                rels = graph.query("MATCH ()-[r]->() RETURN DISTINCT type(r) as relationship LIMIT 20")
                print(f"\n📋 Entities in graph ({len(nodes)}):")
                for n in nodes:
                    print(f"   • {n.get('name', 'N/A')} [{', '.join(n.get('type', []))}]")
                print(f"\n🔗 Relationship types ({len(rels)}):")
                for r in rels:
                    print(f"   • {r.get('relationship', 'N/A')}")
            except Exception as e:
                print(f"Error: {e}")
            continue

        ask_question(question)


if __name__ == '__main__':
    main()
