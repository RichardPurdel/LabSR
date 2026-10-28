import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

# Configurare credentiale Recombee
DB_NAME = 'universitatea-nationala-de-stiinte-si-tehnologie-politeh-dev'
PRIVATE_TOKEN = '784IOGAPV9v4xweXdVrU5ujg8XbzRV5nK35b9Dh1wH1TRabfYNKjpSoEsDfOX5Wq'
REGION = Region.EU_WEST 

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=REGION)
PATH_DATASET = 'best-selling-manga.csv'

def send_items():
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee...")
    
    requests = []
    
    for index, row in df.iterrows():
        # TODO 3: Generam un ID curat si unic legat de pozitia randului (1 .. 187)
        item_id = f"manga_{index + 1}"
        
        # Conversii de tip sigure
        raw_volumes = pd.to_numeric(row.get('No. of collected volumes', 0), errors='coerce')
        volumes = int(raw_volumes) if pd.notna(raw_volumes) else 0

        raw_sales = pd.to_numeric(row.get('Approximate sales in million(s)', 0.0), errors='coerce')
        sales = float(raw_sales) if pd.notna(raw_sales) else 0.0

        # TODO 4: Maparea valorilor reale din CSV
        properties = {
            "title": str(row['Manga series']),
            "author": str(row['Author(s)']),
            "publisher": str(row['Publisher']),
            "demographic": str(row['Demographic']),
            "volumes": volumes,
            "sales_in_millions": sales
        }
        
        requests.append(SetItemValues(item_id, properties, cascade_create=True))
        
        # Trimitere in loturi Batch de cate 100
        if len(requests) == 100:
            client.send(Batch(requests))
            requests = []
            print("S-a trimis primul lot de 100 item-uri...")
            
    if requests:
        client.send(Batch(requests))
        print(f"S-a trimis al doilea lot ({len(requests)} produse).")
        
    print("Finalizat! Toate item-urile au fost sincronizate cu fisierul CSV.")

if __name__ == "__main__":
    send_items()