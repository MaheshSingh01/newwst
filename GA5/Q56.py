import os, json, pandas as pd, io, re

def execute(question: str, parameter, file_bytes = None):
        total_sales_value = total_sales(parameter["_file_"])
        return total_sales_value
        
def total_sales(fileObj, sales_key="sales"):
    fileObj.file.seek(0)
    """
    Calculates the total sales from a JSONL file with potentially malformed data.

    Parameters:
    - file_path (str): Path to the JSONL file.
    - sales_key (str): The key used to extract sales values from JSON objects.

    Returns:
    - int: The total sum of sales values.
    """
    total_sales = 0

    def extract_sales_from_line(line):
        """Attempt to manually extract sales value from a malformed line."""
        match = re.search(rf'"{sales_key}":\s*(\d+)', line)
        return int(match.group(1)) if match else 0

    #with open(fileObj, "r", encoding="utf-8") as file:
    #fileObj = fileObj.read()
    for line in fileObj.file:
        line = str(line).strip()  # Remove leading/trailing whitespace
        try:
            # Try to decode the JSON line
            data = json.loads(line)
            total_sales += data.get(sales_key, 0)
        except json.JSONDecodeError:
            # If decoding fails, extract sales manually from the corrupted line
            sales_value = extract_sales_from_line(line)
            total_sales += sales_value
            #print(f"Corrupted line, sales extracted: {sales_value}")

    return total_sales

def phonetic_cluster(cities):
    clusters = {}
    #print(cities)
    for city in cities:
        found_cluster = False
        for cluster_city in clusters:
            if fuzz.ratio(city.lower(), cluster_city.lower()) > 80:  # Threshold for similarity
                clusters[cluster_city].append(city)
                found_cluster = True
                break
        if not found_cluster:
            clusters[city] = [city]

    city_to_cluster = {}
    for cluster_city, city_list in clusters.items():
        for city in city_list:
            city_to_cluster[city] = cluster_city

    return city_to_cluster

def get_parameters(question):
    # How many units of Gloves were sold in Guangzhou on transactions with at least 7 units?
    # Extract product (assuming it's a single word capitalized)
    product_match = re.findall(r"units of (\w+)", question)

    # Extract city (assuming it's a capitalized word after "in")
    city_match = re.findall(r"sold in (\w+)", question)

    # Extract units (assuming it's a number after "at least")
    units_match = re.findall(r"at least (\d+) units?", question)

    # Take the last occurrence if multiple matches exist
    product = product_match[-1] if product_match else None
    city = city_match[-1] if city_match else None
    units = int(units_match[-1]) if units_match else None
    
    return (product, units, city)
        
