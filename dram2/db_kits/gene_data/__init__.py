"""
Count Heme Regulatory Motifs
----------------------------

This
"""
from typing import Optional
from dram2.db_kits.utils import DBKit
from dram2.utils.utils import Fasta
import pandas as pd
from skbio import read as read_sequence
from Bio import SeqIO

MOTIF = "(C..CH)"


class CountMotifsKit(DBKit):
    name = "stats"
    formal_name: str = "Genome_stats"
    version: Optional[str] = None
    citation: str = (
        'This kit is used to get genome stats produced by prodigal'
    )
    date: Optional[str] = None
    max_threads = 1

    def load_dram_config(self):
        pass

    def setup(self):
        pass

    def search(self, fasta: Fasta) -> pd.DataFrame:
        """
        Take the prodigal gene headers and get the scaffold that it came from
        Based on idba_ud 'scaffold_#' scaffold names with gene name after
        """
        df_dict = dict()
        with open(fasta.faa, 'r') as faa:
            for seq in read_sequence(faa, format="fasta"):
                split_label = seq.metadata["id"].split("_")
                scaffold = "_".join(split_label[:-1])
                gene_position = split_label[-1]
                start_position, end_position, strandedness = seq.metadata[
                    "description"
                ].split("#")[1:4]
                df_dict[seq.metadata["id"]] = [
                    scaffold,
                    int(gene_position),
                    int(start_position),
                    int(end_position),
                    int(strandedness),
                ]
        return pd.DataFrame.from_dict(
            df_dict,
            orient="index",
            columns=[
                "scaffold",
                "gene_position",
                "start_position",
                "end_position",
                "strandedness",
            ],
        )

    def get_descriptions(self, hits) -> pd.DataFrame:
        return hits
