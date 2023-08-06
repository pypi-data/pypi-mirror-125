from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Mapping, Type, TypeVar
import os
import json
import yaml
from zuper_commons.fs import locate_files, read_ustring_from_utf8_file
from zuper_ipce import object_from_ipce

import duckietown_challenges as dc
from zuper_nodes import (
    ExternalProtocolViolation,
    IncompatibleProtocol,
    InteractionProtocol,
)
from zuper_nodes_wrapper.wrapper_outside import ComponentInterface
from . import logger

__all__ = ["run_checker"]

Y = TypeVar("Y")
S = TypeVar("S")
Params = TypeVar("Params")
Query = TypeVar("Query")


@dataclass
class CheckerSession:
    dataset: object
    scores: List
    responses: List


def run_checker(
    cie: dc.ChallengeInterfaceEvaluator,
    protocol: InteractionProtocol,
    *,
    dirname: str,
    K: Type[Y],
    scoring: Callable[[Params, Query, Y, Any], S],
    finalize_scores: Callable[[List[S]], Mapping[str, float]],
) -> Dict[str, CheckerSession]:
    if "replica" in os.environ:
        replica = json.loads(os.environ["replica"])
        index = replica["index"]
        total = replica["total"]
    else:
        index = 0
        total = 1

    logger.info(env=dict(os.environ), index=index, total=total)

    agent_ci = ComponentInterface(
        fnin="/fifos/checker-in",
        fnout="/fifos/checker-out",
        expect_protocol=protocol,
        nickname="checker",
    )
    try:

        # check compatibility so that everything
        # fails gracefully in case of error
        # noinspection PyProtectedMember
        try:
            agent_ci._get_node_protocol()
        except IncompatibleProtocol as e:
            msg = "Invalid protocol"
            raise dc.InvalidSubmission(msg) from e

        K_params = protocol.inputs["set_params"]
        K_query = protocol.inputs["query"]

        @dataclass
        class Interaction:
            query: K_query
            gt: K

        @dataclass
        class Data:
            params: K_params
            interactions: List[Interaction]

        a = locate_files(dirname, "*.tests.yaml")
        a = sorted(a)
        scores = []

        episodes = {}
        for k, fn in enumerate(a):
            if k % total != index:
                msg = f"Skipping k = {k} fn = {fn}"
                logger.warning(msg)
                continue
            responses = []
            data = read_ustring_from_utf8_file(fn)
            ydata = yaml.load(data, Loader=yaml.Loader)
            inside = object_from_ipce(ydata, Data)
            logger.info(fn=fn)
            agent_ci.write_topic_and_expect_zero("set_params", inside.params)
            for i, interaction in enumerate(inside.interactions):
                logger.info(f"set {k+1} of {len(a)} - query {i+1} of {len(inside.interactions)}")
                q = interaction.query
                r = interaction.gt
                msg = agent_ci.write_topic_and_expect("query", q, expect="response")
                response = msg.data
                scores.append(scoring(inside.params, q, r, response))
                responses.append(response)

            episodes[fn] = CheckerSession(dataset=inside, scores=scores, responses=responses)
        final_scores = finalize_scores(scores)

        for k, v in final_scores.items():
            cie.set_score(k, v)

    except ExternalProtocolViolation as e:
        msg = "The remote node has violated protocol"
        raise dc.InvalidSubmission(msg) from e
    except dc.InvalidSubmission:
        raise
    except BaseException as e:
        raise dc.InvalidEvaluator() from e

    finally:
        agent_ci.close()

    return episodes
