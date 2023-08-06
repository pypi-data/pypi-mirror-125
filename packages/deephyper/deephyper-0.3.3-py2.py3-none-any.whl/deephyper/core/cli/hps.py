import sys
import argparse

from deephyper.search.util import load_attr
from deephyper.core.parser import add_arguments_from_signature
from deephyper.evaluator.evaluate import EVALUATORS, Evaluator

HPS_SEARCHES = {
    "ambs": "deephyper.search.hps.AMBS",
}


def build_parser_from(cls):
    parser = argparse.ArgumentParser(conflict_handler="resolve")

    # add the arguments of a specific search
    add_arguments_from_signature(parser, cls)

    # add argument of Search.search interface
    parser.add_argument(
        "--max-evals",
        default=-1,
        type=int,
        help="Type[int]. Defaults to '-1' when an number of evaluations is not imposed.",
    )
    parser.add_argument(
        "--timeout",
        default=None,
        type=int,
        help="Type[int]. Number of seconds before killing the search. Defaults to 'None' when a time budget is not imposed.",
    )

    # add arguments for evaluators
    evaluator_added_arguments = add_arguments_from_signature(parser, Evaluator)

    for eval_name, eval_cls in EVALUATORS.items():
        eval_cls = load_attr(f"deephyper.evaluator.{eval_cls}")
        add_arguments_from_signature(
            parser, eval_cls, prefix=eval_name, exclude=evaluator_added_arguments
        )

    return parser


def add_subparser(parsers):
    parser_name = "hps"

    parser = parsers.add_parser(
        parser_name, help="Command line to run hyperparameter search."
    )

    subparsers = parser.add_subparsers()

    for name, module_attr in HPS_SEARCHES.items():
        search_cls = load_attr(module_attr)

        search_parser = build_parser_from(search_cls)

        subparser = subparsers.add_parser(
            name=name, parents=[search_parser], conflict_handler="resolve"
        )

        subparser.set_defaults(func=main)


def main(**kwargs):

    sys.path.insert(0, ".")

    search_name = sys.argv[2]

    # load search class
    search_cls = load_attr(HPS_SEARCHES[search_name])

    # load problem
    problem = load_attr(kwargs.pop("problem"))

    # load run function
    run_function = load_attr(kwargs.pop("run_function"))

    # filter arguments from evaluator class signature
    evaluator_method = kwargs.pop("evaluator")
    base_arguments = ["num_workers", "callbacks"]
    evaluator_kwargs = {k:kwargs.pop(k) for k in base_arguments}

    for method in EVALUATORS.keys():
        evaluator_method_kwargs = {k:kwargs.pop(k) for k in kwargs.copy() if method in k}
        if method == evaluator_method:
            evaluator_kwargs = {**evaluator_kwargs, **evaluator_method_kwargs}

    # create evaluator
    evaluator = Evaluator.create(
        run_function, method=evaluator_method, method_kwargs=evaluator_kwargs
    )

    # filter arguments from search class signature
    # remove keys in evaluator_kwargs
    kwargs = {k:v for k,v in kwargs.items() if k not in evaluator_kwargs}
    max_evals = kwargs.pop("max_evals")
    timeout = kwargs.pop("timeout")

    # TODO: How about checkpointing and transfer learning?

    # execute the search
    # remaining kwargs are for the search
    search = search_cls(problem, evaluator, **kwargs)

    search.search(max_evals=max_evals, timeout=timeout)
