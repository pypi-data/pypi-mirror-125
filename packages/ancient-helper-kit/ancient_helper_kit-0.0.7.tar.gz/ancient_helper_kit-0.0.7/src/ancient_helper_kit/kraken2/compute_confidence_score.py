
import pandas as pd
from taxonomy import Taxonomy, TaxonomyError
import sys
from collections import defaultdict
from ancient_helper_kit.util.general import create_stdout_logger

from multiprocessing import Process, Queue


def get_c_q(read_descr,label, tax, taxonomy_err_dic):
    c,q = 0,0
    kmer_info = read_descr.split(' ')
    # test if the tax-id of the read is in my taxonomy
    if tax.node(label) is not None:
        for p in kmer_info:
            kmer_tax, no_kmers = p.split(':')
            if kmer_tax != 'A':
                if kmer_tax != '0':
                    try:
                        if tax.lca(kmer_tax, label).id == label:
                            c += int(no_kmers)
                    except TaxonomyError:
                        taxonomy_err_dic[kmer_tax] += 1
                    q += int(no_kmers)
                elif kmer_tax == '0':
                    q += int(no_kmers)
    else:
        taxonomy_err_dic[label] += len(kmer_info)
    return c,q


def compute_conf_score(input_fn, is_paired, output_fn, tax, queue):
    tax_err_dic = defaultdict(int)
    tl = []
    for line in open(input_fn):
        _, read, name, lengths, kmer_desc = line.strip().split("\t")
        label = name.strip(')').split('taxid ')[-1].strip()
        if is_paired:
            c, q = 0, 0
            for s in map(str.strip, kmer_desc.split('|:|')):
                if len(s) > 0:
                    ct, qt = get_c_q(read_descr=s,
                                     label=label, tax=tax,
                                     taxonomy_err_dic=tax_err_dic)
                    c += ct
                    q += qt
        else:
            c, q = get_c_q(read_descr=kmer_desc,
                           label=label,
                           taxonomy_err_dic=tax_err_dic)
        conf_score = c / q if q > 0 else 0
        tl.append([read, name, conf_score])

    pd.DataFrame(tl, columns=['read_name', 'tax_id', 'conf_score']).to_csv(output_fn,index=False)
    queue.put((is_paired,tax_err_dic))


def main(fn_tax_nodes, fn_tax_names, k2_classified_out_single, csv_single,
         k2_classified_out_paired, csv_paired, logger=None):
    tax = Taxonomy.from_ncbi(nodes_path=fn_tax_nodes,
                             names_path=fn_tax_names)

    if logger is not None:
        logger.info("loaded taxonomy")

    queue = Queue()
    p_single = Process(target=compute_conf_score, args=(k2_classified_out_single,
                                                        False, csv_single, tax, queue))
    p_single.start()

    p_paired = Process(target=compute_conf_score, args=(k2_classified_out_paired,
                                                        True, csv_paired, tax, queue))
    p_paired.start()

    p_paired.join()
    p_single.join()
    if logger is not None:
        logger.info("taxonomy errors of each run:")
        for i in range(2):
            is_paired, d = queue.get()
            logger.info(f"{'paired' if is_paired else 'single'}\n {d}")




