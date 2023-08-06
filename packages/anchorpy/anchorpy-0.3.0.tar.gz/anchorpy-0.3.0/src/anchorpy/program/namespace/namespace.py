"""This module deals with creating the program object's namespaces."""
from typing import Dict, Tuple

from solana.publickey import PublicKey
from anchorpy.program.namespace.rpc import (
    RpcFn,
    build_rpc_item,
)
from anchorpy.program.namespace.transaction import (
    TransactionFn,
    build_transaction_fn,
)

from anchorpy.coder.coder import Coder
from anchorpy.program.namespace.account import AccountClient, build_account
from anchorpy.program.namespace.simulate import (
    SimulateFn,
    build_simulate_item,
)
from anchorpy.program.namespace.instruction import (
    InstructionFn,
)
from anchorpy.program.common import parse_idl_errors
from anchorpy.idl import Idl
from anchorpy.provider import Provider


def build_namespace(  # noqa: WPS320
    idl: Idl,
    coder: Coder,
    program_id: PublicKey,
    provider: Provider,
) -> Tuple[
    Dict[str, RpcFn],
    Dict[str, InstructionFn],
    Dict[str, TransactionFn],
    Dict[str, AccountClient],
    Dict[str, SimulateFn],
]:
    """Generate all namespaces for a given program.

    Args:
        idl: The parsed IDL object.
        coder: The program's Coder object .
        program_id: The Program ID.
        provider: The program's provider.

    Returns:
        The program namespaces.
    """
    idl_errors = parse_idl_errors(idl)

    rpc = {}
    instruction = {}
    transaction = {}
    simulate = {}

    for idl_ix in idl.instructions:

        ix_item = InstructionFn(idl_ix, coder.instruction.build, program_id)
        tx_item = build_transaction_fn(idl_ix, ix_item)
        rpc_item = build_rpc_item(idl_ix, tx_item, idl_errors, provider)
        simulate_item = build_simulate_item(
            idl_ix,
            tx_item,
            idl_errors,
            provider,
            coder,
            program_id,
            idl,
        )

        name = idl_ix.name
        instruction[name] = ix_item
        transaction[name] = tx_item
        rpc[name] = rpc_item
        simulate[name] = simulate_item

    account = build_account(idl, coder, program_id, provider) if idl.accounts else {}
    return rpc, instruction, transaction, account, simulate
