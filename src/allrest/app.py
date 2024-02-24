import argparse
import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from allrest.utils import outputmanager
from allrest.restree import RESTree
from allrest.overflowmanager import OverflowManager
from allrest.forestoptimizer import ForestOptimizer
from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.forestoptimizerbuilder import ForestOptimizerBuilder
from allrest.steinertree import SteinerTree
from allrest.treeconverter import TreeConverter


def build_evaluator(weight_wirelength: float, weight_detour: float, weight_overflow: float, overflow_manager: OverflowManager):
    from allrest.restreelengthevaluator import RESTreeLengthEvaluator
    from allrest.restreedetourevaluator import RESTreeDetourEvaluator
    from allrest.restreeoverflowevaluator import RESTreeOverflowEvaluator
    from allrest.restreeweightedevaluator import RESTreeWeightedEvaluator
    from allrest.restreecompositeevaluator import RESTreeCompositeEvaluator

    length_evaluator = RESTreeLengthEvaluator()
    detour_evaluator = RESTreeDetourEvaluator()
    overflow_evaluator = RESTreeOverflowEvaluator(
        overflow_manager=overflow_manager)

    length_weighted_evaluator = RESTreeWeightedEvaluator(
        length_evaluator, weight_wirelength)
    detour_weighted_evaluator = RESTreeWeightedEvaluator(
        detour_evaluator, weight_detour)
    overflow_weighted_evaluator = RESTreeWeightedEvaluator(
        overflow_evaluator, weight_overflow)

    evaluators = [length_weighted_evaluator,
                  detour_weighted_evaluator, overflow_weighted_evaluator]
    return RESTreeCompositeEvaluator(evaluators=evaluators)


def find_res_file() -> str:
    subdirs_pattern = outputmanager.get_output_path("../output_*")
    outputmanager.info("subdirs_pattern:", subdirs_pattern)
    import glob
    subdirs = sorted(glob.glob(subdirs_pattern), reverse=True)
    outputmanager.info("subdirs:", subdirs)

    res_file = None
    for subdir in subdirs:
        if os.path.isdir(subdir):
            file_path = os.path.join(subdir, "res.txt")
            if os.path.exists(file_path):
                res_file = file_path
                break
    return res_file

def write_steiner_tree(restrees: List[RESTree], output_path: str):
    with open(output_path, "w") as f:
        for _, tree in enumerate(restrees):
            stt: SteinerTree = TreeConverter(tree).convert_to_steiner_tree()
            f.write("NET {}\n".format(tree.net_id))
            f.write("DEGREE {}\n".format(stt.deg))
            f.write("LENGTH {}\n".format(stt.length))
            f.write("BRANCH {}\n".format(len(stt.branch)))
            for branch in stt.branch:
                f.write("{} {} {}\n".format(branch.x, branch.y, branch.n))


def run(input_file: str, weight_wirelength: float, weight_detour: float, weight_overflow: float):
    builder = ForestOptimizerBuilder()
    res_file: str = find_res_file()
    restrees: List[RESTree] = builder.create_restrees(input_file, res_file)
    overflow_manager: OverflowManager = builder.create_overflow_manager(
        input_file)
    evaluator: RESTreeAbstractEvaluator = build_evaluator(weight_wirelength=weight_wirelength,
                                                          weight_detour=weight_detour,
                                                          weight_overflow=weight_overflow,
                                                          overflow_manager=overflow_manager)
    optimizer: ForestOptimizer = ForestOptimizer(restrees=restrees,
                                                 overflow_manager=overflow_manager,
                                                 evaluator=evaluator)
    optimizer.optimize()
    write_steiner_tree(optimizer.trees, output_path="output.txt")
    
    
        
        


def initialize_output(output_dir: str, log_level: str):
    import logging
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    level = log_level_map.get(log_level, logging.INFO)
    outputmanager.basicConfig(
        output_dir=output_dir,
        log_level=level,
        log_file_name="allrest.txt",
    )


def main():
    description = "ALLREST"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input_file", type=str,
                        help="Input file path", required=True)
    parser.add_argument("--outdir", type=str,
                        help="output directory", default=None)
    parser.add_argument("--loglevel", type=str,
                        help="log level", default="INFO")
    # parser.add_argument("--render", action="store_true", help="render results", default=False)
    # parser.add_argument("--target_iteration_ratio", type=int, help="#iterations per net", default=10)
    # parser.add_argument("--temperature", type=float, help="temperature", default=1.0)
    # parser.add_argument("--temperature_decay", type=float, help="temperature decay", default=0.9995)
    parser.add_argument("--weight_wirelength", type=float,
                        help="weight wirelength", default=0.1)
    parser.add_argument("--weight_detour", type=float,
                        help="weight detour", default=0.9)
    parser.add_argument("--weight_overflow", type=float,
                        help="weight overflow", default=0.5)
    args = parser.parse_args()

    initialize_output(output_dir=args.outdir, log_level=args.loglevel)

    run(input_file=args.input_file)


if __name__ == "__main__":
    main()
