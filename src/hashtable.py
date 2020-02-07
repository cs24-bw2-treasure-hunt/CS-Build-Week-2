import hashlib
import sys
from uuid import uuid4
import random
import json

def proof_of_work(last_proof,difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """
    # print("Searching for next proof", last_proof)
    block_string = json.dumps(last_proof)
    proof = 0
    #  TODO: Your code here
    while valid_proof(block_string, proof,difficulty) is False:
        proof += 1
    return proof


def valid_proof(last_proof, proof,difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?
    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    guess = f"{last_proof}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # print("guess_hash",guess_hash)
    return guess_hash[:difficulty] == "0"*difficulty