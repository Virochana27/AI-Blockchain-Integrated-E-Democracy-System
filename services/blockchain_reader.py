from web3 import Web3
from config import Config
from utils.crypto import uuid_to_uint256
import json


def get_votes_from_chain(election_id, constituency_id=None):
    w3 = Web3(Web3.HTTPProvider(Config.WEB3_PROVIDER_URL))

    with open("blockchain/abi/VotingContractABI.json") as f:
        abi = json.load(f)

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(Config.VOTING_CONTRACT_ADDRESS),
        abi=abi
    )

    election_uint = uuid_to_uint256(election_id)

    # ✅ Web3.py v6+ compatible way
    events = contract.events.VoteCast.get_logs(
        from_block=0,
        argument_filters={
            "electionId": election_uint
        }
    )

    results = []
    for e in events:
        results.append({
            "candidate_id": str(e["args"]["candidateId"]),
            "timestamp": e["args"]["timestamp"]
        })

    return results
