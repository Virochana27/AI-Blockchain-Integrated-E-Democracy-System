from utils.helpers import sha256_hash, generate_transaction_id
from models.ledger import create_ledger_entry


# -----------------------------
# Blockchain Service (Logical Layer)
# -----------------------------

def create_blockchain_transaction(
    entity_type: str,
    entity_id: str,
    payload: str,
    block_number: int = None
):
    """
    Simulates a blockchain transaction:
    - Hashes payload
    - Generates transaction ID
    - Stores immutable ledger entry
    """

    transaction_hash = sha256_hash(payload)
    transaction_id = generate_transaction_id(prefix=entity_type)

    create_ledger_entry(
        entity_type=entity_type,
        entity_id=entity_id,
        transaction_hash=transaction_id,
        block_number=block_number
    )

    return {
        "transaction_id": transaction_id,
        "transaction_hash": transaction_hash
    }
