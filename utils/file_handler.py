
def read_sales_data(filename):
    
    
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                raw_lines = file.readlines()

                # Skip header and empty lines
                for line in raw_lines[1:]:
                    line = line.strip()
                    if line:
                        lines.append(line)

            print(f"✓ File read successfully using encoding: {encoding}")
            return lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print("❌ Error: sales_data.txt file not found.")
            return []

    print("❌ Error: Unable to read file with supported encodings.")
    return []
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        try:
            transaction_id = parts[0].strip()
            date = parts[1].strip()
            product_id = parts[2].strip()
            product_name = parts[3].replace(',', '').strip()
            quantity = int(parts[4].replace(',', '').strip())
            unit_price = float(parts[5].replace(',', '').strip())
            customer_id = parts[6].strip()
            region = parts[7].strip()

            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }

            transactions.append(transaction)

        except ValueError:
            # Skip rows with conversion issues
            continue

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    # First pass: validation
    for t in transactions:
        try:
            if (
                not t['TransactionID'].startswith('T') or
                not t['ProductID'].startswith('P') or
                not t['CustomerID'].startswith('C') or
                t['Quantity'] <= 0 or
                t['UnitPrice'] <= 0 or
                not t['Region']
            ):
                invalid_count += 1
                continue

            amount = t['Quantity'] * t['UnitPrice']
            regions.add(t['Region'])
            amounts.append(amount)

            valid_transactions.append(t)

        except KeyError:
            invalid_count += 1

    # Display filter options
    print("Available Regions:", ", ".join(sorted(regions)))
    if amounts:
        print(f"Transaction Amount Range: ₹{min(amounts)} - ₹{max(amounts)}")

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }

    # Apply region filter
    if region:
        before = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if t['Region'] == region]
        summary['filtered_by_region'] = before - len(valid_transactions)

    # Apply amount filter
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)
        filtered = []

        for t in valid_transactions:
            amount = t['Quantity'] * t['UnitPrice']
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue
            filtered.append(t)

        valid_transactions = filtered
        summary['filtered_by_amount'] = before - len(valid_transactions)

    summary['final_count'] = len(valid_transactions)

    return valid_transactions, invalid_count, summary
