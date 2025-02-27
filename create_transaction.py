import bitcoinlib
from bitcoinlib.keys import Key
from bitcoinlib.transactions import Transaction, Input, Output
from bitcoinlib.services.services import Service

def create_signed_transaction(target_address, amount, private_key_hex, network='bitcoin'):

    try:
        # 1. Import the private key and get the source address
        private_key = Key(private_key_hex, network=network)
        source_address = private_key.address()

        # 2. Create a service object to interact with the network
        service = Service(network=network)

        # 3. Fetch all UTXOs for the source address
        utxos = service.getutxos(source_address)
        if not utxos:
            return False, f"Saldo insuficiente. Endereço de origem ({source_address}) não possui UTXOs disponíveis."

        # 4. Calculate total available balance
        total_balance = sum(utxo['value'] for utxo in utxos)
        amount_satoshis = int(amount * 100000000)

        estimated_fee = 25 * 200

        # 6. Check if we have enough balance
        if total_balance < (amount_satoshis + estimated_fee):
            return False, f"Saldo insuficiente. Saldo disponível: {total_balance / 100000000} BTC, " \
                         f"Necessário: {(amount_satoshis + estimated_fee) / 100000000} BTC (incluindo a taxa)."

        # 7. Create inputs from UTXOs
        inputs = []
        total_input_amount = 0
        for utxo in utxos:
            if total_input_amount >= (amount_satoshis + estimated_fee):
                break
            inputs.append(Input(utxo['txid'], utxo['output_n'], address=source_address))
            total_input_amount += utxo['value']

        # 8. Create outputs
        outputs = [Output(amount_satoshis, target_address)]
        
        # Calculate and add change output if needed
        change_amount = total_input_amount - amount_satoshis - estimated_fee
        if change_amount > 546:  # Only create change output if it's more than dust amount
            outputs.append(Output(change_amount, source_address))

        # 9. Create and sign the transaction
        transaction = Transaction(inputs, outputs, network=network)
        transaction.sign(private_key)

        # 10. Return the signed transaction in hexadecimal format
        return True, transaction.raw_hex()

    except Exception as e:
        return False, f"Erro ao criar transação: {str(e)}"

if __name__ == '__main__':
    # Example usage (using testnet)
    target_address = '19oW7d21h2ziZ9MnMUidnpvKpbK4wMuppD'  # Example testnet address
    amount = 0.0009  # BTC
    # WARNING: Never hardcode private keys in production code!
    private_key_hex = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Example private key

    success, result = create_signed_transaction(target_address, amount, private_key_hex)
    
    if success:
        print(f"Signed Transaction: {result}")
    else:
        print(f"Failed to create transaction: {result}")
